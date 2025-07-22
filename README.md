# AI Agent for E-commerce Data

A powerful AI-driven web application that allows users to query e-commerce data using natural language. The system converts natural language questions into SQL queries, executes them against a database, and provides beautiful visualizations of the results.

## Features

- **Natural Language Processing**: Ask questions in plain English about your e-commerce data
- **AI-Powered SQL Generation**: Automatically converts questions to SQL queries using LLM (with fallback patterns)
- **Beautiful Web Interface**: Modern, responsive React frontend with intuitive design
- **Data Visualization**: Automatic chart generation for query results
- **Real-time Streaming**: Live typing effect for responses
- **Multiple Data Sources**: Supports ad sales, total sales, and product eligibility data
- **RESTful API**: Clean API endpoints for integration

## Architecture

- **Frontend**: React with Tailwind CSS and shadcn/ui components
- **Backend**: Flask API with CORS support
- **Database**: SQLite with e-commerce data
- **AI Integration**: Ollama for LLM (with intelligent fallback system)
- **Visualization**: Matplotlib for chart generation

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or pnpm

### Installation

1. **Extract the project files**
   ```bash
   # Extract the zip file to your desired location
   cd ai_ecommerce_agent
   ```

2. **Set up the backend**
   ```bash
   # Install Python dependencies
   pip install flask flask-cors pandas matplotlib seaborn
   
   # Optional: Install Ollama for enhanced AI capabilities
   # Download from https://ollama.com/download
   # ollama pull llama2
   ```

3. **Set up the database**
   ```bash
   python database.py
   ```

4. **Set up the frontend**
   ```bash
   cd frontend
   npm install
   # or if you have pnpm: pnpm install
   ```

### Running the Application

1. **Start the backend API**
   ```bash
   # From the root directory (ai_ecommerce_agent)
   python api.py
   ```
   The API will be available at `http://localhost:5000`

2. **Start the frontend (in a new terminal)**
   ```bash
   cd frontend
   npm run dev
   # or: pnpm run dev
   ```
   The web application will be available at `http://localhost:5173`

3. **Open your browser**
   Navigate to `http://localhost:5173` to use the application

## Usage

### Web Interface

1. **Query Interface Tab**
   - Enter your question in natural language
   - Click "Query Data" for basic results
   - Click "Query + Visualize" to include charts
   - Click "Stream Response" for real-time typing effect

2. **Example Queries Tab**
   - Pre-built sample questions
   - Click any example to run it instantly
   - View database schema information

### Example Questions

- "What is the total sales?"
- "Calculate the RoAS (Return on Ad Spend)"
- "Which product had the highest CPC?"
- "Show me products that are not eligible for advertising"
- "What are the top 10 products by impressions?"
- "Which products have the highest ad spend?"

### API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /query` - Submit natural language questions
- `POST /stream_query` - Submit questions with streaming response
- `GET /schema` - Get database schema

#### Example API Usage

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"question": "What is the total sales?", "visualize": true}' \
  http://localhost:5000/query
```

## Data Schema

The application works with three main data tables:

### Ad Sales Table
- `date`: Date of the record
- `item_id`: Product identifier
- `ad_sales`: Revenue from advertising
- `impressions`: Number of ad impressions
- `ad_spend`: Amount spent on advertising
- `clicks`: Number of ad clicks
- `units_sold`: Units sold through ads

### Total Sales Table
- `date`: Date of the record
- `item_id`: Product identifier
- `total_sales`: Total revenue
- `total_units_ordered`: Total units ordered

### Eligibility Table
- `eligibility_datetime_utc`: Timestamp
- `item_id`: Product identifier
- `eligibility`: Eligibility status (TRUE/FALSE)
- `message`: Eligibility message/reason

## Troubleshooting

### Common Issues

1. **"Module not found" errors**
   - Ensure all Python dependencies are installed: `pip install -r requirements.txt`

2. **Database not found**
   - Run `python database.py` to create and populate the database

3. **API connection errors**
   - Ensure the backend is running on port 5000
   - Check that CORS is enabled in the Flask app

4. **Frontend build errors**
   - Delete `node_modules` and run `npm install` again
   - Ensure Node.js version is 16 or higher

5. **Ollama not working**
   - The application has built-in fallback patterns
   - Install Ollama for enhanced AI capabilities (optional)

### Performance Tips

- For better AI responses, install and configure Ollama with a suitable model
- The fallback system handles common e-commerce queries without Ollama
- Use the visualization feature for better data insights

## Development

### Project Structure

```
ai_ecommerce_agent/
├── data/                          # CSV data files
├── frontend/                      # React application
│   ├── src/
│   │   ├── components/           # UI components
│   │   ├── App.jsx              # Main application
│   │   └── App.css              # Styles
│   └── package.json             # Frontend dependencies
├── database.py                   # Database setup
├── llm_interface.py             # AI/LLM integration
├── api.py                       # Flask API server
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

### Adding New Features

1. **New Query Patterns**: Add to `llm_interface.py` fallback patterns
2. **UI Components**: Use shadcn/ui components in the React frontend
3. **API Endpoints**: Add new routes in `api.py`
4. **Data Sources**: Modify `database.py` to include new CSV files

## License

This project is provided as-is for educational and demonstration purposes.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Verify all dependencies are installed
3. Ensure both backend and frontend are running
4. Check browser console for frontend errors
5. Check terminal output for backend errors

