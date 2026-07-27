"""
Entry point — Slack Bot (Socket Mode / HTTP)
Uso:
    python scripts/run_slack.py

Requiere variables de entorno (ver .env.template):
    SLACK_BOT_TOKEN, SLACK_SIGNING_SECRET, SLACK_APP_TOKEN (Socket Mode)
"""
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s %(message)s",
)

from integrations.slack_app import SlackBot
from integrations.config import ChannelConfig

if __name__ == "__main__":
    cfg = ChannelConfig.from_env()
    bot = SlackBot(cfg)
    bot.start()
