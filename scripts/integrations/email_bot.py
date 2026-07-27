import logging
import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pipeline.agent import Agent
from .config import ChannelConfig

log = logging.getLogger("email_bot")


class EmailBot:
    def __init__(self, config: ChannelConfig | None = None):
        self.cfg = config or ChannelConfig.from_env()
        self.agent = Agent()

    def _formatear_fuentes(self, fuentes: list[dict]) -> str:
        if not fuentes:
            return ""
        lines = ["\n\nFuentes consultadas:"]
        for f in fuentes:
            label = f.get("titulo", "")
            if f.get("seccion"):
                label += f" / {f['seccion']}"
            lines.append(f"  - {label}")
        return "\n".join(lines)

    def responder(self, pregunta: str, to: str | None = None) -> bool:
        result = self.agent.ask(pregunta)
        respuesta = result.get("respuesta", "")
        fuentes = result.get("fuentes", [])

        cuerpo = (
            f"Pregunta: {pregunta}\n\n"
            f"{respuesta}"
            f"{self._formatear_fuentes(fuentes)}"
            f"\n\n---\nAprendeYa - Asistente Documental"
        )

        destinatario = to or self.cfg.email_to
        if not destinatario:
            log.error("EMAIL_TO no configurado")
            return False

        msg = MIMEMultipart()
        msg["From"] = self.cfg.email_from
        msg["To"] = destinatario
        msg["Subject"] = f"[AprendeYa] Respuesta: {pregunta[:60]}..."
        msg.attach(MIMEText(cuerpo, "plain", "utf-8"))

        try:
            with smtplib.SMTP(self.cfg.smtp_host, self.cfg.smtp_port) as server:
                server.starttls()
                server.login(self.cfg.smtp_user, self.cfg.smtp_password)
                server.send_message(msg)
            log.info(f"Email enviado a {destinatario}")
            return True
        except Exception as e:
            log.error(f"Error al enviar email: {e}")
            return False

    def responder_y_imprimir(self, pregunta: str):
        result = self.agent.ask(pregunta)
        respuesta = result.get("respuesta", "")
        fuentes = result.get("fuentes", [])
        print(f"Pregunta: {pregunta}")
        print()
        print(respuesta)
        print(self._formatear_fuentes(fuentes))
        print()
        ok = self.responder(pregunta)
        print(f"Email enviado: {'Sí' if ok else 'No (revisa credenciales)'}")
