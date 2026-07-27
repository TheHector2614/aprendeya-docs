from dataclasses import dataclass


@dataclass
class Chunk:
    text: str
    doc_id: str
    doc_title: str
    categoria: str
    chunk_index: int


class Chunker:
    def __init__(self, size: int = 500, overlap: int = 100):
        self.size = size
        self.overlap = overlap

    def chunk(
        self, text: str, doc_id: str, doc_title: str, categoria: str
    ) -> list[Chunk]:
        paragraphs = text.split("\n")
        chunks = []
        buffer = []
        buffer_len = 0

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            words = para.split()
            para_len = len(words)

            if buffer_len + para_len > self.size and buffer:
                chunks.append(self._make_chunk(
                    buffer, doc_id, doc_title, categoria, len(chunks)
                ))
                overlap_words = []
                overlap_len = 0
                for bw in reversed(buffer):
                    if overlap_len + len(bw) > self.overlap:
                        break
                    overlap_words.insert(0, bw)
                    overlap_len += len(bw)
                buffer = overlap_words
                buffer_len = overlap_len

            buffer.append(para)
            buffer_len += para_len

        if buffer:
            chunks.append(self._make_chunk(
                buffer, doc_id, doc_title, categoria, len(chunks)
            ))

        return chunks

    def _make_chunk(
        self, buffer: list[str], doc_id: str, doc_title: str,
        categoria: str, index: int
    ) -> Chunk:
        return Chunk(
            text="\n".join(buffer),
            doc_id=doc_id,
            doc_title=doc_title,
            categoria=categoria,
            chunk_index=index,
        )
