# AI Research Assistant

An Agentic AI Research Assistant built with FastAPI, Streamlit, Groq, Tavily Search, Website Reader, PDF Reader, and an autonomous document-generation agent.

The original RAG-style assistant remains available through `/ask`. The project now also includes `/agent`, which plans and executes a business-document workflow and generates a Microsoft Word `.docx` file.

## Features

* Web search using Tavily
* Website content extraction
* PDF document analysis
* AI-powered tool selection for research queries
* Autonomous planning for business document requests
* Reflection and self-check before final document generation
* Professional Word document generation with `python-docx`
* FastAPI backend
* Streamlit frontend
* Groq LLM integration

## Architecture

```text
User
  |
  v
Streamlit Frontend / API Client
  |
  v
FastAPI Backend
  |
  +-- /ask Research Agent
  |     +-- Web Search Tool
  |     +-- Website Reader Tool
  |     +-- PDF Reader Tool
  |     v
  |   Groq LLM Response
  |
  +-- /agent Autonomous Document Agent
        +-- Planner
        +-- Task Executor
        +-- Reflection / Self Check
        +-- Word Generator
        v
      generated_docs/*.docx
```

## Autonomous Agent Workflow

```text
User Request
  |
  v
Planner
  |
  v
Task Executor
  |
  v
Reflection / Self Check
  |
  v
Word Generator
  |
  v
API Response
```

The planner returns structured JSON containing:

* `document_type`
* `assumptions`
* `required_sections`
* `execution_plan`

Supported document types:

* Business Proposal
* Meeting Minutes
* Project Plan
* Technical Design
* Business Report
* SOP
* Product Specification
* Research Summary
* Implementation Plan

If details are missing, the agent makes reasonable business assumptions and includes them in the response.

## Project Structure

```text
AI_Research_Assistant/
|-- be/
|   |-- main.py
|   |-- agent.py
|   |-- requirements.txt
|   |-- uploads/
|   |-- generated_docs/
|   |-- autonomous_agent/
|   |   |-- __init__.py
|   |   |-- schemas.py
|   |   |-- llm.py
|   |   |-- planner.py
|   |   |-- executor.py
|   |   |-- reflection.py
|   |   |-- document_generator.py
|   |   |-- workflow.py
|   |-- tools/
|       |-- __init__.py
|       |-- web_search.py
|       |-- website_reader.py
|       |-- pdf_reader.py
|-- fe/
|   |-- app.py
|   |-- requirements.txt
|-- .gitignore
|-- README.md
```

## Backend Setup

```bash
cd be
pip install -r requirements.txt
```

Create a `.env` file in `be/`:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Run the backend:

```bash
uvicorn main:app --reload
```

Backend URL:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

## Frontend Setup

```bash
cd fe
pip install -r requirements.txt
streamlit run app.py
```

Frontend URL:

```text
http://localhost:8501
```

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

### Upload PDF

```http
POST /upload-pdf
```

Uploads a PDF for analysis.

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

### Autonomous Document Agent

```http
POST /agent
```

Request:

```json
{
  "request": "Create a business proposal for implementing AI customer support."
}
```

Response:

```json
{
  "status": "completed",
  "execution_plan": [
    "Understand the business request",
    "Identify assumptions",
    "Create the document outline",
    "Generate section content",
    "Review for completeness and tone",
    "Create the Word document"
  ],
  "assumptions": [
    "Assume a medium-sized business",
    "Budget is not specified",
    "Timeline is flexible"
  ],
  "document_type": "Business Proposal",
  "document_path": "generated_docs/business_proposal_20260706_101500.docx",
  "execution_time": "2.4 sec",
  "reflection": "No critical issues found."
}
```

Invalid input returns HTTP 400. If the LLM returns invalid JSON, the app retries once and then returns a structured error if parsing still fails.

## Sample Test Requests

```json
{
  "request": "Create meeting minutes for today's sprint planning meeting."
}
```

```json
{
  "request": "Prepare a business proposal for implementing AI customer support. No budget is available. Timeline is unknown. Decide reasonable assumptions yourself."
}
```

## Generated Documents

Word files are saved in:

```text
be/generated_docs/
```

Each file includes a title, assumptions, and professional document sections with formatted headings.

## Deployment

### Backend Deployment

Root directory:

```text
be
```

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Environment variables:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### Frontend Deployment

Main file:

```text
fe/app.py
```

Environment variable:

```env
BACKEND_URL=https://your-backend-url
```

## Future Improvements

* Multi-tool reasoning across uploaded files and web data
* Source citations in generated Word documents
* Conversation memory
* Multi-PDF support
* Download endpoint for generated documents

## Author

Vamshi
