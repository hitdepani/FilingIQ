<div align="center">

<!-- Animated Banner -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:6366f1,50:8b5cf6,100:ec4899&height=200&section=header&text=FilingIQ&fontSize=80&fontAlignY=35&animation=fadeIn&fontColor=ffffff&desc=AI-Powered%20RAG%20for%20Indian%20Company%20Filings&descAlignY=55&descSize=22&descColor=e0e7ff" width="100%"/>

<!-- Animated Typing SVG -->
<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&duration=3000&pause=1000&color=818CF8&center=true&vCenter=true&multiline=true&width=700&height=80&lines=Ask+any+question+about+company+filings+%F0%9F%93%84;Get+AI-powered+answers+with+source+citations+%F0%9F%A4%96;Semantic+search+over+2%2C735+indexed+chunks+%F0%9F%94%8D" alt="Typing SVG" />
</a>

<br/>

<!-- Core Badges Row -->
<p>
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-0.111-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/ChromaDB-1.5.9-FF6B6B?style=for-the-badge&logo=databricks&logoColor=white"/>
  <img src="https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-F97316?style=for-the-badge&logo=meta&logoColor=white"/>
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
</p>

<!-- Status Badges -->
<p>
  <img src="https://img.shields.io/badge/License-MIT-22C55E?style=flat-square&logo=opensourceinitiative&logoColor=white"/>
  <img src="https://img.shields.io/badge/Status-Production%20Ready-22C55E?style=flat-square&logo=checkmarx&logoColor=white"/>
  <img src="https://img.shields.io/badge/Chunks%20Indexed-2%2C735-8B5CF6?style=flat-square&logo=databricks&logoColor=white"/>
  <img src="https://img.shields.io/badge/Response%20Time-2--3s-EC4899?style=flat-square&logo=speedtest&logoColor=white"/>
  <img src="https://img.shields.io/badge/Companies-Reliance%20%7C%20TCS%20%7C%20Infosys%20%7C%20SEBI-6366F1?style=flat-square&logo=homeassistant&logoColor=white"/>
</p>

</div>

---

## 🌟 What is FilingIQ?

<div align="center">

```
╔══════════════════════════════════════════════════════════════════╗
║  📄  Ask ANY question in plain English about Indian company      ║
║       filings, annual reports & SEBI regulations                 ║
║                                                                  ║
║  🔍  Get back a precise, cited answer sourced directly from       ║
║       2,735 indexed document chunks — no hallucinations          ║
║                                                                  ║
║  ⚡  Powered by Hybrid RAG: BM25 + Vector Search + Cross-Encoder ║
╚══════════════════════════════════════════════════════════════════╝
```

</div>

**FilingIQ** is a production-grade **Retrieval-Augmented Generation (RAG)** system built to make financial and compliance research **10× faster**. It combines semantic vector search, BM25 keyword retrieval, and a cross-encoder reranker — then feeds the best evidence to **LLaMA 3.3 70B** running on **Groq's ultra-fast inference** to produce grounded, citation-backed answers.

---

## ✨ Feature Highlights

<table>
<tr>
<td width="50%">

### 🔮 AI Intelligence
- 🧠 **LLaMA 3.3 70B** via Groq API — state-of-the-art LLM
- 🔍 **Hybrid Retrieval** — BM25 + dense vector search fusion
- 📐 **Cross-Encoder Reranking** — ms-marco MiniLM for precision
- 🎯 **Citation-Aware** — every fact is traceable to a source page
- 🚫 **Zero Hallucination** — strict context-grounded generation

</td>
<td width="50%">

### ⚙️ Engineering
- ⚡ **Sub-3s responses** end-to-end including LLM generation
- 🐳 **Docker-ready** — one command to deploy anywhere
- 📦 **2,735 chunks** pre-indexed and ready to query
- 🛡️ **Health check endpoint** with automatic recovery
- 🌐 **CORS-enabled FastAPI** — works with any frontend

</td>
</tr>
<tr>
<td width="50%">

### 📚 Data Coverage
- 📊 **Reliance Industries** — FY2024, FY2025, FY2026
- 💻 **TCS** — FY2024, FY2025, FY2026
- 🟢 **Infosys** — FY2024, FY2025, FY2026
- ⚖️ **SEBI Regulations** — LODR 2015 & Insider Trading 2015

</td>
<td width="50%">

### 🎨 Developer Experience
- 📖 **Interactive Swagger UI** at `/docs`
- 🧪 **Dual API modes** — debug `/query` + clean `/chat`
- 🔧 **Memory-optimized ingest** — batch embedding pipeline
- 📝 **Structured logging** — full observability
- 🔄 **Easy to extend** — add any PDF in minutes

