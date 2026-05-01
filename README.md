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

```
ai-business-copilot/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main FastAPI app
│   ├── routes/             # API endpoints
│   │   ├── auth.py         # Authentication routes
│   │   ├── upload.py       # File upload routes
│   │   ├── dashboard.py    # Dashboard data routes
│   │   └── chat.py         # Chat API routes
│   ├── database/           # Database operations
│   │   ├── db.py           # MongoDB connection
│   │   ├── models.py       # Data models
│   │   └── crud.py         # CRUD operations
│   └── services/           # Business logic
│       ├── file_service.py # File handling
│       ├── processing_service.py # Data processing
│       ├── rag_service.py  # RAG operations
│       └── config.py       # Configuration
├── rag/                    # RAG pipeline components
│   ├── data_interpreter.py # Data interpretation
│   ├── embedder.py         # Text embeddings
│   ├── vector_store.py     # FAISS vector store
│   ├── retriever.py        # Context retrieval
│   ├── llm.py              # LLM integration
│   └── prompts.py          # Prompt templates
├── models/                 # Business logic models
│   ├── metrics.py          # Metrics calculation
│   ├── rules.py            # Business rules engine
│   └── segmentation.py     # Data segmentation
├── data/                   # Data storage
│   ├── uploads/            # User uploaded files
│   └── vectorstores/       # User vector stores
├── frontend/               # Streamlit frontend
│   └── streamlit_app.py    # Main Streamlit app
└── docs/                   # Documentation
    └── architecture.pdf    # System architecture
```

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
