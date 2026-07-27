FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV HF_HOME=/home/app/.cache/huggingface
RUN useradd --create-home --uid 10001 app

COPY scripts/requirements.txt /tmp/requirements.txt

# CPU-only torch (evita descargar ~4GB de CUDA)
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu \
    "torch>=2.0.0" --force-reinstall

RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Precargar modelo de embeddings en el build
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')"

COPY --chown=app:app scripts/ ./scripts/
COPY --chown=app:app docs-management/ ./docs-management/
COPY --chown=app:app raw/ ./raw/

RUN mkdir -p /app/index && chown -R app:app /app/index

USER app

RUN python scripts/ingest.py

ENV PYTHONPATH=/app/scripts
ENV PYTHONUNBUFFERED=1
ENV GROQ_API_KEY=""
ENV OCI_VAULT_SECRET_ID=""
ENV OCI_OBJECT_STORAGE_BUCKET=""
ENV OCI_OBJECT_STORAGE_NAMESPACE=""

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=90s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=4).status == 200 else 1)"

CMD ["python", "scripts/api.py"]
