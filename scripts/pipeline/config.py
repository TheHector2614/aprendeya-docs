from pathlib import Path


class Config:
    ROOT = Path(__file__).resolve().parent.parent.parent
    INVENTARIO = ROOT / "docs-management" / "inventario.yaml"
    RAW_DIR = ROOT / "raw"
    INDEX_DIR = ROOT / "index" / "chroma"
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 100
    EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
    COLLECTION_NAME = "aprendeya-docs"
