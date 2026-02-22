from fastapi import FastAPI, UploadFile, File
from rag.utils import extract_text_from_file, chunk_text
from pathlib import Path
import shutil
import os

from dotenv import load_dotenv
from pypdf import PdfReader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

EMBEDDING_MODEL = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=OPENAI_API_KEY
)

VECTOR_DB_DIR = Path("chroma_db")

vectorstore = Chroma(
    collection_name="documents",
    embedding_function=EMBEDDING_MODEL,
    persist_directory=str(VECTOR_DB_DIR)
)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    openai_api_key=OPENAI_API_KEY,
    temperature=0
)


@app.get("/")
def root():
    return {"message": "Mini RAG backend is running"}

def store_chunks_in_vector_db(chunks, filename):
    """
    Store text chunks and their embeddings in ChromaDB.
    """
    metadatas = [{"source": filename} for _ in chunks]

    vectorstore.add_texts(
        texts=chunks,
        metadatas=metadatas
    )

    vectorstore.persist()

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "status": "uploaded successfully"
    }
@app.get("/extract-text/{filename}")
def extract_text(filename: str):
    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        return {"error": "File not found"}

    text = extract_text_from_file(file_path)

    return {
        "filename": filename,
        "text_preview": text[:1000]  
    }

@app.get("/chunk-text/{filename}")
def chunk_file_text(filename: str):
    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        return {"error": "File not found"}

    text = extract_text_from_file(file_path)

    if not text.strip():
        return {"error": "No text extracted from file"}

    chunks = chunk_text(text)

    return {
        "filename": filename,
        "total_chunks": len(chunks),
        "sample_chunks": chunks[:3]  
    }
@app.post("/index/{filename}")
def index_file(filename: str):
    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        return {"error": "File not found"}

    text = extract_text_from_file(file_path)

    if not text.strip():
        return {"error": "No text extracted"}

    chunks = chunk_text(text)

    store_chunks_in_vector_db(chunks, filename)

    return {
        "filename": filename,
        "chunks_indexed": len(chunks),
        "status": "Embeddings stored successfully"
    }
@app.post("/ask")
def ask_question(question: str):
    docs = vectorstore.similarity_search(question, k=3)

    if not docs:
        return {"answer": "No relevant information found in documents."}

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
    Answer the question using ONLY the context below.
    If the answer is not present, say "I don't know".

    Context:
    {context}

    Question:
    {question}
    """

    response = llm.invoke(prompt)

    return {
        "question": question,
        "answer": response.content
    }