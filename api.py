from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import json
import time
import base64
import io
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from llm_interface import natural_language_to_sql, execute_sql_query, format_results
import traceback

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set a nice style for matplotlib
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
def generate_chart(results, column_names, question="", chart_type="auto"):
    """
    Generate a chart based on query results.
    Returns base64 encoded image string.
    """
    if not results or not column_names:
        return None
    
    try:
        # Determine chart type based on data
        if len(column_names) < 2:
            return None
        
        # Convert results to lists for plotting
        if len(column_names) == 2:
            labels = [str(row[0]) for row in results]
            values = [float(row[1]) if isinstance(row[1], (int, float)) else 0 for row in results]
        else:
            # For multi-column data, use first column as labels and second as values
            labels = [str(row[0]) for row in results]
            values = [float(row[1]) if isinstance(row[1], (int, float)) else 0 for row in results]
        
        # Limit to top 10 items for readability
        if len(labels) > 10:
            labels = labels[:10]
            values = values[:10]
        
        plt.figure(figsize=(12, 8))
        
        # Determine chart type
        if chart_type == 'auto':
            if len(labels) <= 5 and all(isinstance(v, (int, float)) for v in values):
                chart_type = 'pie'
            else:
                chart_type = 'bar'
        
        if chart_type == 'bar':
            bars = plt.bar(labels, values, color=sns.color_palette("husl", len(labels)))
            plt.xlabel(column_names[0])
            plt.ylabel(column_names[1] if len(column_names) > 1 else 'Value')
            plt.xticks(rotation=45, ha='right')
            
            # Add value labels on bars
            for bar, value in zip(bars, values):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.01,
                        f'{value:.2f}' if isinstance(value, float) else str(value),
                        ha='center', va='bottom')
        
        elif chart_type == 'pie':
            plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
            plt.axis('equal')
        
        elif chart_type == 'line':
            plt.plot(labels, values, marker='o', linewidth=2, markersize=8)
            plt.xlabel(column_names[0])
            plt.ylabel(column_names[1] if len(column_names) > 1 else 'Value')
            plt.xticks(rotation=45, ha='right')
            plt.grid(True, alpha=0.3)
        
        # Set title
        title = f"Results for: {question}" if question else "Query Results"
        plt.title(title, fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        # Save to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        plt.close()
        
        return image_base64
        
    except Exception as e:
        print(f"Error generating chart: {str(e)}")
        plt.close()
        return None

@app.route('/')
def home():
    """
    Home endpoint with API information.
    """
    return jsonify({
        'message': 'AI Agent for E-commerce Data API',
        'version': '1.0.0',
        'endpoints': {
            '/query': 'POST - Submit natural language questions',
            '/stream_query': 'POST - Submit questions with streaming response',
            '/health': 'GET - Check API health'
        },
        'example_questions': [
            'What is the total sales?',
            'Calculate the RoAS (Return on Ad Spend)',
            'Which product had the highest CPC?',
            'Show me products that are not eligible'
        ]
    })

@app.route('/health')
def health():
    """
    Health check endpoint.
    """
    try:
        # Test database connection
        from llm_interface import get_table_schema
        schema = get_table_schema()
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'tables': list(schema.keys()) if schema else []
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@app.route('/query', methods=['POST'])
def query_data():
    """
    Main query endpoint for natural language questions.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        question = data.get('question')
        visualize = data.get('visualize', False)
        chart_type = data.get('chart_type', 'auto')
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        # Generate SQL query
        sql_query = natural_language_to_sql(question)
        
        # Execute query
        results, column_names = execute_sql_query(sql_query)
        
        # Format results
        formatted_results = format_results(results, column_names)
        
        response_data = {
            'question': question,
            'sql_query': sql_query,
            'results': results,
            'column_names': column_names,
            'formatted_results': formatted_results,
            'row_count': len(results)
        }
        
        # Generate visualization if requested
        if visualize and results and len(results) > 0:
            chart_image = generate_chart(results, column_names, question, chart_type)
            if chart_image:
                response_data['chart_image_base64'] = chart_image
        
        return jsonify(response_data)
        
    except Exception as e:
        error_details = {
            'error': str(e),
            'type': type(e).__name__,
            'traceback': traceback.format_exc()
        }
        return jsonify(error_details), 500

@app.route('/stream_query', methods=['POST'])
def stream_query_data():
    """
    Streaming query endpoint with real-time updates.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        question = data.get('question')
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        def generate():
            try:
                # Step 1: Processing
                yield f"data: {json.dumps({'status': 'thinking', 'message': 'Processing your question...'})}\n\n"
                time.sleep(0.5)
                
                # Step 2: SQL Generation
                yield f"data: {json.dumps({'status': 'generating_sql', 'message': 'Converting to SQL query...'})}\n\n"
                sql_query = natural_language_to_sql(question)
                yield f"data: {json.dumps({'status': 'sql_generated', 'sql_query': sql_query})}\n\n"
                time.sleep(0.5)
                
                # Step 3: Query Execution
                yield f"data: {json.dumps({'status': 'executing', 'message': 'Executing database query...'})}\n\n"
                results, column_names = execute_sql_query(sql_query)
                yield f"data: {json.dumps({'status': 'results_fetched', 'message': f'Found {len(results)} results'})}\n\n"
                time.sleep(0.5)
                
                # Step 4: Formatting Results
                yield f"data: {json.dumps({'status': 'formatting', 'message': 'Formatting results...'})}\n\n"
                formatted_results = format_results(results, column_names)
                
                # Step 5: Streaming the formatted response with typing effect
                yield f"data: {json.dumps({'status': 'typing_start', 'message': 'Generating response...'})}\n\n"
                
                response_text = f"Here are the results for your question: '{question}'\n\n{formatted_results}"
                
                for char in response_text:
                    yield f"data: {json.dumps({'status': 'typing', 'char': char})}\n\n"
                    time.sleep(0.02)  # Typing speed
                
                # Step 6: Complete
                final_data = {
                    'status': 'complete',
                    'question': question,
                    'sql_query': sql_query,
                    'results': results,
                    'column_names': column_names,
                    'formatted_results': formatted_results,
                    'row_count': len(results)
                }
                yield f"data: {json.dumps(final_data)}\n\n"
                
            except Exception as e:
                error_data = {
                    'status': 'error',
                    'error': str(e),
                    'type': type(e).__name__
                }
                yield f"data: {json.dumps(error_data)}\n\n"
        
        return Response(generate(), mimetype='text/event-stream',
                       headers={'Cache-Control': 'no-cache',
                               'Connection': 'keep-alive'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/schema')
def get_schema():
    """
    Get database schema information.
    """
    try:
        from llm_interface import get_table_schema, get_sample_data
        
        schema = get_table_schema()
        samples = get_sample_data(limit=2)
        
        return jsonify({
            'schema': schema,
            'sample_data': samples
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting AI Agent for E-commerce Data API...")
    print("Available endpoints:")
    print("  GET  /          - API information")
    print("  GET  /health    - Health check")
    print("  POST /query     - Submit questions")
    print("  POST /stream_query - Submit questions with streaming")
    print("  GET  /schema    - Get database schema")
    print("\nExample curl command:")
    print('curl -X POST -H "Content-Type: application/json" -d \'{"question": "What is the total sales?"}\' http://localhost:5000/query')
    
    app.run(host='0.0.0.0', port=5000, debug=True)