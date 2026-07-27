import re
from dataclasses import dataclass


@dataclass
class Chunk:
    text: str
    doc_id: str
    doc_title: str
    categoria: str
    chunk_index: int
    seccion: str = ""


class Chunker:
    """
    Chunking con dos estrategias:
      - 'structural': divide por secciones/encabezados (markdown #, HTML h1-h6)
      - 'fixed':     divide por tamaño fijo con overlap (fallback)
    """

    def __init__(self, strategy: str = "structural", size: int = 300, overlap: int = 50):
        if strategy not in ("structural", "fixed"):
            raise ValueError(f"Estrategia no válida: {strategy}")
        self.strategy = strategy
        self.size = size
        self.overlap = overlap

    def chunk(
        self, text: str, doc_id: str, doc_title: str, categoria: str
    ) -> list[Chunk]:
        if self.strategy == "structural":
            return self._chunk_structural(text, doc_id, doc_title, categoria)
        return self._chunk_fixed(text, doc_id, doc_title, categoria)

    def _chunk_structural(
        self, text: str, doc_id: str, doc_title: str, categoria: str
    ) -> list[Chunk]:
        sections = self._split_by_headings(text)
        chunks = []
        global_index = 0
        for seccion, contenido in sections:
            if not contenido.strip():
                continue
            subchunks = self._chunk_fixed(
                contenido, doc_id, doc_title, categoria,
                section_name=seccion,
                start_index=global_index,
            )
            chunks.extend([c for c in subchunks if c.text.strip()])
            global_index += len(subchunks)
        return chunks

    def _split_by_headings(self, text: str) -> list[tuple[str, str]]:
        heading_pattern = re.compile(r"^(#{1,6}\s+|\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\s*\n[-=]+\s*$)", re.MULTILINE)
        lines = text.split("\n")
        sections = []
        current_title = "sin_seccion"
        current_lines = []

        for line in lines:
            stripped = line.strip()
            heading = self._is_heading(stripped)
            if heading:
                if current_lines:
                    sections.append((current_title, "\n".join(current_lines)))
                current_title = heading
                current_lines = []
            else:
                current_lines.append(line)

        if current_lines:
            sections.append((current_title, "\n".join(current_lines)))
        return sections

    def _is_heading(self, line: str) -> str | None:
        m = re.match(r"^(#{1,6})\s+(.+)$", line)
        if m:
            return m.group(2).strip()
        if "|" in line:
            return None
        if line and line.isupper() and len(line) > 3 and len(line) < 80:
            return line
        return None

    def _chunk_fixed(
        self, text: str, doc_id: str, doc_title: str, categoria: str,
        section_name: str = "",
        start_index: int = 0,
    ) -> list[Chunk]:
        paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
        if not paragraphs:
            return []

        chunks = []
        buffer = []
        buffer_len = 0

        for para in paragraphs:
            para_len = len(para.split())
            if buffer_len + para_len > self.size and buffer:
                chunks.append(self._make_chunk(
                    buffer, doc_id, doc_title, categoria, start_index + len(chunks), section_name,
                ))
                overlap_words = []
                overlap_len = 0
                for bw in reversed(buffer):
                    wc = len(bw.split())
                    if overlap_len + wc > self.overlap:
                        break
                    overlap_words.insert(0, bw)
                    overlap_len += wc
                buffer = overlap_words
                buffer_len = overlap_len
            buffer.append(para)
            buffer_len += para_len

        if buffer:
            chunks.append(self._make_chunk(
                buffer, doc_id, doc_title, categoria, start_index + len(chunks), section_name,
            ))
        return chunks

    def _make_chunk(
        self, buffer: list[str], doc_id: str, doc_title: str,
        categoria: str, index: int, seccion: str = "",
    ) -> Chunk:
        return Chunk(
            text="\n".join(buffer),
            doc_id=doc_id,
            doc_title=doc_title,
            categoria=categoria,
            chunk_index=index,
            seccion=seccion,
        )
