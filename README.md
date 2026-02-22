# AI Personal Knowledge Assistant (Mini RAG)

A simple AI-based system that allows users to upload their own documents (PDFs) and ask questions based strictly on the document content using Retrieval-Augmented Generation (RAG).

---

## Problem Statement

People often forget what information exists inside their own documents.  
This project enables users to query their documents using natural language and receive accurate, document-grounded answers.

---

## Features

- Upload PDF documents
- Index documents using vector embeddings
- Ask questions related to uploaded documents
- Answers are grounded in document content
- Avoids hallucinations by responding “I don’t know” when information is missing

---

## Tech Stack

### Backend
- Python
- FastAPI
- LangChain
- OpenAI API
- ChromaDB (vector database)
- PyPDF

### Frontend
- Streamlit

---

## Running the Application

### Start Backend (FastAPI)
- cd backend
- uvicorn main:app --reload

Backend will run at:
- http://127.0.0.1:8000

Swagger API Docs:
- http://127.0.0.1:8000/docs

### Start Frontend (Streamlit)
- cd frontend
- streamlit run app.py