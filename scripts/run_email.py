"""
Entry point — Email Bot (prueba manual)
Uso:
    python scripts/run_email.py "¿Cuántos días tengo para solicitar reembolso?"

Requiere variables de entorno (ver .env.template):
    SMTP_HOST, SMTP_USER, SMTP_PASSWORD, EMAIL_FROM, EMAIL_TO
"""
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s %(message)s",
)

from integrations.email_bot import EmailBot
from integrations.config import ChannelConfig

if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    if not question:
        question = input("Pregunta: ")

    cfg = ChannelConfig.from_env()
    bot = EmailBot(cfg)
    bot.responder_y_imprimir(question)
