from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.core.rag_engine import RAGEngine
import os

app = FastAPI(title="Enterprise RAG Ops API")
rag_engine = RAGEngine()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]

@app.on_event("startup")
async def startup_event():
    # In a real app, we might check if DB exists or run ingestion
    if os.path.exists("chroma_db"):
        rag_engine.load_vector_store()
        rag_engine.setup_qa_chain()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    try:
        result = rag_engine.query(request.question)
        sources = [doc.metadata.get("source", "unknown") for doc in result["source_documents"]]
        return QueryResponse(
            answer=result["result"],
            sources=list(set(sources))
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest")
async def ingest_docs():
    try:
        rag_engine.ingest_documents()
        rag_engine.setup_qa_chain()
        return {"message": "Ingestion successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
