FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --retries 5 --default-timeout=1000 -r requirements.txt || \
    pip install --no-cache-dir --retries 5 --default-timeout=1000 -r requirements.txt

COPY config.py .
COPY src/ ./src/
COPY db/ ./db/
COPY frontend/ ./frontend/

EXPOSE 8000 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["sh", "-c", "python -m http.server 3000 --directory frontend & python -m uvicorn src.api:app --host 0.0.0.0 --port 8000"]