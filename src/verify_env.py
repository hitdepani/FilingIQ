"""
FilingIQ Ingest - TEST VERSION (2 PDFs only)
Proves the pipeline works before scaling to all 11
"""

import os
import sys
from pathlib import Path
from dataclasses import dataclass
import fitz
from sentence_transformers import SentenceTransformer
import chromadb
import gc

sys.path.insert(0, '.')
from config import DATA_PATH, CHROMA_PATH, FILING_REGISTRY, EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP

@dataclass
class Chunk:
    content: str
    metadata: dict

def clean_text(text: str) -> str:
    import re
    text = re.sub(r'([A-Za-z])\s+(?=[A-Za-z])', r'\1', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def parse_pdf(pdf_path: str, company: str, year: str) -> list:
    chunks = []
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(min(10, len(doc))):  # Only first 10 pages
            page = doc[page_num]
            text = page.get_text()
            text = clean_text(text)
            
            if text:
                chunks.append(Chunk(
                    content=text,
                    metadata={
                        "source_file": Path(pdf_path).name,
                        "company": company,
                        "year": year,
                        "page_number": page_num + 1,
                    }
                ))
        doc.close()
    except Exception as e:
        print(f"Error: {e}")
    return chunks

def run_test_ingest():
    print("="*60)
    print("FilingIQ TEST INGEST (2 PDFs, 20 pages total)")
    print("="*60)

    all_chunks = []
    test_filings = FILING_REGISTRY[:2]  # Only first 2 PDFs

    print(f"\n📂 Loading test PDFs...")
    for filing in test_filings:
        pdf_path = os.path.join(DATA_PATH, filing["file"])
        if not os.path.exists(pdf_path):
            print(f"❌ {filing['file']} not found")
            continue

        print(f"📄 {filing['company']} ({filing['year']})")
        chunks = parse_pdf(pdf_path, filing["company"], filing["year"])
        all_chunks.extend(chunks)
        print(f"   ✓ {len(chunks)} chunks")

    print(f"\n📈 Total chunks: {len(all_chunks)}")

    # Embed in tiny batches
    print(f"📊 Embedding (batch_size=8)...")
    model = SentenceTransformer(EMBEDDING_MODEL)
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(name="filingiq")

    for i in range(0, len(all_chunks), 8):
        batch = all_chunks[i:i+8]
        texts = [c.content[:500] for c in batch]  # Truncate to 500 chars
        
        embeddings = model.encode(texts, normalize_embeddings=True)
        
        collection.add(
            ids=[f"test_{i}_{j}" for j in range(len(batch))],
            documents=texts,
            embeddings=embeddings.tolist(),
            metadatas=[c.metadata for c in batch]
        )
        
        del embeddings
        gc.collect()
        print(f"  ✓ Batch {i//8 + 1}")

    print("\n✅ TEST INGEST COMPLETE - Database ready at ./db")

if __name__ == "__main__":
    run_test_ingest()