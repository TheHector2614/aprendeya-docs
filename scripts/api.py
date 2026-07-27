"""
API REST — Agente RAG AprendeYa
Endpoints:
  POST /ask    →  responde una pregunta
  GET  /health →  health check
  GET  /       →  chat web UI

Uso local:   python api.py
             http://localhost:8000
Despliegue:  Docker + OCI (Container Instance privada + Load Balancer)
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pipeline.agent import Agent

# ── OCI Vault: retrieve GROQ_API_KEY if not set in env ──────────
OCI_VAULT_SECRET_ID = os.getenv("OCI_VAULT_SECRET_ID", "")
if not os.getenv("GROQ_API_KEY") and OCI_VAULT_SECRET_ID:
    try:
        import oci

        signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
        client = oci.secrets.SecretsClient(config={}, signer=signer)
        secret_bundle = client.get_secret_bundle(OCI_VAULT_SECRET_ID)
        content = secret_bundle.data.secret_bundle_content.content
        import base64
        os.environ["GROQ_API_KEY"] = base64.b64decode(content).decode("utf-8").strip()
    except Exception as e:
        print(f"[OCI Vault] No se pudo recuperar el secreto: {e}")

# ── App Setup ────────────────────────────────────────────────────
HERE = Path(__file__).resolve().parent

app = FastAPI(title="AprendeYa — Agente Documental", version="1.0.0")

# Por defecto se mantiene abierto (el sitio es público y no se envían cookies
# ni credenciales), pero CORS_ALLOW_ORIGINS permite restringirlo al dominio del
# frontend en producción: "https://docs.aprendeya.com,https://aprendeya.com".
_origins = os.getenv("CORS_ALLOW_ORIGINS", "*")
ALLOWED_ORIGINS = ["*"] if _origins.strip() == "*" else [
    o.strip() for o in _origins.split(",") if o.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

agent = Agent()


# ── Schemas ──────────────────────────────────────────────────────
class AskRequest(BaseModel):
    # Sin límites, un `question` de megabytes o un `top_k` enorme se traducían
    # directamente en trabajo de embedding y de consulta a Chroma por parte de
    # un cliente anónimo.
    question: str = Field(min_length=1, max_length=1000)
    top_k: int = Field(default=3, ge=1, le=20)


class AskResponse(BaseModel):
    pregunta: str
    respuesta: str
    fuentes: list[dict]
    # Agent.ask ya devolvía este valor, pero al no estar declarado aquí el
    # response_model lo descartaba antes de llegar al cliente.
    confianza: float | None = None


# ── Endpoints ────────────────────────────────────────────────────
@app.get("/health")
def health():
    return {
        "status": "ok",
        "indice": agent.indexer.count(),
        "modelo": "llama-3.3-70b-versatile (Groq)",
        "embedding": "paraphrase-multilingual-MiniLM-L12-v2",
    }


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    return agent.ask(req.question, top_k=req.top_k)


@app.get("/", response_class=HTMLResponse)
@app.get("/chat", response_class=HTMLResponse)
def chat_ui():
    html_path = HERE / "chat.html"
    if html_path.exists():
        return HTMLResponse(html_path.read_text("utf-8"))
    return HTMLResponse("<h1>chat.html no encontrado</h1>", status_code=404)


# ── Entry point ──────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        proxy_headers=True,
        forwarded_allow_ips="*",
    )
