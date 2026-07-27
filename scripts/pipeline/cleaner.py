import re


class Cleaner:
    PATRONES_PAGINA = [
        r"Página \d+ de \d+",
        r"Page \d+ of \d+",
        r"-\s+\d+\s+-",
        r"^\d+$",
    ]
    PATRONES_ENCABEZADO = [
        r"^Confidencial\b",
        r"^\b[A-Z][a-z]+ – [A-Z][a-z]+\b",
    ]

    def clean(self, text: str) -> str:
        text = self._remove_page_numbers(text)
        text = self._normalize_whitespace(text)
        return text.strip()

    def _remove_page_numbers(self, text: str) -> str:
        lines = text.split("\n")
        clean_lines = []
        for line in lines:
            stripped = line.strip()
            skip = False
            for patron in self.PATRONES_PAGINA:
                if re.match(patron, stripped):
                    skip = True
                    break
            for patron in self.PATRONES_ENCABEZADO:
                if re.match(patron, stripped, re.IGNORECASE):
                    skip = True
                    break
            if not skip:
                clean_lines.append(line)
        return "\n".join(clean_lines)

    def _normalize_whitespace(self, text: str) -> str:
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"[^\S\n]+", " ", text)
        return text
