import os
import re
import logging
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from .config import Config

log = logging.getLogger("generator")

SYSTEM_PROMPT = (
    "Eres un asistente de AprendeYa que responde preguntas de colaboradores "
    "bas\u00e1ndote EXCLUSIVAMENTE en los fragmentos de documentos proporcionados.\n\n"
    "INSTRUCCIONES:\n"
    "- Responde solo con la informaci\u00f3n presente en los fragmentos.\n"
    "- Si los fragmentos NO contienen la respuesta, responde exactamente: "
    "No encontr\u00e9 esta informaci\u00f3n en los documentos disponibles.\n"
    "- No uses conocimiento externo ni inventes informaci\u00f3n.\n"
    "- Cita la fuente al final de cada afirmaci\u00f3n con el formato: "
    "(Fuente: T\u00edtulo del Documento / Secci\u00f3n)\n"
    "- Responde en el mismo idioma de la pregunta.\n"
    "- Si hay informaci\u00f3n contradictoria entre fragmentos, menci\u00f3nalo."
)


class Generator:
    def __init__(self, model_name: str | None = None):
        self.cfg = Config()
        self.model = model_name or self.cfg.GENERATION_MODEL
        self.client = None
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            from groq import Groq
            self.client = Groq(api_key=api_key)
            log.info(f"Generador listo: {self.model} (Groq)")
        else:
            log.warning("GROQ_API_KEY no configurada. Usando fallback por extracci\u00f3n.")

    def generate(self, question: str, context_parts: list[dict]) -> str:
        if self.client:
            return self._generar_con_groq(question, context_parts)
        return self._generar_extraccion(question, context_parts)

    def _generar_con_groq(self, question: str, context_parts: list[dict]) -> str:
        context_lines = []
        for i, cp in enumerate(context_parts, 1):
            label = cp["titulo"]
            if cp.get("seccion"):
                label += f" / {cp['seccion']}"
            context_lines.append(
                f"--- Fragmento {i} ---\n"
                f"Fuente: {label}\n"
                f"{cp['texto']}"
            )
        context_block = "\n\n".join(context_lines)

        user_prompt = (
            f"CONTEXTO:\n{context_block}\n\n"
            f"PREGUNTA: {question}\n\n"
            "RESPUESTA:"
        )

        try:
            chat = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.1,
                max_tokens=512,
                top_p=0.9,
            )
            respuesta = chat.choices[0].message.content.strip()
            log.info(f"Generaci\u00f3n Groq exitosa ({len(respuesta)} chars)")
            return respuesta
        except Exception as e:
            log.error(f"Error en Groq API: {e}")
            return self._generar_extraccion(question, context_parts)

    def _generar_extraccion(self, question: str, context_parts: list[dict]) -> str:
        lines = []
        for cp in context_parts:
            label = cp["titulo"]
            if cp.get("seccion"):
                label += f" / {cp['seccion']}"
            lines.append(f"{cp['texto']} (Fuente: {label})")
        return "\n\n".join(lines)

    def verificar_alucinacion(
        self, respuesta: str, context_parts: list[dict]
    ) -> bool:
        if not respuesta:
            return False
        if "no encontr" in respuesta.lower():
            return True
        texto_contexto = " ".join(
            cp["texto"].lower() for cp in context_parts
        )
        palabras_resp = set(re.findall(r"\w{4,}", respuesta.lower()))
        palabras_ctx = set(re.findall(r"\w{4,}", texto_contexto))
        overlap = palabras_resp & palabras_ctx
        ratio = len(overlap) / len(palabras_resp) if palabras_resp else 0
        return ratio >= 0.3
