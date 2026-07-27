import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from pipeline.agent import Agent
from .config import ChannelConfig

log = logging.getLogger("slack_bot")


class SlackBot:
    def __init__(self, config: ChannelConfig | None = None):
        self.cfg = config or ChannelConfig.from_env()
        self.agent = Agent()

        self.app = App(
            token=self.cfg.slack_bot_token,
            signing_secret=self.cfg.slack_signing_secret,
        )
        self._register_commands()

    def _register_commands(self):
        @self.app.command("/ask")
        def ask_command(ack, respond, command):
            ack()
            question = command.get("text", "").strip()
            if not question:
                respond("Por favor escribe una pregunta. Ej: `/ask ¿Cuántos días tengo para solicitar reembolso?`")
                return

            respond("Buscando en los documentos de AprendeYa...")
            result = self.agent.ask(question)

            respuesta = result.get("respuesta", "")
            fuentes = result.get("fuentes", [])

            text = f"*Pregunta:* {question}\n\n{respuesta}"

            if fuentes:
                text += "\n\n*Fuentes:*"
                for f in fuentes:
                    label = f.get("titulo", "")
                    if f.get("seccion"):
                        label += f" / {f['seccion']}"
                    text += f"\n• {label}"

            if len(text) > 3000:
                text = text[:3000] + "\n\n*(respuesta truncada, consulta el chat web para el texto completo)*"

            respond(text)

        @self.app.event("app_mention")
        def handle_mention(event, say):
            text = event.get("text", "").strip()
            question = text.split(">", 1)[-1].strip() if ">" in text else text
            if not question:
                say("¿En qué puedo ayudarte?")
                return

            say("Buscando en los documentos de AprendeYa...")
            result = self.agent.ask(question)
            respuesta = result.get("respuesta", "")
            say(f"*Pregunta:* {question}\n\n{respuesta}")

        @self.app.event("message")
        def handle_dm(event, say):
            if event.get("channel_type") != "im":
                return
            text = event.get("text", "").strip()
            if not text or text.startswith("/"):
                return
            say("Buscando en los documentos de AprendeYa...")
            result = self.agent.ask(text)
            say(result.get("respuesta", ""))

    def start(self):
        if self.cfg.slack_socket_mode and self.cfg.slack_app_token:
            handler = SocketModeHandler(self.app, self.cfg.slack_app_token)
            log.info("Slack Bot iniciado en Socket Mode")
            handler.start()
        else:
            log.info("Slack Bot iniciando en modo HTTP (usa ngrok para desarrollo)")
            self.app.start(port=3000)
