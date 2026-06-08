# AI Research Assistant

An Agentic AI Research Assistant built using FastAPI, Streamlit, Groq, Tavily Search, Website Reader, and PDF Reader.

The assistant intelligently decides which tool to use based on the user's query and generates accurate, context-aware responses.

---

## Features

* Web Search using Tavily
* Website Content Extraction
* PDF Document Analysis
* AI-powered Tool Selection
* FastAPI Backend
* Streamlit Frontend
* Groq LLM Integration
* Ready for Render and Streamlit Cloud Deployment

---

## Architecture

```text
User
  │
  ▼
Streamlit Frontend
  │
  ▼
FastAPI Backend
  │
  ▼
Research Agent
  │
  ├── Web Search Tool
  ├── Website Reader Tool
  └── PDF Reader Tool
  │
  ▼
Groq LLM
  │
  ▼
Final Response
```

---

## Project Structure

```text
AI_Research_Assistant/

├── backend/
│   ├── main.py
│   ├── agent.py
│   ├── requirements.txt
│   ├── .env
│   │
│   ├── uploads/
│   │
│   └── tools/
│       ├── __init__.py
│       ├── web_search.py
│       ├── website_reader.py
│       └── pdf_reader.py
│
├── frontend/
│   ├── app.py
│   └── requirements.txt
│
├── .gitignore
└── README.md
```

---

## Tech Stack

### Backend

* FastAPI
* Python

### Frontend

* Streamlit

### AI Model

* Groq
* Llama 3.3 70B Versatile

### Tools

* Tavily Search API
* BeautifulSoup
* Requests
* PyMuPDF

---

## Installation

### Clone Repository

```bash
git clone <repository-url>

cd AI_Research_Assistant
```

---

## Backend Setup

Navigate to backend folder:

```bash
cd backend
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Run backend:

```bash
uvicorn main:app --reload
```

Backend URL:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

---

## Frontend Setup

Navigate to frontend folder:

```bash
cd frontend
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run Streamlit:

```bash
streamlit run app.py
```

Frontend URL:

```text
http://localhost:8501
```

---

## API Endpoints

### Home

```http
GET /
```

Response:

```json
{
  "message": "AI Research Assistant Running"
}
```

---

### Upload PDF

```http
POST /upload-pdf
```

Uploads a PDF for analysis.

Response:

```json
{
  "message": "PDF Uploaded Successfully"
}
```

---

### Ask Question

```http
POST /ask
```

Request:

```json
{
  "query": "Latest AI news"
}
```

Response:

```json
{
  "tool_used": "web_search",
  "answer": "..."
}
```

---

## Available Tools

### Web Search Tool

Uses Tavily Search API to retrieve real-time information from the internet.

Example:

```text
What are the latest developments in AI?
```

---

### Website Reader Tool

Reads and extracts content from webpages.

Example:

```text
Summarize https://fastapi.tiangolo.com/
```

---

### PDF Reader Tool

Extracts and analyzes text from uploaded PDF files.

Example:

```text
Summarize the uploaded PDF
```

---

## Tool Selection Process

The AI agent evaluates the user query and selects the most appropriate tool.

### Examples

#### Web Search

Input:

```text
Latest AI news
```

Tool Selected:

```text
web_search
```

---

#### Website Reader

Input:

```text
Summarize https://www.python.org/
```

Tool Selected:

```text
website_reader
```

---

#### PDF Reader

Input:

```text
Summarize the uploaded PDF
```

Tool Selected:

```text
pdf_reader
```

---

## Deployment

### Backend Deployment (Render)

Root Directory:

```text
backend
```

Build Command:

```bash
pip install -r requirements.txt
```

Start Command:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Environment Variables:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

### Frontend Deployment (Streamlit Cloud)

Main File:

```text
frontend/app.py
```

Environment Variable:

```env
BACKEND_URL=https://your-render-backend-url.onrender.com
```

---

## Future Improvements

* Multi-tool reasoning
* Research report generation
* Conversation memory
* Source citations
* RAG for PDFs
* Chat history
* Multi-PDF support
* Downloadable research reports

---

## Example Workflow

```text
User:
Compare the latest AI trends with my uploaded PDF.

Agent:
1. Read PDF
2. Search Latest AI Trends
3. Compare Information
4. Generate Final Report
```

---

## Author

Vamshi

Built as an Agentic AI portfolio project demonstrating:

* FastAPI
* Streamlit
* Groq
* Tool Calling
* Agentic AI
* Web Search
* PDF Processing
* Website Content Analysis
