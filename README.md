# AI Business Copilot

A multi-user, full-stack AI system for business data analysis and strategy generation.

## Features

- CSV data upload and processing
- Automated metrics and insights generation
- RAG-powered business strategy and advertisement ideas
- CPU-only architecture using free tools

## Tech Stack

- Backend: FastAPI (Python)
- Database: MongoDB (local)
- Vector DB: FAISS
- LLM: Ollama (Mistral)
- Frontend: Streamlit

## Project Structure

```plaintext
ai-business-copilot/
│
├── backend/                         # FastAPI Backend
│   ├── main.py
│   │
│   ├── routes/                     # API Routes
│   │   ├── auth.py
│   │   ├── upload.py
│   │   ├── dashboard.py
│   │   └── chat.py
│   │
│   ├── database/                   # Database Layer
│   │   ├── db.py
│   │   ├── models.py
│   │   └── crud.py
│   │
│   └── services/                   # Business Logic
│       ├── file_service.py
│       ├── processing_service.py
│       ├── rag_service.py
│       └── config.py
│
├── rag/                            # RAG Pipeline
│   ├── data_interpreter.py
│   ├── embedder.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── llm.py
│   └── prompts.py
│
├── models/                         # Business Intelligence Models
│   ├── metrics.py
│   ├── rules.py
│   └── segmentation.py
│
├── data/                           # Storage
│   ├── uploads/
│   └── vectorstores/
│
├── frontend/                       # React + Vite Frontend
│   ├── public/
│   │
│   ├── src/
│   │   ├── components/
│   │   │   ├── charts/
│   │   │   ├── dashboard/
│   │   │   ├── chat/
│   │   │   └── ui/
│   │   │
│   │   ├── pages/
│   │   │   ├── Landing.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Upload.jsx
│   │   │   └── Chat.jsx
│   │   │
│   │   ├── services/
│   │   │   └── api.js
│   │   │
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   │
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── docs/
│   └── architecture.pdf
│
├── .gitignore
├── README.md
└── requirements.txt
```
# ⚙️ Backend Setup

```bash
cd backend

pip install -r requirements.txt

uvicorn main:app --reload
```

Backend runs on:

```plaintext
http://127.0.0.1:8000
```

---

# 💻 Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend runs on:

```plaintext
http://localhost:5173
```
---

## Setup Instructions

1. Install dependencies (we'll add these as we build)
2. Set up MongoDB locally
3. Install Ollama and pull Mistral model
4. Run the backend and frontend

## Development Roadmap

1. Project setup and folder structure
2. FastAPI app setup
3. MongoDB connection and authentication
4. File upload system
5. CSV processing and data interpretation
6. Metrics and rule engine
7. RAG pipeline (FAISS + embeddings)
8. LLM integration (Ollama)
9. Chat API
10. Dashboard API
11. Streamlit frontend
