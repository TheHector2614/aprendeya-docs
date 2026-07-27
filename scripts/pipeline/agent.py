"""
Agente RAG — AprendeYa
Recupera fragmentos relevantes del índice vectorial y construye
una respuesta estructurada basada en los documentos.

Para mejorar la generación, conectar con un LLM externo (OpenAI,
Ollama, HF Inference API) reemplazando _build_response().

Uso:
  from pipeline.agent import Agent
  agent = Agent()
  respuesta = agent.ask("¿cuál es la política de reembolso?")
"""

import logging
import warnings

from .config import Config
from .embedder import Embedder
from .indexer import Indexer

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("agent")
warnings.filterwarnings("ignore", category=UserWarning, module="huggingface_hub")


class Agent:
    def __init__(self):
        self.cfg = Config()
        self.embedder = Embedder(model_name=self.cfg.EMBEDDING_MODEL)
        self.indexer = Indexer(
            persist_dir=str(self.cfg.INDEX_DIR),
            collection_name=self.cfg.COLLECTION_NAME,
        )

    def ask(self, question: str, top_k: int = 3) -> dict:
        log.info(f"Pregunta: {question}")

        query_emb = self.embedder.embed([question])[0]
        results = self.indexer.search(query_emb, top_k=top_k)

        if not results:
            return {
                "pregunta": question,
                "respuesta": "No encontré información relevante en los documentos disponibles.",
                "fuentes": [],
            }

        chunk_ids = [r["id"] for r in results]
        fetched = self.indexer.collection.get(ids=chunk_ids, include=["documents", "metadatas"])

        chunk_map = {}
        if fetched and fetched.get("ids"):
            for i in range(len(fetched["ids"])):
                cid = fetched["ids"][i]
                chunk_map[cid] = fetched["documents"][i]

        # Construir fuentes y contenido ordenado por relevancia
        fuentes = []
        partes = []
        seen = set()

        for r in results:
            title = r["documento"]
            full_text = chunk_map.get(r["id"], r["contenido"])
            full_text = full_text.rstrip("...")
            if len(full_text) > 600:
                full_text = full_text[:600] + "..."

            if title not in seen:
                seen.add(title)
                fuentes.append({
                    "titulo": title,
                    "categoria": r["categoria"],
                    "relevancia": round(1 - r["distancia"], 4),
                })
                partes.append(f"[{title}]\n{full_text}")

        respuesta = (
            "Basado en los documentos de AprendeYa:\n\n"
            + "\n\n".join(partes)
            + "\n\nPuedes consultar el documento completo para mas detalles."
        )

        return {"pregunta": question, "respuesta": respuesta, "fuentes": fuentes}
