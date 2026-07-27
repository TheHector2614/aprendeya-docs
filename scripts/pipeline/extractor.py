from pathlib import Path
from bs4 import BeautifulSoup
import markdown
from docx import Document
from openpyxl import load_workbook


class Extractor:
    def extract(self, path: Path) -> str:
        ext = path.suffix.lower()
        handler = {
            ".html": self._extract_html,
            ".htm": self._extract_html,
            ".md": self._extract_markdown,
            ".docx": self._extract_docx,
            ".xlsx": self._extract_xlsx,
            ".txt": self._extract_txt,
        }
        handler_fn = handler.get(ext)
        if not handler_fn:
            raise ValueError(f"Formato no soportado: {ext}")
        return handler_fn(path)

    def _extract_html(self, path: Path) -> str:
        soup = BeautifulSoup(path.read_text("utf-8"), "lxml")
        for tag in soup(["script", "style", "nav", "header", "footer"]):
            tag.decompose()
        text = soup.get_text(separator="\n")
        return "\n".join(
            line.strip() for line in text.splitlines() if line.strip()
        )

    def _extract_markdown(self, path: Path) -> str:
        html = markdown.markdown(path.read_text("utf-8"))
        return self._extract_html_from_string(html)

    def _extract_docx(self, path: Path) -> str:
        doc = Document(str(path))
        return "\n".join(
            p.text for p in doc.paragraphs if p.text.strip()
        )

    def _extract_xlsx(self, path: Path) -> str:
        wb = load_workbook(path, data_only=True)
        lines = []
        for sheet in wb.sheetnames:
            ws = wb[sheet]
            lines.append(f"\n--- {sheet} ---\n")
            for row in ws.iter_rows(values_only=True):
                row_text = " | ".join(
                    str(c) for c in row if c is not None
                )
                if row_text.strip():
                    lines.append(row_text)
        return "\n".join(lines)

    def _extract_txt(self, path: Path) -> str:
        return path.read_text("utf-8")

    def _extract_html_from_string(self, html: str) -> str:
        soup = BeautifulSoup(html, "lxml")
        return "\n".join(
            line.strip() for line in soup.get_text().splitlines() if line.strip()
        )
