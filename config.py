import os
from dotenv import load_dotenv

load_dotenv()

# LLM
GROQ_API_KEY    = os.getenv("GROQ_API_KEY")
LLM_MODEL       = "llama-3.3-70b-versatile"
LLM_BASE_URL    = "https://api.groq.com/openai/v1"

# Embeddings + Reranker (fully local)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
RERANKER_MODEL  = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# Chunking
CHUNK_SIZE      = 400
CHUNK_OVERLAP   = 50

# Retrieval
TOP_K_RETRIEVAL = 15
TOP_K_RERANK    = 3

# Paths
CHROMA_PATH     = "./db"
DATA_PATH       = "./data/raw"

# Filing registry
FILING_REGISTRY = [
    {"file": "reliance_annual_report_fy2024.pdf", "company": "Reliance Industries", "doc_type": "annual_report", "year": "FY2024"},
    {"file": "reliance_annual_report_fy2025.pdf", "company": "Reliance Industries", "doc_type": "annual_report", "year": "FY2025"},
    {"file": "reliance_annual_report_fy2026.pdf", "company": "Reliance Industries", "doc_type": "annual_report", "year": "FY2026"},
    {"file": "tcs_annual_report_fy2024.pdf",      "company": "TCS",                 "doc_type": "annual_report", "year": "FY2024"},
    {"file": "tcs_annual_report_fy2025.pdf",      "company": "TCS",                 "doc_type": "annual_report", "year": "FY2025"},
    {"file": "tcs_annual_report_fy2026.pdf",      "company": "TCS",                 "doc_type": "annual_report", "year": "FY2026"},
    {"file": "infosys_annual_report_fy2024.pdf",  "company": "Infosys",             "doc_type": "annual_report", "year": "FY2024"},
    {"file": "infosys_annual_report_fy2025.pdf",  "company": "Infosys",             "doc_type": "annual_report", "year": "FY2025"},
    {"file": "infosys_annual_report_fy2026.pdf",  "company": "Infosys",             "doc_type": "annual_report", "year": "FY2026"},
    {"file": "sebi_regulation_insider_trading_2015.pdf", "company": "SEBI", "doc_type": "regulation", "year": "2015"},
    {"file": "sebi_regulation_lodr_2015.pdf",            "company": "SEBI", "doc_type": "regulation", "year": "2015"},
]

# Validate on import
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")