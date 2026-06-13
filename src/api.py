"""
FilingIQ Production API
FastAPI backend for FilingIQ RAG system
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
from typing import List

sys.path.insert(0, '.')
from config import CHROMA_PATH, GROQ_API_KEY, LLM_BASE_URL, LLM_MODEL
from src.retrieve import Retriever, generate_answer

# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title="FilingIQ API",
    description="RAG system for Indian company filings",
    version="1.0.0"
)

# CORS - Allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# DATA MODELS
# ============================================================================

class QueryRequest(BaseModel):
    """User query request"""
    question: str

class Source(BaseModel):
    """Source chunk"""
    id: str
    company: str
    year: str
    page: int
    relevance: float
    content: str

class QueryResponse(BaseModel):
    """Full response with all details (for CLI/debugging)"""
    answer: str
    sources: List[Source]
    chunks_used: int

class SimpleQueryResponse(BaseModel):
    """Simple response for frontend UI"""
    answer: str
    sources: List[str]  # Just ["Company | Year | Page", ...]

# ============================================================================
# GLOBAL RETRIEVER (loaded once)
# ============================================================================

retriever = None

@app.on_event("startup")
async def startup_event():
    """Initialize retriever on startup"""
    global retriever
    try:
        retriever = Retriever(chroma_path=CHROMA_PATH)
        print(f"✅ Retriever initialized with {retriever.collection.count()} chunks")
    except Exception as e:
        print(f"❌ Failed to initialize retriever: {e}")

# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    if retriever and retriever.collection:
        return {
            "status": "healthy",
            "chunks_indexed": retriever.collection.count(),
            "message": "FilingIQ API is running"
        }
    else:
        return {
            "status": "unhealthy",
            "chunks_indexed": 0,
            "message": "Retriever not initialized"
        }

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Full query endpoint (for debugging/CLI)
    Returns answer with all source details and relevance scores
    """
    if not retriever or not retriever.collection:
        raise HTTPException(status_code=503, detail="Service not initialized")

    if not request.question or len(request.question.strip()) == 0:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        # Retrieve relevant chunks
        chunks = retriever.retrieve(request.question, top_k=3)

        # Generate answer
        result = generate_answer(request.question, chunks)

        # Format sources with details
        sources = [
            Source(
                id=chunk.id,
                company=chunk.metadata.get("company", "Unknown"),
                year=chunk.metadata.get("year", "?"),
                page=chunk.metadata.get("page_number", 0),
                relevance=round(chunk.rerank_score, 2),
                content=chunk.content[:200] + "..." if len(chunk.content) > 200 else chunk.content
            )
            for chunk in result["sources"]
        ]

        return QueryResponse(
            answer=result["answer"],
            sources=sources,
            chunks_used=result["chunks_used"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.post("/chat", response_model=SimpleQueryResponse)
async def chat_endpoint(request: QueryRequest):
    """
    Simple query endpoint for frontend UI
    Returns just the answer text + simple source list
    Perfect for web/mobile UI
    """
    if not retriever or not retriever.collection:
        raise HTTPException(status_code=503, detail="Service not initialized")

    if not request.question or len(request.question.strip()) == 0:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        # Retrieve relevant chunks
        chunks = retriever.retrieve(request.question, top_k=3)

        # Generate answer
        result = generate_answer(request.question, chunks)

        # Format sources as simple strings
        sources = [
            f"{chunk.metadata.get('company', '?')} | {chunk.metadata.get('year', '?')} | Page {chunk.metadata.get('page_number', '?')}"
            for chunk in result["sources"]
        ]

        return SimpleQueryResponse(
            answer=result["answer"],
            sources=sources
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint - API documentation"""
    return {
        "name": "FilingIQ API",
        "version": "1.0.0",
        "description": "RAG system for Indian company filings",
        "docs": "/docs",
        "endpoints": {
            "health": "GET /health",
            "query_detailed": "POST /query (for debugging)",
            "query_simple": "POST /chat (for frontend UI)"
        }
    }

# ============================================================================
# RUN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )