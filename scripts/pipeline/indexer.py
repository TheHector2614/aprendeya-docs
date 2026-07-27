import chromadb
from chromadb.errors import NotFoundError
from chromadb.config import Settings

from .chunker import Chunk


class Indexer:
    def __init__(self, persist_dir: str, collection_name: str, reset: bool = False):
        self.client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(anonymized_telemetry=False),
        )
        if reset:
            try:
                self.client.delete_collection(name=collection_name)
            except (ValueError, NotFoundError):
                pass
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def index(self, chunks: list[Chunk], embeddings: list[list[float]]):
        ids = [f"{c.doc_id}-chunk-{c.chunk_index:04d}" for c in chunks]
        metadatas = [
            {
                "doc_id": c.doc_id,
                "doc_title": c.doc_title,
                "categoria": c.categoria,
                "seccion": c.seccion or "",
                "chunk_index": c.chunk_index,
            }
            for c in chunks
        ]
        texts = [c.text for c in chunks]

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=texts,
        )

    PREVIEW_CHARS = 300

    def search(
        self, query_embedding: list[float], top_k: int = 5
    ) -> list[dict]:
        # Chroma devuelve error si n_results supera el tamaño de la colección.
        n_results = min(top_k, self.count())
        if n_results <= 0:
            return []

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
        )
        output = []
        for i in range(len(results["ids"][0])):
            # Un chunk indexado sin metadatos devuelve None, no un dict vacío.
            meta = results["metadatas"][0][i] or {}
            texto = results["documents"][0][i] or ""
            output.append({
                "id": results["ids"][0][i],
                "documento": meta.get("doc_title"),
                "categoria": meta.get("categoria"),
                "seccion": meta.get("seccion", ""),
                # Los puntos suspensivos solo se añaden si de verdad se recortó;
                # antes se anexaban siempre, incluso a fragmentos completos.
                "contenido": (
                    texto[: self.PREVIEW_CHARS] + "..."
                    if len(texto) > self.PREVIEW_CHARS
                    else texto
                ),
                "distancia": round(results["distances"][0][i], 4),
            })
        return output

    def count(self) -> int:
        return self.collection.count()
