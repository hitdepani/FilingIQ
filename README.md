# FilingIQ

FilingIQ is an AI-powered retrieval-augmented generation (RAG) assistant for exploring Indian company filings, annual reports, and regulatory documents with natural-language search and source-backed answers.

Built to make financial and compliance research faster, FilingIQ combines semantic search, citation-aware retrieval, and a lightweight web interface into a single, deployable experience.

## 1. Project Title & Description

FilingIQ is a modern RAG application designed for querying structured and unstructured filings data from companies like Reliance, TCS, and Infosys, as well as SEBI regulations.

It helps users ask complex questions in plain English and receive grounded responses with evidence from the indexed source documents.

## 2. Features

- 2,735 indexed document chunks
- Real-time RAG search over uploaded and indexed filings
- Source citations for every generated answer
- Clean web UI for fast interaction
- Docker deployment ready for local and cloud use

## 3. Tech Stack

- Backend: FastAPI
- Vector database: ChromaDB
- Embeddings: Sentence Transformers
- LLM: Groq API
- Frontend: Vanilla HTML, CSS, and JavaScript

## 4. Quick Start

### Prerequisites

- Python 3.12+
- Docker

### Setup

```bash
git clone https://github.com/your-github-username/filingiq.git
cd filingiq
```

Create a `.env` file in the project root with your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### Run with Docker

```bash
docker run -p 8000:8000 -p 3000:3000 -e GROQ_API_KEY=your_key filingiq:latest
```

Open the app at:

- http://localhost:3000

## 5. Local Development

### Manual setup without Docker

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Run the API:

```bash
uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

Serve the frontend:

```bash
python -m http.server 3000 --directory frontend
```

API docs will be available at:

- http://localhost:8000/docs

## 6. Project Structure

- src/api.py — FastAPI application and API routes
- src/ingest.py — Document ingestion, chunking, and indexing pipeline
- src/retrieve.py — Retrieval and ranking logic for RAG
- src/verify_env.py — Environment validation helper
- frontend/index.html — Main web interface
- db/ — ChromaDB vector store and local data files
- .github/workflows/ — CI/CD workflow configuration
- Dockerfile — Container build definition
- docker-compose.yml — Container orchestration config
- requirements.txt — Python dependencies
- config.py — Project configuration settings

## 7. Performance

- 2,735 chunks indexed
- Query response time of approximately 2–3 seconds
- Content coverage includes Reliance, TCS, Infosys, and SEBI regulations

## 8. Future Roadmap

- User authentication and role-based access
- Multi-turn conversational follow-ups
- Export results to PDF or DOCX
- Advanced filtering by company, year, and document type
- Analytics dashboard for usage and retrieval insights

## 9. API Endpoints

- POST /chat — Main chat endpoint for natural-language Q&A
- POST /query — Debug endpoint with similarity scores and retrieval details
- GET /health — Health check endpoint
- GET /docs — Swagger UI for interactive API exploration

## 10. Contributing

To add new documents:

1. Place your PDFs in the data/raw directory.
2. Run the ingestion pipeline:

```bash
python src/ingest.py
```

This will process the new documents and update the vector store for retrieval.

## 11. License & Author

- License: MIT
- Author: Hit Depani
- GitHub: https://github.com/hitdepani
- Linkedin: https://www.linkedin.com/in/hit-depani-3b0698367/
