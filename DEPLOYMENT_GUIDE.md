# AI Agent for E-commerce Data - Deployment Guide

This guide provides step-by-step instructions for setting up and running the AI Agent for E-commerce Data on your Windows system.

## System Requirements

- **Operating System**: Windows 10/11 (64-bit)
- **Python**: Version 3.8 or higher
- **Node.js**: Version 16 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: At least 2GB free space

## Step 1: Install Python

1. **Download Python**
   - Visit [python.org](https://python.org/downloads/)
   - Download the latest Python 3.x version for Windows
   - **Important**: During installation, check "Add Python to PATH"

2. **Verify Installation**
   ```cmd
   python --version
   pip --version
   ```

## Step 2: Install Node.js

1. **Download Node.js**
   - Visit [nodejs.org](https://nodejs.org/)
   - Download the LTS version for Windows
   - Run the installer with default settings

2. **Verify Installation**
   ```cmd
   node --version
   npm --version
   ```

## Step 3: Extract and Setup Project

1. **Extract the ZIP file**
   - Extract `ai_ecommerce_agent.zip` to your desired location
   - Example: `C:\Users\YourName\ai_ecommerce_agent`

2. **Open Command Prompt**
   - Press `Win + R`, type `cmd`, press Enter
   - Navigate to the project directory:
   ```cmd
   cd C:\Users\YourName\ai_ecommerce_agent
   ```

## Step 4: Setup Backend

1. **Install Python Dependencies**
   ```cmd
   pip install flask flask-cors pandas matplotlib seaborn
   ```
   
   Or use the requirements file:
   ```cmd
   pip install -r requirements.txt
   ```

2. **Setup Database**
   ```cmd
   python database.py
   ```
   
   You should see output like:
   ```
   Setting up e-commerce database...
   Table ad_sales created and populated with 3696 rows.
   Table total_sales created and populated with 702 rows.
   Table eligibility created and populated with 4381 rows.
   Database setup complete.
   ```

3. **Test Backend**
   ```cmd
   python api.py
   ```
   
   You should see:
   ```
   Starting AI Agent for E-commerce Data API...
   * Running on http://127.0.0.1:5000
   ```
   
   Keep this terminal open and running.

## Step 5: Setup Frontend

1. **Open New Command Prompt**
   - Open another Command Prompt window
   - Navigate to the frontend directory:
   ```cmd
   cd C:\Users\YourName\ai_ecommerce_agent\frontend
   ```

2. **Install Frontend Dependencies**
   ```cmd
   npm install
   ```
   
   This may take a few minutes to complete.

3. **Start Frontend**
   ```cmd
   npm run dev
   ```
   
   You should see:
   ```
   Local:   http://localhost:5173/
   ```

## Step 6: Access the Application

1. **Open Web Browser**
   - Open your preferred web browser (Chrome, Firefox, Edge)
   - Navigate to: `http://localhost:5173`

2. **Verify Connection**
   - You should see "API Connected • 3 tables loaded" at the top
   - If you see "API Disconnected", check that the backend is running

## Step 7: Test the Application

1. **Try a Simple Query**
   - In the text area, type: "What is the total sales?"
   - Click "Query Data"
   - You should see results showing the total sales amount

2. **Test Visualization**
   - Type: "Which product had the highest CPC?"
   - Click "Query + Visualize"
   - You should see both a chart and data table

3. **Try Example Queries**
   - Click the "Example Queries" tab
   - Click any "Visualize" button to test pre-built queries

## Optional: Install Ollama (Enhanced AI)

For better AI responses, you can install Ollama:

1. **Download Ollama**
   - Visit [ollama.com/download/windows](https://ollama.com/download/windows)
   - Download and install Ollama for Windows

2. **Install a Model**
   ```cmd
   ollama pull llama2
   ```

3. **Start Ollama Service**
   ```cmd
   ollama serve
   ```

The application will automatically use Ollama if available, otherwise it uses built-in fallback patterns.

## Troubleshooting

### Backend Issues

**Error: "Module not found"**
```cmd
pip install flask flask-cors pandas matplotlib seaborn
```

**Error: "Database not found"**
```cmd
python database.py
```

**Error: "Port 5000 already in use"**
- Close other applications using port 5000
- Or modify `api.py` to use a different port

### Frontend Issues

**Error: "npm not recognized"**
- Reinstall Node.js and ensure it's added to PATH
- Restart Command Prompt

**Error: "Module not found" (Frontend)**
```cmd
cd frontend
rm -rf node_modules
npm install
```

**Error: "Port 5173 already in use"**
- The frontend will automatically use the next available port
- Check the terminal output for the actual URL

### Browser Issues

**"API Disconnected" message**
- Ensure backend is running on port 5000
- Check Windows Firewall settings
- Try accessing `http://localhost:5000/health` directly

**Charts not displaying**
- Ensure matplotlib is installed: `pip install matplotlib`
- Try refreshing the browser page

## Running in Production

For production deployment:

1. **Use a Production WSGI Server**
   ```cmd
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 api:app
   ```

2. **Build Frontend for Production**
   ```cmd
   cd frontend
   npm run build
   ```

3. **Serve Static Files**
   - Use a web server like Nginx or Apache
   - Or serve through Flask with the built files

## Stopping the Application

1. **Stop Frontend**
   - In the frontend terminal, press `Ctrl + C`

2. **Stop Backend**
   - In the backend terminal, press `Ctrl + C`

## File Structure

```
ai_ecommerce_agent/
├── data/                     # CSV data files
│   ├── Product-LevelAdSalesandMetrics(mapped)-Product-LevelAdSalesandMetrics(mapped).csv
│   ├── Product-LevelTotalSalesandMetrics(mapped)-Product-LevelTotalSalesandMetrics(mapped).csv
│   └── Product-LevelEligibilityTable(mapped)-Product-LevelEligibilityTable(mapped).csv
├── frontend/                 # React web application
│   ├── src/                 # Source code
│   ├── public/              # Static assets
│   ├── package.json         # Dependencies
│   └── ...
├── database.py              # Database setup script
├── llm_interface.py         # AI/LLM integration
├── api.py                   # Flask API server
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
├── DEPLOYMENT_GUIDE.md     # This guide
└── ecommerce.db            # SQLite database (created after setup)
```

## Support

If you encounter issues:

1. **Check Prerequisites**: Ensure Python and Node.js are properly installed
2. **Verify Ports**: Make sure ports 5000 and 5173 are available
3. **Check Logs**: Look at terminal output for error messages
4. **Restart Services**: Stop and restart both backend and frontend
5. **Browser Cache**: Clear browser cache or try incognito mode

## Next Steps

Once the application is running:

1. **Explore Sample Queries**: Use the Example Queries tab
2. **Try Custom Questions**: Ask your own questions about the data
3. **Use Visualizations**: Enable charts for better insights
4. **API Integration**: Use the REST API for custom integrations

The application is now ready for use with your e-commerce data analysis needs!

