"""
FilingIQ Retrieval Pipeline
Query → Embed → Search ChromaDB → Rerank → Format for LLM → Call Groq LLM
"""

import sys
import os
from dataclasses import dataclass
import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder
from rank_bm25 import BM25Okapi
import chromadb

sys.path.insert(0, '.')
from config import (
    CHROMA_PATH, EMBEDDING_MODEL, RERANKER_MODEL,
    TOP_K_RETRIEVAL, TOP_K_RERANK, GROQ_API_KEY, LLM_BASE_URL, LLM_MODEL
)

from openai import OpenAI

# ============================================================================
# DATACLASSES
# ============================================================================

@dataclass
class RetrievedChunk:
    """A chunk retrieved from the vector store"""
    id: str
    content: str
    metadata: dict
    embedding_score: float
    rerank_score: float = 0.0

# ============================================================================
# RETRIEVAL
# ============================================================================

class Retriever:
    """Hybrid retrieval: BM25 + vector search + reranking"""

    def __init__(self, chroma_path: str = CHROMA_PATH):
        self.chroma_path = chroma_path
        self.client = chromadb.PersistentClient(path=chroma_path)
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        self.reranker = CrossEncoder(RERANKER_MODEL)
        
        # Load collection
        try:
            self.collection = self.client.get_collection(name="filingiq")
            print(f"✅ ChromaDB collection loaded ({self.collection.count()} chunks)")
        except Exception as e:
            print(f"❌ Collection error: {e}")
            self.collection = None

    def embed_query(self, query: str) -> np.ndarray:
        """Embed the user's query"""
        return self.embedding_model.encode(query, normalize_embeddings=True)

    def vector_search(self, query_embedding: np.ndarray, top_k: int = TOP_K_RETRIEVAL) -> list:
        """Vector similarity search"""
        if not self.collection:
            return []

        try:
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=top_k,
                include=["documents", "metadatas", "distances"]
            )

            chunks = []
            for i in range(len(results["ids"][0])):
                chunks.append(RetrievedChunk(
                    id=results["ids"][0][i],
                    content=results["documents"][0][i],
                    metadata=results["metadatas"][0][i],
                    embedding_score=1 - results["distances"][0][i]  # Convert distance to similarity
                ))
            return chunks
        except Exception as e:
            print(f"Vector search error: {e}")
            return []

    def rerank(self, query: str, chunks: list, top_k: int = TOP_K_RERANK) -> list:
        """Rerank chunks using cross-encoder"""
        if not chunks:
            return []

        # Score each chunk
        pairs = [(query, chunk.content) for chunk in chunks]
        scores = self.reranker.predict(pairs)

        # Sort by score
        for chunk, score in zip(chunks, scores):
            chunk.rerank_score = float(score)

        chunks = sorted(chunks, key=lambda c: c.rerank_score, reverse=True)
        return chunks[:top_k]

    def retrieve(self, query: str, top_k: int = TOP_K_RERANK) -> list:
        """Full retrieval pipeline: embed → vector search → rerank"""
        print(f"\n🔍 Retrieving for: {query}")

        # Embed query
        query_embedding = self.embed_query(query)

        # Vector search
        candidates = self.vector_search(query_embedding, top_k=TOP_K_RETRIEVAL)
        print(f"   ✓ Vector search: {len(candidates)} candidates")

        if not candidates:
            print("   ✗ No chunks found")
            return []

        # Rerank
        reranked = self.rerank(query, candidates, top_k=top_k)
        print(f"   ✓ Reranked: {len(reranked)} chunks")

        return reranked

# ============================================================================
# PROMPT FORMATTING
# ============================================================================

SYSTEM_PROMPT = """You are FilingIQ, a financial research assistant for Indian company filings.

RULES:
1. Answer ONLY using the provided SOURCE BLOCKS
2. Cite every fact: [SOURCE N] after each sentence with a claim
3. If context is insufficient, respond: "The indexed documents do not contain sufficient information to answer this question."
4. Do NOT use training knowledge about these companies
5. Reproduce numbers exactly as they appear
6. Keep answers concise (3-5 sentences for facts, up to 2 paragraphs for analysis)

Format citations as: "Statement here. [SOURCE N]"
"""

def format_context(chunks: list) -> str:
    """Format retrieved chunks as SOURCE BLOCKS for the LLM"""
    blocks = []

    for i, chunk in enumerate(chunks, start=1):
        meta = chunk.metadata
        company = meta.get("company", "Unknown")
        year = meta.get("year", "?")
        page = meta.get("page_number", "?")

        header = f"[SOURCE {i}] {company} | {year} | Page {page}"
        score_line = f"Relevance: {chunk.rerank_score:.2f}"
        content = chunk.content[:500] + ("..." if len(chunk.content) > 500 else "")

        block = f"{header}\n{score_line}\n{content}"
        blocks.append(block)

    return "\n\n---\n\n".join(blocks)

# ============================================================================
# LLM GENERATION
# ============================================================================

def generate_answer(query: str, chunks: list) -> dict:
    """Call Groq LLM to generate answer based on retrieved chunks"""

    if not chunks:
        return {
            "answer": "The indexed documents do not contain sufficient information to answer this question.",
            "sources": [],
            "chunks_used": 0
        }

    # Format context
    context = format_context(chunks)

    user_message = f"""Please answer the following question using ONLY the source blocks provided.

## SOURCES
{context}

## QUESTION
{query}"""

    # Call Groq via OpenAI SDK
    try:
        client = OpenAI(api_key=GROQ_API_KEY, base_url=LLM_BASE_URL)
        
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0,  # Deterministic for factual answers
            max_tokens=1024
        )

        answer_text = response.choices[0].message.content

        return {
            "answer": answer_text,
            "sources": chunks,
            "chunks_used": len(chunks)
        }

    except Exception as e:
        return {
            "answer": f"Error generating answer: {e}",
            "sources": [],
            "chunks_used": 0
        }

# ============================================================================
# MAIN QUERY INTERFACE
# ============================================================================

def query_filingiq(question: str):
    """Full pipeline: retrieve relevant chunks → generate answer"""

    retriever = Retriever()

    if not retriever.collection:
        print("❌ No database found. Run ingest.py first.")
        return

    # Retrieve
    chunks = retriever.retrieve(question, top_k=TOP_K_RERANK)

    # Generate
    result = generate_answer(question, chunks)

    # Display
    print("\n" + "="*60)
    print("📋 ANSWER")
    print("="*60)
    print(result["answer"])

    if result["sources"]:
        print("\n" + "="*60)
        print("📚 SOURCES USED")
        print("="*60)
        for i, chunk in enumerate(result["sources"], start=1):
            meta = chunk.metadata
            print(f"\n[SOURCE {i}]")
            print(f"  Company: {meta.get('company', '?')}")
            print(f"  Year: {meta.get('year', '?')}")
            print(f"  Page: {meta.get('page_number', '?')}")
            print(f"  Relevance: {chunk.rerank_score:.2f}")

    print("\n" + "="*60)

# ============================================================================
# INTERACTIVE MODE
# ============================================================================

if __name__ == "__main__":
    print("="*60)
    print("FilingIQ RETRIEVAL INTERFACE")
    print("="*60)
    print("Type 'quit' to exit\n")

    while True:
        question = input("❓ Ask a question: ").strip()

        if question.lower() == 'quit':
            print("Goodbye!")
            break

        if not question:
            print("Please enter a question.\n")
            continue

        query_filingiq(question)