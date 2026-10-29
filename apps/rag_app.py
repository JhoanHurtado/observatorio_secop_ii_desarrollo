"""Componente A: Interfaz del Asistente en la Nube (RAG Normativo + SQL) en Streamlit (RF-9, RF-10)."""

from __future__ import annotations

import streamlit as st


def renderizar_vista_rag() -> None:
    """Renderiza el chat con memoria corta, mostrando el SQL ejecutado y los artículos citados."""
    st.header("Componente A: Asistente Normativo y Consultas SQL")
    st.markdown(
        "Formula preguntas en lenguaje natural sobre **cifras de contratos (SQLite)** "
        "y sobre el **marco legal de contratación estatal (Ley 80 de 1993, Ley 1150 de 2007, Decreto 1082 de 2015)**."
    )

    if "mensajes_rag" not in st.session_state:
        st.session_state.mensajes_rag = []

    for msg in st.session_state.mensajes_rag:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    pregunta = st.chat_input("Ej. ¿Cuántos contratos se firmaron por contratación directa y qué dice la Ley 1150?")
    if pregunta:
        st.session_state.mensajes_rag.append({"role": "user", "content": pregunta})
        with st.chat_message("user"):
            st.markdown(pregunta)

        with st.chat_message("assistant"):
            respuesta_demo = (
                "🚧 *El motor RAG + SQL se conectará una vez completes la Etapa 1 y Etapa 2 del Notebook.*"
            )
            st.markdown(respuesta_demo)
        st.session_state.mensajes_rag.append({"role": "assistant", "content": respuesta_demo})


if __name__ == "__main__":
    renderizar_vista_rag()
