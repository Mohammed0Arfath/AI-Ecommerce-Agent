import sqlite3
import json
import re
from typing import Dict, List, Tuple, Optional

# Note: For production use, you would import ollama
import ollama

def get_table_schema(db_name='ecommerce.db') -> Dict[str, List[str]]:
    """
    Get the schema of all tables in the database.
    Returns a dictionary with table names as keys and column lists as values.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    schema = {}
    
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        for table_name in tables:
            table_name = table_name[0]
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            schema[table_name] = [col[1] for col in columns]
    except Exception as e:
        print(f"Error getting schema: {str(e)}")
    finally:
        conn.close()
    
    return schema

def get_sample_data(db_name='ecommerce.db', limit=3) -> Dict[str, List[Tuple]]:
    """
    Get sample data from each table to help with SQL generation.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    samples = {}
    
    try:
        schema = get_table_schema(db_name)
        for table_name in schema.keys():
            cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit};")
            samples[table_name] = cursor.fetchall()
    except Exception as e:
        print(f"Error getting sample data: {str(e)}")
    finally:
        conn.close()
    
    return samples

def natural_language_to_sql_fallback(question: str, db_name='ecommerce.db') -> str:
    """
    Fallback SQL generation for common queries when LLM is not available.
    This is a simplified version for demonstration purposes.
    """
    question_lower = question.lower()
    
    # Common patterns and their SQL equivalents
    if 'total sales' in question_lower:
        if 'item_id' in question_lower:
            # Extract item_id if mentioned
            match = re.search(r'item\s*id\s*(\d+)', question_lower)
            if match:
                item_id = match.group(1)
                return f"SELECT SUM(total_sales) as total_sales FROM total_sales WHERE item_id = {item_id};"
        return "SELECT SUM(total_sales) as total_sales FROM total_sales;"
    
    elif 'roas' in question_lower or 'return on ad spend' in question_lower:
        return """
        SELECT 
            a.item_id,
            a.ad_sales,
            a.ad_spend,
            CASE 
                WHEN a.ad_spend > 0 THEN ROUND(a.ad_sales / a.ad_spend, 2)
                ELSE 0 
            END as roas
        FROM ad_sales a 
        WHERE a.ad_spend > 0
        ORDER BY roas DESC;
        """
    
    elif 'highest cpc' in question_lower or 'cost per click' in question_lower:
        return """
        SELECT 
            item_id,
            ad_spend,
            clicks,
            CASE 
                WHEN clicks > 0 THEN ROUND(ad_spend / clicks, 2)
                ELSE 0 
            END as cpc
        FROM ad_sales 
        WHERE clicks > 0
        ORDER BY cpc DESC
        LIMIT 10;
        """
    
    elif 'eligibility' in question_lower:
        if 'false' in question_lower or 'not eligible' in question_lower:
            return "SELECT * FROM eligibility WHERE eligibility = 'FALSE';"
        return "SELECT * FROM eligibility;"
    
    elif 'impressions' in question_lower:
        return "SELECT item_id, SUM(impressions) as total_impressions FROM ad_sales GROUP BY item_id ORDER BY total_impressions DESC;"
    
    else:
        # Default query - show some basic stats
        return "SELECT COUNT(*) as total_products FROM (SELECT DISTINCT item_id FROM total_sales);"

def natural_language_to_sql(question: str, model='llama2', db_name='ecommerce.db') -> str:
    """
    Convert natural language question to SQL query.
    Falls back to pattern matching if Ollama is not available.
    """
    question_lower = question.lower()
    
    # Check for specific patterns that work better with fallback
    if ('roas' in question_lower or 'return on ad spend' in question_lower or 
        'highest cpc' in question_lower or 'cost per click' in question_lower):
        print("Using fallback for RoAS/CPC calculation...")
        return natural_language_to_sql_fallback(question, db_name)
    
    try:
        # Try to use Ollama if available
        import ollama
        
        schema = get_table_schema(db_name)
        samples = get_sample_data(db_name)
        
        # Create detailed schema description
        schema_description = []
        for table, columns in schema.items():
            schema_description.append(f"Table '{table}': {', '.join(columns)}")
            
            # Add sample data for context
            if table in samples and samples[table]:
                sample_row = samples[table][0]
                sample_desc = ', '.join([f"{col}={val}" for col, val in zip(columns, sample_row)])
                schema_description.append(f"  Sample: {sample_desc}")
        
        schema_str = '\n'.join(schema_description)
        
        prompt = f"""Given the following SQLite database schema and sample data:

{schema_str}

Important notes:
- The 'ad_sales' table contains advertising metrics (ad_sales, impressions, ad_spend, clicks, units_sold). When calculating CPC (Cost Per Click), use the formula: ad_spend / clicks from the 'ad_sales' table.
- The 'total_sales' table contains total sales data (total_sales, total_units_ordered)
- The 'eligibility' table contains product eligibility information
- RoAS (Return on Ad Spend) = ad_sales / ad_spend. When calculating RoAS, use the formula: ad_sales / ad_spend from the 'ad_sales' table.
- Use proper SQL syntax for SQLite
- Return only the SQL query, no explanations

Convert this natural language question into a SQLite SQL query:
Question: {question}

SQL Query:"""

        response = ollama.generate(model=model, prompt=prompt)
        sql_query = response['response'].strip()
        
        # Clean up the response - remove any markdown formatting
        sql_query = re.sub(r'```sql\s*', '', sql_query)
        sql_query = re.sub(r'```\s*', '', sql_query)
        sql_query = sql_query.strip()
        
        return sql_query
        
    except ImportError:
        print("Ollama not available, using fallback SQL generation...")
        return natural_language_to_sql_fallback(question, db_name)
    except Exception as e:
        print(f"Error with Ollama, using fallback: {str(e)}")
        return natural_language_to_sql_fallback(question, db_name)

def execute_sql_query(sql_query: str, db_name='ecommerce.db') -> Tuple[List[Tuple], List[str]]:
    """
    Execute SQL query and return results with column names.
    Returns (results, column_names)
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        
        # Get column names
        column_names = [description[0] for description in cursor.description] if cursor.description else []
        
        return results, column_names
    except Exception as e:
        raise Exception(f"SQL execution error: {str(e)}")
    finally:
        conn.close()

def format_results(results: List[Tuple], column_names: List[str]) -> str:
    """
    Format query results into a readable string.
    """
    if not results:
        return "No results found."
    
    if not column_names:
        return str(results)
    
    # Create a simple table format
    formatted = []
    
    # Header
    header = " | ".join(column_names)
    formatted.append(header)
    formatted.append("-" * len(header))
    
    # Rows
    for row in results:
        row_str = " | ".join([str(val) if val is not None else "NULL" for val in row])
        formatted.append(row_str)
    
    return "\n".join(formatted)

if __name__ == '__main__':
    # Test the interface
    print("Testing LLM Interface...")
    
    # Test schema retrieval
    schema = get_table_schema()
    print(f"Database schema: {schema}")
    
    # Test sample queries
    test_questions = [
        "What is the total sales?",
        "Calculate the RoAS",
        "Which product had the highest CPC?",
        "Show me products that are not eligible"
    ]
    
    for question in test_questions:
        print(f"\nQuestion: {question}")
        try:
            sql_query = natural_language_to_sql(question)
            print(f"Generated SQL: {sql_query}")
            
            results, columns = execute_sql_query(sql_query)
            formatted = format_results(results, columns)
            print(f"Results:\n{formatted}")
        except Exception as e:
            print(f"Error: {str(e)}")