</td>
</tr>
</table>

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          FilingIQ RAG Architecture                           │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌──────────┐     HTTP/REST      ┌─────────────────────────────────────────┐
  │          │ ─────────────────► │             FastAPI Backend              │
  │  Browser │                   │          (src/api.py · Port 8000)        │
  │ Frontend │ ◄───────────────── │   /chat  ·  /query  ·  /health  ·  /    │
  │  :3000   │   JSON Response    └──────────────────┬──────────────────────┘
  └──────────┘                                       │
                                                     ▼
                              ┌──────────────────────────────────────┐
                              │          Retriever Pipeline           │
                              │           (src/retrieve.py)          │
                              │                                      │
                              │  ┌─────────────┐  ┌──────────────┐  │
                              │  │  BM25 Index │  │  ChromaDB    │  │
                              │  │  (keyword)  │  │ (vector DB)  │  │
                              │  └──────┬──────┘  └──────┬───────┘  │
                              │         └────────┬────────┘          │
                              │                  │ 15 candidates     │
                              │                  ▼                   │
                              │  ┌───────────────────────────────┐  │
                              │  │  Cross-Encoder Reranker        │  │
                              │  │  ms-marco-MiniLM-L-6-v2       │  │
                              │  │  → Top 3 most relevant chunks  │  │
                              │  └───────────────┬───────────────┘  │
                              └──────────────────┼───────────────────┘
                                                 │
                                                 ▼
                              ┌──────────────────────────────────────┐
                              │           Groq LLM API               │
                              │    LLaMA-3.3-70B-Versatile           │
                              │  Temperature=0 · Max tokens=1024     │
                              │  → Citation-grounded answer          │
                              └──────────────────────────────────────┘

  ═══════════════════════ INGESTION PIPELINE (Offline) ═══════════════════════

  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌────────────┐
  │  PDF Files   │───►│  PyMuPDF     │───►│  Text        │───►│  all-      │
  │  (data/raw/) │    │  Parser      │    │  Chunker     │    │  MiniLM-   │
  │              │    │  • Skip OCR  │    │  400 tok     │    │  L6-v2     │
  │  11 docs     │    │  • Strip H/F │    │  50 overlap  │    │  Embedder  │
  └──────────────┘    └──────────────┘    └──────────────┘    └─────┬──────┘
                                                                     │
                                                                     ▼
                                                          ┌──────────────────┐
                                                          │   ChromaDB       │
                                                          │   Persistent     │
                                                          │   Vector Store   │
                                                          │   (./db/)        │
                                                          │   2,735 chunks   │
                                                          └──────────────────┘
```

---

## 🔬 RAG Pipeline Deep Dive

```mermaid
flowchart TD
    A[👤 User Query] --> B[Query Embedding\nall-MiniLM-L6-v2]
    A --> C[BM25 Tokenization\nrank-bm25]
    
    B --> D[ChromaDB\nVector Search\nTop-15 candidates]
    C --> E[BM25 Keyword\nSearch]
    
    D --> F{Fusion &\nDeduplication}
    E --> F
    
    F --> G[Cross-Encoder\nReranker\nms-marco-MiniLM-L-6-v2]
    G --> H[Top-3\nReranked Chunks]
    
    H --> I[Prompt Builder\nSOURCE BLOCKS\nformat]
    I --> J[Groq API\nLLaMA 3.3 70B]
    J --> K[✅ Cited Answer\nwith Source References]
    
    style A fill:#6366f1,color:#fff
    style K fill:#22c55e,color:#fff
    style J fill:#f97316,color:#fff
    style G fill:#8b5cf6,color:#fff
    style D fill:#3b82f6,color:#fff
