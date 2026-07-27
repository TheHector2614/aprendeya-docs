"""
Ingesta documental — AprendeYa
Procesa los documentos listados en docs-management/inventario.yaml:
  1. Extrae texto plano según el formato
  2. Divide en chunks semánticos
  3. Genera embeddings (multilingual)
  4. Indexa en ChromaDB

Uso: python scripts/ingest.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import yaml
from pipeline import Config, Extractor, Chunker, Embedder, Indexer


def load_inventario(path: Path) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("documentos", [])


def resolve_path(doc: dict) -> Path | None:
    fuente: str = doc.get("fuente", "")
    formato: str = doc.get("formato", "HTML").lower()
    extensiones = {"html": ".html", "md": ".md", "docx": ".docx", "xlsx": ".xlsx", "pdf": ".pdf", "txt": ".txt"}

    if "Sitio web" in fuente:
        ruta = Config.RAW_DIR / "web" / f"{doc['id']}.html"
    elif "Repositorio" in fuente:
        md_path = fuente.split("—")[-1].strip() if "—" in fuente else ""
        ruta = Config.RAW_DIR / "github" / f"{doc['id']}.md"
    elif "Google Drive" in fuente:
        ruta = Config.RAW_DIR / "drive" / doc["categoria"].lower() / f"{doc['id']}.{formato}"
    elif "SharePoint" in fuente:
        ext = extensiones.get(formato, ".xlsx")
        ruta = Config.RAW_DIR / "sharepoint" / doc["categoria"].lower() / f"{doc['id']}{ext}"
    else:
        ext = extensiones.get(formato, ".txt")
        ruta = Config.RAW_DIR / "general" / f"{doc['id']}{ext}"

    if formato == "html" and ruta.suffix != ".html":
        ruta = ruta.with_suffix(".html")

    return ruta


def ensure_sample_docs():
    """Crea documentos HTML de muestra desde las páginas existentes en src/pages."""
    web_dir = Config.RAW_DIR / "web"
    web_dir.mkdir(parents=True, exist_ok=True)

    pages_dir = Config.ROOT / "src" / "pages"
    for html_file in pages_dir.glob("*.astro"):
        doc_id = {
            "index": None,
            "reglamento-estudiante": "ACA-001",
            "politica-reembolso": "ACA-002",
            "faq": "ACA-003",
            "guia-uso": "ACA-004",
            "programa-becas": "ACA-005",
        }.get(html_file.stem)
        if not doc_id:
            continue
        out = web_dir / f"{doc_id}.html"
        if not out.exists():
            content = html_file.read_text("utf-8")
            simple_html = f"<html><body><pre>{content}</pre></body></html>"
            out.write_text(simple_html, "utf-8")
            print(f"  [creado] {out.name}")


def main():
    cfg = Config()
    extractor = Extractor()
    chunker = Chunker(size=cfg.CHUNK_SIZE, overlap=cfg.CHUNK_OVERLAP)
    embedder = Embedder(model_name=cfg.EMBEDDING_MODEL)
    indexer = Indexer(
        persist_dir=str(cfg.INDEX_DIR),
        collection_name=cfg.COLLECTION_NAME,
    )

    print("=== INGESTA DOCUMENTAL — AprendeYa ===\n")

    inventario = load_inventario(cfg.INVENTARIO)
    print(f"Documentos en inventario: {len(inventario)}")

    ensure_sample_docs()

    all_chunks = []
    for doc in inventario:
        doc_id = doc["id"]
        titulo = doc.get("titulo", doc_id)
        categoria = doc.get("categoria", "GENERAL")
        formato = doc.get("formato", "HTML")

        ruta = resolve_path(doc)
        if not ruta or not ruta.exists():
            print(f"  [omitido] {doc_id} — {titulo} (archivo no encontrado: {ruta})")
            continue

        try:
            text = extractor.extract(ruta)
            chunks = chunker.chunk(text, doc_id, titulo, categoria)
            all_chunks.extend(chunks)
            print(f"  [ok] {doc_id} — {titulo} ({len(chunks)} chunks)")
        except Exception as e:
            print(f"  [error] {doc_id} — {titulo}: {e}")

    print(f"\nTotal chunks generados: {len(all_chunks)}")

    if not all_chunks:
        print("No hay chunks para indexar.")
        return

    texts = [c.text for c in all_chunks]
    print("Generando embeddings...")
    embeddings = embedder.embed(texts)

    print("Indexando en ChromaDB...")
    indexer.index(all_chunks, embeddings)

    print(f"\n=== INGESTA COMPLETADA ===")
    print(f"Chunks indexados: {indexer.count()}")
    print(f"Colección: {cfg.COLLECTION_NAME}")
    print(f"Índice persistido en: {cfg.INDEX_DIR}")


if __name__ == "__main__":
    main()
