import pandas as pd
import sqlite3
import os

def create_and_populate_db(db_name='ecommerce.db', data_folder='data'):
    """
    Create and populate SQLite database with e-commerce data from CSV files.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    try:
        # Product-Level Ad Sales and Metrics
        ad_sales_file = os.path.join(data_folder, 'Product-LevelAdSalesandMetrics(mapped)-Product-LevelAdSalesandMetrics(mapped).csv')
        if os.path.exists(ad_sales_file):
            ad_sales_df = pd.read_csv(ad_sales_file)
            ad_sales_df.to_sql('ad_sales', conn, if_exists='replace', index=False)
            print(f'Table ad_sales created and populated with {len(ad_sales_df)} rows.')
        else:
            print(f'Warning: {ad_sales_file} not found.')
        
        # Product-Level Total Sales and Metrics
        total_sales_file = os.path.join(data_folder, 'Product-LevelTotalSalesandMetrics(mapped)-Product-LevelTotalSalesandMetrics(mapped).csv')
        if os.path.exists(total_sales_file):
            total_sales_df = pd.read_csv(total_sales_file)
            total_sales_df.to_sql('total_sales', conn, if_exists='replace', index=False)
            print(f'Table total_sales created and populated with {len(total_sales_df)} rows.')
        else:
            print(f'Warning: {total_sales_file} not found.')
        
        # Product-Level Eligibility Table
        eligibility_file = os.path.join(data_folder, 'Product-LevelEligibilityTable(mapped)-Product-LevelEligibilityTable(mapped).csv')
        if os.path.exists(eligibility_file):
            eligibility_df = pd.read_csv(eligibility_file)
            eligibility_df.to_sql('eligibility', conn, if_exists='replace', index=False)
            print(f'Table eligibility created and populated with {len(eligibility_df)} rows.')
        else:
            print(f'Warning: {eligibility_file} not found.')
            
    except Exception as e:
        print(f'Error creating database: {str(e)}')
    finally:
        conn.close()

def get_database_info(db_name='ecommerce.db'):
    """
    Get information about the database tables and their schemas.
    """
    if not os.path.exists(db_name):
        print(f'Database {db_name} does not exist. Run create_and_populate_db() first.')
        return
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    try:
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f'\nDatabase: {db_name}')
        print('=' * 50)
        
        for table_name in tables:
            table_name = table_name[0]
            print(f'\nTable: {table_name}')
            print('-' * 30)
            
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            for col in columns:
                print(f'  {col[1]} ({col[2]})')
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f'  Rows: {count}')
            
    except Exception as e:
        print(f'Error getting database info: {str(e)}')
    finally:
        conn.close()

if __name__ == '__main__':
    print('Setting up e-commerce database...')
    create_and_populate_db()
    print('\nDatabase setup complete.')
    get_database_info()

