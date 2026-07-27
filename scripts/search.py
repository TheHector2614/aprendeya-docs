"""
Búsqueda semántica en los documentos indexados de AprendeYa.

Uso:
  python scripts/search.py "¿cuál es la política de reembolso?"
  python scripts/search.py "becas disponibles" --top-k 10
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pipeline import Config, Embedder, Indexer


def main():
    parser = argparse.ArgumentParser(description="Búsqueda semántica — AprendeYa")
    parser.add_argument("query", type=str, help="Texto a buscar")
    parser.add_argument("--top-k", type=int, default=5, help="Número de resultados")
    args = parser.parse_args()

    cfg = Config()
    embedder = Embedder(model_name=cfg.EMBEDDING_MODEL)
    indexer = Indexer(
        persist_dir=str(cfg.INDEX_DIR),
        collection_name=cfg.COLLECTION_NAME,
    )

    print(f"Buscando: \"{args.query}\"\n")

    query_embedding = embedder.embed([args.query])[0]
    results = indexer.search(query_embedding, top_k=args.top_k)

    if not results:
        print("Sin resultados.")
        return

    for i, r in enumerate(results, 1):
        print(f"{'='*60}")
        print(f"{i}. [{r['categoria']}] {r['documento']}")
        print(f"   Distancia: {r['distancia']}")
        print(f"   ID: {r['id']}")
        print(f"   {r['contenido']}")

    print(f"\n{'='*60}")
    print(f"{len(results)} resultado(s) encontrado(s).")


if __name__ == "__main__":
    main()
