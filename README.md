# AI Agent for E-commerce Data

A powerful AI-driven web application that allows users to query e-commerce data using natural language. The system converts natural language questions into SQL queries, executes them against a database, and provides beautiful visualizations of the results.

<img width="2816" height="1536" alt="Gemini_Generated_Image_58fu3i58fu3i58fu" src="https://github.com/user-attachments/assets/1d0df92d-0342-4310-a07a-e45c4d4c37ef" />


> **📌 Tip**: Want to see it in action? Check out the live demo GIF below!

![Demo GIF](./Third-video---Made-with-Clipchamp.gif)

---

## ✨ Features

* **🧠 Natural Language Processing**: Ask questions in plain English about your e-commerce data
* **🪄 AI-Powered SQL Generation**: Automatically converts questions to SQL queries using LLM (with fallback patterns)
* **🌈 Beautiful Web Interface**: Modern, responsive React frontend with Tailwind and shadcn/ui
* **📊 Data Visualization**: Auto-generates visual insights from query results
* **💬 Real-time Streaming**: Typing animation for LLM responses
* **📂 Multiple Data Sources**: Ad sales, total sales, eligibility data supported
* **🔗 RESTful API**: Clean endpoints for integration into other systems

---

## 🏗️ Architecture

* **Frontend**: React (Vite) + Tailwind CSS + shadcn/ui
* **Backend**: Flask REST API with CORS support
* **Database**: SQLite with preloaded data
* **AI Integration**: Local LLM via Ollama (fallback logic included)
* **Visualization**: Matplotlib/Seaborn for charts

```mermaid
### 🧠 System Architecture

graph TD
    subgraph Frontend [🌐 Frontend (React/Vite)]
        A1[User Interface]
        A2[Search & Chat UI]
        A1 --> A2
    end

    subgraph Backend [🛠️ Backend (Python Flask API)]
        B1[API Layer (api.py)]
        B2[LLM Interface (llm_interface.py)]
        B3[Database Layer (database.py)]
        B4[SQLite DB (ecommerce.db)]
        B1 --> B2
        B1 --> B3
        B3 --> B4
    end

    subgraph AI Engine [🤖 LLM Engine]
        C1[Ollama (local LLM runtime)]
        C2[Model: llama2 or phi3:mini]
        C1 --> C2
    end

    subgraph Deployment [🚀 Deployment]
        D1[Netlify (Frontend)]
        D2[Render/VM (Backend & Ollama)]
    end

    A2 -->|API Calls| B1
    B2 -->|Prompt + Context| C1
    C1 -->|LLM Response| B2
    B1 -->|Returns JSON| A2

    A1 -->|Static Assets| D1
    B1 -->|API Host| D2
```

---

## 🚀 Quick Start

### Prerequisites

* Python 3.8+
* Node.js 16+
* `npm` or `pnpm`

### Installation Steps

```bash
# 1. Extract the zip file
cd ai_ecommerce_agent

# 2. Backend setup
pip install flask flask-cors pandas matplotlib seaborn

# Optional: Install Ollama for LLM
# https://ollama.com/download
# ollama pull llama2

# 3. Set up the database
python database.py

# 4. Frontend setup
cd frontend
npm install  # or: pnpm install
```

### Running the App

```bash
# 1. Backend
cd ../  # Root directory
python api.py
# API will be at http://localhost:5000

# 2. Frontend (in new terminal)
cd frontend
npm run dev
# Frontend will be at http://localhost:5173
```

---

## 🌐 Usage

### Web Interface

* **Query Interface**: Ask questions, visualize answers, get live responses
* **Example Queries**: One-click examples and schema info

### Example Natural Language Queries

* "What is the total sales?"
* "Calculate the RoAS (Return on Ad Spend)"
* "Which product had the highest CPC?"
* "Show me products not eligible for advertising"
* "Top 10 products by impressions"

---

## 📡 API Endpoints

| Endpoint        | Method | Description                     |
| --------------- | ------ | ------------------------------- |
| `/`             | GET    | API home                        |
| `/health`       | GET    | Health check                    |
| `/query`        | POST   | Submit a natural language query |
| `/stream_query` | POST   | Real-time typing stream query   |
| `/schema`       | GET    | Get DB schema                   |

### Example cURL

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"question": "What is the total sales?", "visualize": true}' \
  http://localhost:5000/query
```

---

## 🧾 Data Schema

### Ad Sales Table

* `date`, `item_id`, `ad_sales`, `impressions`, `ad_spend`, `clicks`, `units_sold`

### Total Sales Table

* `date`, `item_id`, `total_sales`, `total_units_ordered`

### Eligibility Table

* `eligibility_datetime_utc`, `item_id`, `eligibility`, `message`

---

## 🛠️ Troubleshooting

| Issue               | Fix                                          |
| ------------------- | -------------------------------------------- |
| Module not found    | `pip install -r requirements.txt`            |
| DB not found        | Run `python database.py`                     |
| API not connecting  | Ensure Flask is running at `:5000` with CORS |
| Frontend crashes    | `rm -rf node_modules && npm install`         |
| Ollama memory issue | Use fallback mode (see terminal logs)        |

---

## 📁 Project Structure

```
ai_ecommerce_agent/
├── data/                          # CSV data files
├── frontend/                      # React UI
│   ├── src/components/            # UI Components
│   ├── App.jsx                    # Main App
│   └── App.css                    # Styling
├── database.py                   # DB init
├── llm_interface.py              # AI logic
├── api.py                        # Flask API
├── requirements.txt              # Python deps
├── README.md                     # You're here ✨
```

---

## 🔧 Dev Guide

* Add new fallback prompts → `llm_interface.py`
* Add API routes → `api.py`
* Add UI components → `frontend/src/components`
* Add new data → `database.py` and `data/`

---

## 📄 License

This project is open-source and available for educational/demo purposes.

---

## 🤝 Support & Contributions

* Star the repo ⭐ if it helped you!
* PRs welcome for new features or bugfixes 🙌
* For issues, open GitHub Issues or reach out!

---

