FROM python:3.12-slim AS builder

WORKDIR /build
RUN pip install --no-cache-dir sentence-transformers>=3.0.0
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')"

FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /root/.cache /root/.cache

COPY scripts/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scripts/ ./scripts/
COPY docs-management/ ./docs-management/
COPY raw/ ./raw/

# Build ChromaDB index during Docker build (avoids tracking UUID artifacts in git)
RUN python scripts/ingest.py

ENV PYTHONPATH=/app/scripts
ENV GROQ_API_KEY=""
ENV OCI_VAULT_SECRET_ID=""
ENV OCI_OBJECT_STORAGE_BUCKET=""
ENV OCI_OBJECT_STORAGE_NAMESPACE=""

EXPOSE 8000

CMD ["python", "scripts/api.py"]
