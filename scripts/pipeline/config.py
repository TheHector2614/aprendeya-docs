from pathlib import Path


class Config:
    ROOT = Path(__file__).resolve().parent.parent.parent
    INVENTARIO = ROOT / "docs-management" / "inventario.yaml"
    RAW_DIR = ROOT / "raw"
    INDEX_DIR = ROOT / "index" / "chroma"
    EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
    COLLECTION_NAME = "aprendeya-docs"

    CHUNK_STRATEGY = "structural"
    CHUNK_SIZE = 300
    CHUNK_OVERLAP = 50

    OCR_FALLBACK = True

    GENERATION_MODEL = "llama-3.3-70b-versatile"
    CONFIDENCE_THRESHOLD = 0.3
