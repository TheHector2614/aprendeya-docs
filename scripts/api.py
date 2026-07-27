"""
API REST — Agente RAG AprendeYa
Endpoints:
  POST /ask    →  responde una pregunta
  GET  /health →  health check
  GET  /       →  chat web UI

Uso: python api.py
     http://localhost:8000
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pipeline.agent import Agent

HERE = Path(__file__).resolve().parent

app = FastAPI(title="AprendeYa — Agente Documental", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = Agent()


class AskRequest(BaseModel):
    question: str
    top_k: int = 3


class AskResponse(BaseModel):
    pregunta: str
    respuesta: str
    fuentes: list[dict]


@app.get("/health")
def health():
    return {"status": "ok", "indice": agent.indexer.count()}


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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
