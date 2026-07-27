"""
Entry point — Teams Bot (envía a webhook)
Uso:
    python scripts/run_teams.py "¿Cuántos días tengo para solicitar reembolso?"

Requiere variables de entorno (ver .env.template):
    TEAMS_WEBHOOK_URL
"""
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s %(message)s",
)

from integrations.teams_bot import TeamsBot
from integrations.config import ChannelConfig

if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    if not question:
        question = input("Pregunta: ")

    cfg = ChannelConfig.from_env()
    bot = TeamsBot(cfg)
    ok = bot.enviar(question)
    bot.close()
    print(f"Enviado a Teams: {'Sí' if ok else 'No (revisa TEAMS_WEBHOOK_URL)'}")
