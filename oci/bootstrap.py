"""
OCI Bootstrap — Sincroniza documentos y reconstruye el índice en OCI.

Pasos:
  1. Descarga documentos desde OCI Object Storage si existen.
  2. Reconstruye el índice ChromaDB.
  3. Verifica que el agente responde.

Uso (en el Container Instance):
  python oci/bootstrap.py

Variables de entorno requeridas:
  OCI_OBJECT_STORAGE_BUCKET  — nombre del bucket
  OCI_OBJECT_STORAGE_NAMESPACE — namespace del bucket
  GROQ_API_KEY               — llave de Groq
"""

import os
import sys
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("oci-bootstrap")

OCI_BUCKET = os.getenv("OCI_OBJECT_STORAGE_BUCKET", "")
OCI_NS = os.getenv("OCI_OBJECT_STORAGE_NAMESPACE", "")
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "raw"
INDEX_DIR = PROJECT_ROOT / "index" / "chroma"


def download_docs_from_object_storage():
    if not OCI_BUCKET or not OCI_NS:
        log.info("OCI Object Storage no configurado, usando documentos locales")
        return

    try:
        import oci

        signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
        client = oci.object_storage.ObjectStorageClient(config={}, signer=signer)

        objects = client.list_objects(OCI_NS, OCI_BUCKET).data.objects
        for obj in objects:
            local_path = RAW_DIR / obj.name
            local_path.parent.mkdir(parents=True, exist_ok=True)
            obj_data = client.get_object(OCI_NS, OCI_BUCKET, obj.name)
            local_path.write_bytes(obj_data.data.content)
            log.info(f"  Descargado: {obj.name}")

        log.info(f"Documentos sincronizados desde OCI Object Storage")
    except Exception as e:
        log.warning(f"No se pudieron descargar documentos desde OCI: {e}")
        log.info("Usando documentos locales existentes")


def rebuild_index():
    log.info("Reconstruyendo índice ChromaDB...")
    sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
    from pipeline import Config, Extractor, Cleaner, Chunker, Embedder, Indexer
    from ingest import load_inventario, resolve_path

    cfg = Config()
    extractor = Extractor(ocr_fallback=cfg.OCR_FALLBACK)
    cleaner = Cleaner()
    chunker = Chunker(strategy=cfg.CHUNK_STRATEGY, size=cfg.CHUNK_SIZE, overlap=cfg.CHUNK_OVERLAP)
    embedder = Embedder(model_name=cfg.EMBEDDING_MODEL)
    indexer = Indexer(persist_dir=str(INDEX_DIR), collection_name=cfg.COLLECTION_NAME, reset=True)

    inventario = load_inventario(cfg.INVENTARIO)
    all_chunks = []

    for doc in inventario:
        doc_id = doc["id"]
        titulo = doc.get("titulo", doc_id)
        categoria = doc.get("categoria", "GENERAL")
        ruta = resolve_path(doc)

        if not ruta or not ruta.exists():
            log.info(f"  [omitido] {doc_id}")
            continue

        try:
            text = extractor.extract(ruta)
            text = cleaner.clean(text)
            chunks = chunker.chunk(text, doc_id, titulo, categoria)
            all_chunks.extend(chunks)
            log.info(f"  [ok] {doc_id} ({len(chunks)} chunks)")
        except Exception as e:
            log.info(f"  [error] {doc_id}: {e}")

    log.info(f"\nTotal chunks: {len(all_chunks)}")

    if all_chunks:
        texts = [c.text for c in all_chunks]
        embeddings = embedder.embed(texts)
        indexer.index(all_chunks, embeddings)
        log.info(f"Índice reconstruido: {indexer.count()} chunks")


def verify_agent():
    log.info("\nVerificando agente...")
    sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
    from pipeline.agent import Agent

    agent = Agent()
    test_questions = [
        "Que es el NPS y cual es la meta?",
        "Cual es el tope diario para gastos de alimentacion?",
    ]
    for q in test_questions:
        result = agent.ask(q)
        c = result.get("confianza", 0)
        r = result.get("respuesta", "")
        log.info(f"  [{c:.3f}] {q}")
        log.info(f"  -> {r[:120]}...")
    log.info("Verificación completada")


if __name__ == "__main__":
    download_docs_from_object_storage()
    rebuild_index()
    verify_agent()
