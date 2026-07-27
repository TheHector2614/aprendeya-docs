import json
import logging
import sys
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pipeline.agent import Agent
from .config import ChannelConfig

log = logging.getLogger("teams_bot")


class TeamsBot:
    def __init__(self, config: ChannelConfig | None = None):
        self.cfg = config or ChannelConfig.from_env()
        self.agent = Agent()
        self.client = httpx.Client(timeout=30)

    def enviar(self, pregunta: str) -> bool:
        webhook = self.cfg.teams_webhook_url
        if not webhook:
            log.error("TEAMS_WEBHOOK_URL no configurado")
            return False

        result = self.agent.ask(pregunta)
        respuesta = result.get("respuesta", "")
        fuentes = result.get("fuentes", [])

        sections = []
        if respuesta:
            sections.append({
                "text": respuesta[:4000],
            })

        if fuentes:
            facts = []
            for f in fuentes:
                label = f.get("titulo", "")
                if f.get("seccion"):
                    label += f" / {f['seccion']}"
                facts.append({"name": "Fuente", "value": label})
            sections.append({
                "title": "Fuentes consultadas",
                "facts": facts,
            })

        card = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "1F4E79",
            "title": f"Pregunta: {pregunta[:120]}",
            "sections": sections,
            "potentialAction": [
                {
                    "@type": "OpenUri",
                    "name": "Abrir Chat Web",
                    "targets": [
                        {"os": "default", "uri": "http://localhost:8000/chat"}
                    ],
                }
            ],
        }

        try:
            r = self.client.post(webhook, json=card)
            r.raise_for_status()
            log.info(f"Mensaje enviado a Teams: {pregunta[:50]}...")
            return True
        except Exception as e:
            log.error(f"Error al enviar a Teams: {e}")
            return False

    def close(self):
        self.client.close()
