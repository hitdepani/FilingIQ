"""
FilingIQ Ingest Pipeline (Memory-Optimized)
Load PDFs → Parse → Chunk → Embed (small batches) → Store in ChromaDB
"""

import os
import sys
from pathlib import Path
from dataclasses import dataclass
import fitz
import numpy as np
from sentence_transformers import SentenceTransformer
import chromadb
from tqdm import tqdm
import gc

sys.path.insert(0, '.')
from config import (
    DATA_PATH, CHROMA_PATH, FILING_REGISTRY,
    EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP
)

@dataclass
class Document:
    content: str
    metadata: dict

@dataclass
class Chunk:
    content: str
    metadata: dict
    token_estimate: int

def detect_pdf_type(pdf_path: str) -> str:
    try:
        doc = fitz.open(pdf_path)
        text_pages = sum(1 for page in doc if len(page.get_text().strip()) > 50)
        doc.close()
        return "text" if text_pages > 0 else "scanned"
    except:
        return "unknown"

def is_header_footer(y0: float, y1: float, page_height: float) -> bool:
    margin = page_height * 0.08
    return y0 < margin or y1 > (page_height - margin)

def clean_text(text: str) -> str:
    import re
    text = re.sub(r'([A-Za-z])\s+(?=[A-Za-z])', r'\1', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('"', '"').replace('"', '"')
    text = text.replace('–', '-').replace('—', '-')
    text = text.replace('\xad', '').replace('\f', '')
    return text.strip()

def parse_pdf(pdf_path: str, company: str, doc_type: str, year: str) -> list:
    if detect_pdf_type(pdf_path) == "scanned":
        print(f"⚠️  {Path(pdf_path).name} is scanned — skipping")
        return []

    documents = []
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc[page_num]
            blocks = page.get_text("blocks")
            page_text = []

            for block in blocks:
                x0, y0, x1, y1, text, block_type = block[:6]
                if is_header_footer(y0, y1, page.rect.height):
                    continue
                if block_type == 0:
                    cleaned = clean_text(text)
                    if cleaned:
                        page_text.append(cleaned)

            full_text = "\n".join(page_text)
            if full_text.strip():
                documents.append(Document(
                    content=full_text,
                    metadata={
                        "source_file": Path(pdf_path).name,
                        "company": company,
                        "doc_type": doc_type,
                        "year": year,
                        "page_number": page_num + 1,
                        "total_pages": len(doc),
                    }
                ))
        doc.close()
    except Exception as e:
        print(f"Error parsing {pdf_path}: {e}")

    return documents

def estimate_tokens(text: str) -> int:
    return len(text) // 4

def chunk_document(doc: Document) -> list:
    text = doc.content
    chunks = []
    chunk_id = 0
    char_size = CHUNK_SIZE * 4
    overlap_chars = CHUNK_OVERLAP * 4
    start_idx = 0

    while start_idx < len(text):
        end_idx = min(start_idx + char_size, len(text))

        if end_idx < len(text):
            for delim in ['. ', '.\n', '\n\n', '\n']:
                last_delim = text.rfind(delim, start_idx, end_idx)
                if last_delim > start_idx:
                    end_idx = last_delim + len(delim)
                    break

        chunk_text = text[start_idx:end_idx].strip()
        if chunk_text:
            chunks.append(Chunk(
                content=chunk_text,
                metadata={
                    **doc.metadata,
                    "chunk_id": f"{doc.metadata['source_file'].replace('.pdf', '')}_p{doc.metadata['page_number']}_c{chunk_id}",
                    "chunk_index": chunk_id,
                },
                token_estimate=estimate_tokens(chunk_text)
            ))
            chunk_id += 1

        start_idx = end_idx - overlap_chars
        if start_idx <= 0:
            break

    return chunks

def embed_and_store_batch(chunks: list, batch_size: int = 16):
    """
    Embed and store in smaller batches to save RAM.
    Batch size 16 = ~100MB RAM instead of all at once.
    """
    print(f"\n📊 Embedding {len(chunks)} chunks (batch_size={batch_size})...")

    model = SentenceTransformer(EMBEDDING_MODEL)
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(
        name="filingiq",
        metadata={"model": EMBEDDING_MODEL}
    )

    for i in tqdm(range(0, len(chunks), batch_size)):
        batch = chunks[i:i+batch_size]
        texts = [c.content for c in batch]

        # Embed just this batch
        embeddings = model.encode(texts, batch_size=8, normalize_embeddings=True)

        # Store immediately
        ids = [c.metadata["chunk_id"] for c in batch]
        documents = [c.content for c in batch]
        metadatas = [c.metadata for c in batch]

        collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings.tolist(),
            metadatas=metadatas
        )

        # Clear memory
        del embeddings
        gc.collect()

    print(f"✅ Stored {len(chunks)} chunks")

def run_ingest():
    print("=" * 60)
    print("FilingIQ INGEST PIPELINE (Memory-Optimized)")
    print("=" * 60)

    all_chunks = []

    print(f"\n📂 Loading PDFs from {DATA_PATH}...")
    for filing in FILING_REGISTRY:
        pdf_path = os.path.join(DATA_PATH, filing["file"])

        if not os.path.exists(pdf_path):
            print(f"❌ {pdf_path} not found")
            continue

        print(f"\n📄 {filing['company']} ({filing['year']})")

        documents = parse_pdf(pdf_path, filing["company"], filing["doc_type"], filing["year"])
        print(f"   ✓ {len(documents)} pages")

        for doc in documents:
            chunks = chunk_document(doc)
            all_chunks.extend(chunks)

    print(f"\n📈 Total chunks: {len(all_chunks)}")

    # Embed and store with small batch size
    embed_and_store_batch(all_chunks, batch_size=16)

    print("\n" + "=" * 60)
    print("✅ INGEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    run_ingest()