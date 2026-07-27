from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ChannelConfig:
    slack_bot_token: str = ""
    slack_signing_secret: str = ""
    slack_app_token: str = ""
    slack_socket_mode: bool = True

    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    email_from: str = "soporte@aprendeya.com"
    email_to: str = ""

    teams_webhook_url: str = ""

    @classmethod
    def from_env(cls) -> "ChannelConfig":
        import os
        return cls(
            slack_bot_token=os.getenv("SLACK_BOT_TOKEN", ""),
            slack_signing_secret=os.getenv("SLACK_SIGNING_SECRET", ""),
            slack_app_token=os.getenv("SLACK_APP_TOKEN", ""),
            slack_socket_mode=os.getenv("SLACK_SOCKET_MODE", "true").lower() == "true",
            smtp_host=os.getenv("SMTP_HOST", "smtp.gmail.com"),
            smtp_port=int(os.getenv("SMTP_PORT", "587")),
            smtp_user=os.getenv("SMTP_USER", ""),
            smtp_password=os.getenv("SMTP_PASSWORD", ""),
            email_from=os.getenv("EMAIL_FROM", "soporte@aprendeya.com"),
            email_to=os.getenv("EMAIL_TO", ""),
            teams_webhook_url=os.getenv("TEAMS_WEBHOOK_URL", ""),
        )

    def save_env_template(self, path: Path | None = None) -> str:
        lines = [
            "# ============================================================",
            "# AprendeYa — Channel Integrations Config",
            "# Copy to .env and fill in your credentials",
            "# ============================================================",
            "",
            "# --- Slack ---",
            "# Crea un app en https://api.slack.com/apps",
            "# Bot Token Scopes: chat:write, commands",
            'export SLACK_BOT_TOKEN="xoxb-..."',
            'export SLACK_SIGNING_SECRET="..."',
            "# Socket Mode: activar en Settings > Socket Mode",
            'export SLACK_APP_TOKEN="xapp-..."',
            "export SLACK_SOCKET_MODE=true",
            "",
            "# --- Email (SMTP) ---",
            "# Gmail: usar contraseña de aplicación",
            'export SMTP_HOST="smtp.gmail.com"',
            "export SMTP_PORT=587",
            'export SMTP_USER="soporte@aprendeya.com"',
            'export SMTP_PASSWORD="..."',
            'export EMAIL_FROM="soporte@aprendeya.com"',
            'export EMAIL_TO="colaborador@aprendeya.com"',
            "",
            "# --- Microsoft Teams ---",
            "# Crear Incoming Webhook en un canal de Teams",
            'export TEAMS_WEBHOOK_URL="https://..."',
            "",
            "# --- Groq (generaci\u00f3n de respuestas) ---",
            "# Obt\u00e9n tu API key gratis en https://console.groq.com",
            "# Modelo usado: llama3-70b-8192",
            'export GROQ_API_KEY="gsk_..."',
        ]
        text = "\n".join(lines)
        if path:
            path.write_text(text, encoding="utf-8")
        return text
