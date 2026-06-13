# FilingIQ 📊

**Production-grade RAG system for Indian company filings**

Query annual reports from Reliance, TCS, Infosys and SEBI regulations using AI.

## Features

✅ **Vector Search** — Semantic search using all-MiniLM-L6-v2 embeddings  
✅ **Reranking** — Cross-encoder reranking for precision  
✅ **LLM Generation** — Groq LLM for natural language answers  
✅ **Citations** — Automatic source attribution  
✅ **REST API** — FastAPI backend  
✅ **Cloud Ready** — Docker + AWS deployment  

## Quick Start

### Local Development

```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/filingiq.git
cd filingiq

# Install dependencies
pip install -r requirements.txt

# Run API
python src/api.py

# Visit http://localhost:8000/docs
```

### Docker

```bash
# Build image
docker build -t filingiq .

# Run container
docker run -p 8000:8000 -e GROQ_API_KEY=your_key filingiq
```

### Docker Compose

```bash
docker-compose up -d
```

## API Usage

### Query Endpoint

**POST** `/query`

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What was Reliance revenue in FY2024?"
  }'
```

**Response:**
```json
{
  "answer": "Reliance's revenue in FY2024 was ₹3,06,848 Crore...",
  "sources": [
    {
      "company": "Reliance Industries",
      "year": "FY2024",
      "page": 3,
      "relevance": 1.57,
      "content": "..."
    }
  ],
  "chunks_used": 3
}
```

### Health Check

**GET** `/health`

```bash
curl http://localhost:8000/health
```

## Architecture
PDFs (11)

↓

Ingest (parse → chunk → embed)

↓

ChromaDB (2735 chunks)

↓

API (retrieve → rerank → generate)

↓

Response with citations

## Deployment

See [aws-deployment.md](./aws-deployment.md) for AWS EC2 deployment guide.

## Tech Stack

- **Backend**: FastAPI, Python 3.12
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Reranking**: cross-encoder (ms-marco-MiniLM-L-6-v2)
- **Vector Store**: ChromaDB
- **LLM**: Groq (llama-3.3-70b-versatile)
- **Container**: Docker
- **Cloud**: AWS EC2

## Configuration

Create `.env`:
GROQ_API_KEY=your_groq_api_key_here

## Project Structure
filing/

├── src/

│   ├── api.py           # FastAPI application

│   ├── ingest.py        # PDF indexing pipeline

│   ├── retrieve.py      # RAG retrieval logic

│   └── verify_env.py    # Environment checker

├── db/                  # ChromaDB vector store

├── data/raw/            # PDF documents

├── config.py            # Configuration

├── requirements.txt     # Dependencies

├── Dockerfile           # Docker image

├── docker-compose.yml   # Docker Compose

├── .github/workflows/   # CI/CD pipeline

└── README.md           # This file

## Performance

- **Chunks Indexed**: 2,735
- **Companies**: 3 (Reliance, TCS, Infosys)
- **Regulations**: SEBI (2015)
- **Query Time**: ~2-3 seconds
- **Accuracy**: High relevance for factual questions

## License

MIT

## Author

Built with ❤️ for learning RAG systems