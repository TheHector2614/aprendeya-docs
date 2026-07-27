import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="huggingface_hub")

import streamlit as st
from pipeline.agent import Agent
from pipeline.config import Config

st.set_page_config(
    page_title="AprendeYa — Agente Documental",
    page_icon="\U0001F4DA",
    layout="wide",
)

cfg = Config()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    with st.spinner("Cargando agente..."):
        st.session_state.agent = Agent()
if "feedback" not in st.session_state:
    st.session_state.feedback = {}

with st.sidebar:
    st.markdown(
        f"<div style='text-align:center; padding:1rem 0'>"
        f"<h1 style='margin:0; font-size:2rem; color:#1F4E79'>\U0001F4DA</h1>"
        f"<h2 style='margin:0; color:#1F4E79'>AprendeYa</h2>"
        f"<p style='color:#666; font-size:0.9rem'>Agente Documental de IA</p>"
        f"</div>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.info(
        "\u2139\ufe0f Este es un asistente autom\u00e1tico de IA. "
        "No est\u00e1s conversando con una persona real. "
        "Las respuestas se generan con base exclusiva en los documentos "
        "corporativos indexados."
    )
    st.markdown("---")

    if st.button("\U0001F5D1\ufe0f Nueva conversaci\u00f3n", use_container_width=True):
        st.session_state.messages = []
        st.session_state.feedback = {}
        st.rerun()

    st.markdown("---")
    st.markdown("### \U0001F4CA Estado")
    st.markdown(f"**Modelo:** `{cfg.GENERATION_MODEL}`")
    st.markdown(f"**Embebidos:** `{cfg.EMBEDDING_MODEL.split('/')[-1]}`")
    st.markdown(f"**Colecci\u00f3n:** `{cfg.COLLECTION_NAME}`")
    st.markdown(f"**Fuentes:** Directorio de Contactos por \u00c1rea (REF-001)")

    st.markdown("---")
    st.markdown("### \U0001F4AC Historial")
    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            preview = msg["content"][:50] + ("..." if len(msg["content"]) > 50 else "")
            st.markdown(f"- **T\u00fa:** {preview}")

    st.markdown("---")
    st.markdown(
        "<p style='color:#999; font-size:0.75rem; text-align:center'>"
        "AprendeYa \u2022 2026</p>",
        unsafe_allow_html=True,
    )


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("fuentes"):
            with st.expander("\U0001F4CE Fuentes consultadas"):
                for f in msg["fuentes"]:
                    label = f.get("titulo", "")
                    if f.get("seccion"):
                        label += f" / {f['seccion']}"
                    rel = f.get("relevancia", "")
                    rel_str = f" (relevancia: {rel})" if rel else ""
                    st.markdown(f"- **{label}**{rel_str}")

    msg_idx = st.session_state.messages.index(msg)
    if msg["role"] == "assistant":
        fb = st.session_state.feedback.get(msg_idx)
        cols = st.columns([1, 1, 20])
        if fb is None:
            with cols[0]:
                if st.button("\U0001F44D", key=f"up_{msg_idx}", help="\u00datil"):
                    st.session_state.feedback[msg_idx] = "positive"
                    st.rerun()
            with cols[1]:
                if st.button("\U0001F44E", key=f"down_{msg_idx}", help="No \u00fatil"):
                    st.session_state.feedback[msg_idx] = "negative"
                    st.rerun()
        else:
            with cols[0]:
                icon = "\u2705" if fb == "positive" else "\U0001F4DD"
                tip = "Gracias por tu retroalimentaci\u00f3n" if fb == "positive" else "Lo tendremos en cuenta"
                st.caption(f"{icon} {tip}")

prompt = st.chat_input("Escribe tu pregunta sobre los documentos de AprendeYa...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Buscando en los documentos..."):
            result = st.session_state.agent.ask(prompt)

        respuesta = result.get("respuesta", "")
        fuentes = result.get("fuentes", [])

        st.markdown(respuesta)
        msg_data = {
            "role": "assistant",
            "content": respuesta,
            "fuentes": fuentes,
            "confianza": result.get("confianza"),
        }
        st.session_state.messages.append(msg_data)

        if fuentes:
            with st.expander("\U0001F4CE Fuentes consultadas"):
                for f in fuentes:
                    label = f.get("titulo", "")
                    if f.get("seccion"):
                        label += f" / {f['seccion']}"
                    rel = f.get("relevancia", "")
                    rel_str = f" (relevancia: {rel})" if rel else ""
                    st.markdown(f"- **{label}**{rel_str}")

        msg_idx = len(st.session_state.messages) - 1
        cols = st.columns([1, 1, 20])
        with cols[0]:
            if st.button("\U0001F44D", key=f"up_{msg_idx}", help="\u00datil"):
                st.session_state.feedback[msg_idx] = "positive"
                st.rerun()
        with cols[1]:
            if st.button("\U0001F44E", key=f"down_{msg_idx}", help="No \u00fatil"):
                st.session_state.feedback[msg_idx] = "negative"
                st.rerun()
