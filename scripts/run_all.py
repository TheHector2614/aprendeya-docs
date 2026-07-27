"""
Lanza todos los canales simultáneamente:
  - API REST (FastAPI) en puerto 8000
  - Slack Bot (Socket Mode)
  - Teams Bot (webhook inline)
  - Email Bot (bajo demanda)

Uso:
    python scripts/run_all.py
"""
import asyncio
import logging
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s %(message)s",
)
log = logging.getLogger("run_all")


def start_api():
    import uvicorn
    from api import app
    log.info("API REST en http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="warning")


def start_slack():
    from integrations.slack_app import SlackBot
    from integrations.config import ChannelConfig
    cfg = ChannelConfig.from_env()
    if cfg.slack_bot_token:
        bot = SlackBot(cfg)
        log.info("Slack Bot iniciado")
        bot.start()
    else:
        log.info("Slack no configurado (SLACK_BOT_TOKEN vacío)")


async def main():
    threads = []
    for fn in [start_api, start_slack]:
        t = threading.Thread(target=fn, daemon=True)
        t.start()
        threads.append(t)

    log.info("Todos los servicios iniciados. Presiona Ctrl+C para detener.")
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        log.info("Deteniendo servicios...")


if __name__ == "__main__":
    asyncio.run(main())