```

---

## 🧰 Tech Stack

<div align="center">

| Layer | Technology | Version | Purpose |
|:------|:-----------|:--------|:--------|
| 🌐 **API Framework** | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white) | `0.111.0` | REST endpoints, Pydantic validation, Swagger UI |
| 🗄️ **Vector Database** | ![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6B6B?style=flat&logo=databricks&logoColor=white) | `1.5.9` | Persistent local vector store with cosine similarity |
| 🧬 **Embeddings** | ![HuggingFace](https://img.shields.io/badge/Sentence--Transformers-FFD21E?style=flat&logo=huggingface&logoColor=black) | `5.5.1` | `all-MiniLM-L6-v2` — 384-dim dense embeddings |
| 📊 **Reranker** | ![HuggingFace](https://img.shields.io/badge/CrossEncoder-FFD21E?style=flat&logo=huggingface&logoColor=black) | — | `ms-marco-MiniLM-L-6-v2` cross-encoder |
| 🔠 **Keyword Search** | `rank-bm25` | `0.2.2` | BM25Okapi sparse retrieval |
| 🤖 **LLM** | ![Meta](https://img.shields.io/badge/LLaMA%203.3%2070B-0467DF?style=flat&logo=meta&logoColor=white) | 70B | Instruction-tuned, 128k context |
| ⚡ **LLM Inference** | ![Groq](https://img.shields.io/badge/Groq%20API-F97316?style=flat&logo=lightning&logoColor=white) | — | Ultra-fast LPU inference (300+ tok/s) |
| 📄 **PDF Parsing** | `PyMuPDF (fitz)` | `1.24.1` | Block-level text extraction, header/footer removal |
| 🐍 **Runtime** | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) | `3.12+` | Async-ready, type-safe |
| 🐳 **Containerization** | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white) | Latest | Multi-service single container |
| 🌐 **Frontend** | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white) ![JS](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black) | Vanilla | Zero-dependency chat UI |
| 🔧 **Server** | ![Uvicorn](https://img.shields.io/badge/Uvicorn-499848?style=flat&logo=gunicorn&logoColor=white) | `0.24.0` | ASGI production server |

</div>

---

## 📁 Project Structure

```
filingiq/
│
├── 📂 src/                         # Core application logic
│   ├── 🐍 api.py                   # FastAPI app · 4 endpoints · CORS · startup init
│   ├── 🔄 ingest.py                # PDF → Chunks → Embeddings → ChromaDB pipeline
│   ├── 🔍 retrieve.py              # Hybrid retrieval · reranking · Groq LLM generation
│   └── ✅ verify_env.py            # Pre-flight environment validator
│
├── 📂 frontend/
│   └── 🌐 index.html               # Vanilla JS chat UI · Fetch API · source citations
│
├── 📂 db/                          # ChromaDB persistent vector store (2,735 chunks)
│
├── 📂 data/                        # (Not committed) Place raw PDFs here
│   └── raw/                        # 11 PDF filings go here for ingestion
│
├── 📂 .github/
│   └── workflows/                  # CI/CD pipeline configuration
│
├── 🐳 Dockerfile                   # Python 3.12-slim · dual-port · health check
├── 🐙 docker-compose.yml           # One-command orchestration
├── ⚙️  config.py                   # All tuneable parameters in one place
├── 📋 requirements.txt             # 9 pinned production dependencies
├── 🚫 .gitignore                   # Excludes venv, .env, raw PDFs
└── 📖 README.md                    # This file
```

---

## ⚡ Quick Start

### Option 1 — Docker (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/hitdepani/filingiq.git
cd filingiq

# 2. Create your environment file
echo "GROQ_API_KEY=your_groq_api_key_here" > .env

# 3. Run with a single command
docker run -p 8000:8000 -p 3000:3000 --env-file .env filingiq:latest
```

> 🌐 Open **http://localhost:3000** in your browser — that's it!

---

### Option 2 — Local Development

```bash
# 1. Clone & enter directory
git clone https://github.com/hitdepani/filingiq.git
cd filingiq

# 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your API key
echo "GROQ_API_KEY=your_groq_api_key_here" > .env

# 5. Start the API backend
uvicorn src.api:app --reload --host 0.0.0.0 --port 8000

# 6. Serve the frontend (new terminal)
python -m http.server 3000 --directory frontend
```

| Service | URL |
|:--------|:----|
| 💬 Chat UI | http://localhost:3000 |
| 📖 API Docs (Swagger) | http://localhost:8000/docs |
| ❤️ Health Check | http://localhost:8000/health |

---

## 📡 API Reference

<details>
<summary><b>🟢 GET /health — Service status & chunk count</b></summary>

```json
// Response 200 OK
{
  "status": "healthy",
  "chunks_indexed": 2735,
  "message": "FilingIQ API is running"
}
```
</details>

<details>
<summary><b>🔵 POST /chat — Frontend-optimized Q&A</b></summary>

```json
// Request
{ "question": "What was Reliance's revenue in FY2024?" }

// Response 200 OK
{
  "answer": "Reliance Industries reported a consolidated revenue of ₹9,01,378 crore in FY2024. [SOURCE 1]",
  "sources": [
    "Reliance Industries | FY2024 | Page 87",
    "Reliance Industries | FY2024 | Page 92"
  ]
}
```
</details>

<details>
<summary><b>🟣 POST /query — Debug mode with full relevance scores</b></summary>

```json
// Request
{ "question": "What are SEBI's insider trading disclosure requirements?" }

// Response 200 OK
{
  "answer": "SEBI's Prohibition of Insider Trading Regulations 2015 require... [SOURCE 1]",
  "sources": [
    {
      "id": "sebi_regulation_insider_trading_2015_p3_c0",
      "company": "SEBI",
      "year": "2015",
      "page": 3,
      "relevance": 0.94,
      "content": "Every insider shall maintain a structured digital database..."
    }
  ],
  "chunks_used": 3
}
```
</details>

