import chromadb
from chromadb.config import Settings

from .chunker import Chunk


class Indexer:
    def __init__(self, persist_dir: str, collection_name: str):
        self.client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(anonymized_telemetry=False),
        )
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

    def search(
        self, query_embedding: list[float], top_k: int = 5
    ) -> list[dict]:
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )
        output = []
        for i in range(len(results["ids"][0])):
            output.append({
                "id": results["ids"][0][i],
                "documento": results["metadatas"][0][i].get("doc_title"),
                "categoria": results["metadatas"][0][i].get("categoria"),
                "contenido": results["documents"][0][i][:300] + "...",
                "distancia": round(results["distances"][0][i], 4),
            })
        return output

    def count(self) -> int:
        return self.collection.count()
