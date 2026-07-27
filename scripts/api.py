"""
API REST — Agente RAG AprendeYa
Endpoints:
  POST /ask    →  responde una pregunta
  GET  /health →  health check
  GET  /       →  chat web UI

Uso local:   python api.py
             http://localhost:8000
Despliegue:  Docker + OCI Container Instances (GROQ_API_KEY via OCI Vault)
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = Agent()


# ── Schemas ──────────────────────────────────────────────────────
class AskRequest(BaseModel):
    question: str
    top_k: int = 3


class AskResponse(BaseModel):
    pregunta: str
    respuesta: str
    fuentes: list[dict]


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


@app.get("/")
@app.get("/chat")
def chat_ui():
    html_path = HERE / "chat.html"
    if html_path.exists():
        return HTMLResponse(html_path.read_text("utf-8"))
    return HTMLResponse("<h1>chat.html no encontrado</h1>")


# ── Entry point ──────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