---

## 🗄️ Data Ingestion Pipeline

To add new documents to the knowledge base:

```bash
# 1. Place your PDFs in the raw data directory
cp your_annual_report.pdf data/raw/

# 2. Register the file in config.py → FILING_REGISTRY list
# Example entry:
# {"file": "your_annual_report.pdf", "company": "YourCo", "doc_type": "annual_report", "year": "FY2025"}

# 3. Run the ingestion pipeline
python src/ingest.py
```

**What happens under the hood:**

```
PDF File
  ↓ detect_pdf_type()       → Skip scanned/OCR-only PDFs
  ↓ parse_pdf()             → PyMuPDF block extraction
  ↓ is_header_footer()      → Strip 8% top/bottom margin noise
  ↓ clean_text()            → Normalize whitespace, dashes, quotes
  ↓ chunk_document()        → 400-token chunks, 50-token overlap
  ↓ embed_and_store_batch() → Encode in batches of 16 (~100MB RAM)
  ↓ ChromaDB.add()          → Persistent vector storage
```

---

## 📊 Performance Metrics

<div align="center">

| Metric | Value |
|:-------|:------|
| 📦 Total document chunks indexed | **2,735** |
| 🏢 Companies covered | **4** (Reliance, TCS, Infosys, SEBI) |
| 📅 Years covered | **FY2024 · FY2025 · FY2026** |
| 📄 Total documents | **11 PDFs** |
| ⏱️ Average end-to-end query latency | **~2–3 seconds** |
| 🧩 Chunk size | **400 tokens** |
| 🔀 Chunk overlap | **50 tokens** |
| 🔍 Vector search candidates | **Top 15** |
| 🎯 Final chunks fed to LLM | **Top 3** (after reranking) |
| 💾 Embedding dimensions | **384** (all-MiniLM-L6-v2) |
| 🔢 LLM max output tokens | **1,024** |

</div>

---

## 🔧 Configuration Reference

All parameters live in [`config.py`](./config.py):

```python
# ── LLM ──────────────────────────────────────────────────────────
LLM_MODEL       = "llama-3.3-70b-versatile"   # Groq-hosted LLaMA 3.3
LLM_BASE_URL    = "https://api.groq.com/openai/v1"

# ── Embeddings & Reranker (100% local, no API needed) ────────────
EMBEDDING_MODEL = "all-MiniLM-L6-v2"          # 384-dim, fast & accurate
RERANKER_MODEL  = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# ── Chunking ──────────────────────────────────────────────────────
CHUNK_SIZE      = 400   # tokens (~1,600 chars)
CHUNK_OVERLAP   = 50    # tokens of context carry-over

# ── Retrieval ─────────────────────────────────────────────────────
TOP_K_RETRIEVAL = 15    # candidates from vector search
TOP_K_RERANK    = 3     # final chunks sent to LLM
```

---

## 🗺️ Roadmap

- [x] Hybrid BM25 + vector retrieval
- [x] Cross-encoder reranking
- [x] Citation-aware answer generation
- [x] Docker deployment
- [x] Swagger API documentation
- [ ] 🔐 User authentication & role-based access
- [ ] 💬 Multi-turn conversational follow-ups (chat memory)
- [ ] 📤 Export answers to PDF / DOCX
- [ ] 🔎 Advanced filters by company, year, document type
- [ ] 📈 Analytics dashboard — usage & retrieval insights
- [ ] 🌏 Support for BSE/NSE filing formats
- [ ] 🔄 Auto-ingest from SEBI EDGAR API

---

## 🤝 Contributing

Contributions are warmly welcome!

```bash
# Fork → Clone → Branch → Code → PR
git checkout -b feature/your-feature-name
git commit -m "feat: add amazing feature"
git push origin feature/your-feature-name
```

To add support for new document types, extend the `FILING_REGISTRY` in `config.py` and drop the PDFs into `data/raw/`.

---

## 📜 License

This project is licensed under the **MIT License** — use it, extend it, ship it.

---

<div align="center">

<!-- Footer Wave -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:ec4899,50:8b5cf6,100:6366f1&height=120&section=footer" width="100%"/>

**Built with ❤️ by [Hit Depani](https://github.com/hitdepani)**

[![GitHub](https://img.shields.io/badge/GitHub-hitdepani-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/hitdepani)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Hit%20Depani-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/hit-depani-3b0698367/)

<br/>

*"Making financial research smarter, faster, and verifiable — one filing at a time."*

<br/>

![Visitor Count](https://visitor-badge.laobi.icu/badge?page_id=hitdepani.filingiq&left_color=6366f1&right_color=ec4899)
⭐ **Star this repo if FilingIQ helped you!** ⭐

</div>
