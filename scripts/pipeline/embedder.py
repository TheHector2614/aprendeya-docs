from sentence_transformers import SentenceTransformer


class Embedder:
    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(
        self, texts: list[str], show_progress: bool = False
    ) -> list[list[float]]:
        """Vectoriza los textos.

        `show_progress` está desactivado por defecto: la barra tiene sentido en
        la ingesta por lotes, pero en la API se dibujaba en cada pregunta y
        ensuciaba los logs del contenedor con secuencias de escape.
        """
        embeddings = self.model.encode(texts, show_progress_bar=show_progress)
        return [emb.tolist() for emb in embeddings]
