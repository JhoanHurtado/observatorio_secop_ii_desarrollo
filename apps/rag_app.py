"""Interfaz del Asistente Normativo y Analítico (RAG + SQL) en Streamlit."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from observatorio.rag.assistant import AsistenteHibrido, RespuestaAsistente


@st.cache_resource(show_spinner="Iniciando motor de consulta híbrido...")
def obtener_asistente_local() -> AsistenteHibrido:
    """Carga una única instancia del asistente en memoria local."""
    return AsistenteHibrido(usar_local=True)


@st.cache_resource(show_spinner="Conectando asistente con Gemini Flash...")
def obtener_asistente_gemini() -> AsistenteHibrido:
    """Carga instancia híbrida con Gemini Flash."""
    return AsistenteHibrido(usar_local=False)


def renderizar_vista_rag() -> None:
    """Renderiza el asistente conversacional con control de trazabilidad de fuentes y SQL."""
    st.subheader("Asistente de Consulta Normativa y Analítica")
    st.caption(
        "Combina la consulta estructurada en SQLite sobre 50.000 contratos de SECOP II "
        "con el corpus jurídico de contratación estatal (Ley 80, Ley 1150, Decreto 1082 y Guías CCE)."
    )

    # Configuración en barra lateral
    with st.sidebar:
        st.markdown("### Configuración del Asistente")
        modo_seleccionado = st.radio(
            "Modo de Inferencia:",
            options=["Local (Autónomo)", "Nube (Gemini 2.5 Flash)"],
            index=0,
            help="El modo local opera offline sin consumir cuotas de API ni requerir llaves.",
        )
        usar_local = modo_seleccionado.startswith("Local")

        filtro_doc = st.selectbox(
            "Filtrar por Documento Normativo:",
            options=[
                "Todos los documentos",
                "Ley 80 de 1993",
                "Ley 1150 de 2007",
                "Decreto 1082 de 2015",
                "MANUAL DE LA MODALIDAD DE SELECCIÓN DE MÍNIMA CUANTÍA",
                "guia_para_el_control_social_a_la_contratacion_en_la_gestion_publica",
            ],
            index=0,
        )
        doc_filtro_param = None if filtro_doc == "Todos los documentos" else filtro_doc

        top_k = st.slider("Fragmentos normativos a recuperar (Top-k):", min_value=2, max_value=5, value=3)

        if st.button("Limpiar conversación"):
            st.session_state.mensajes_rag = []
            st.rerun()

    # Cargar asistente según el modo
    asistente = obtener_asistente_local() if usar_local else obtener_asistente_gemini()

    # Historial de conversación
    if "mensajes_rag" not in st.session_state:
        st.session_state.mensajes_rag = []

    # Preguntas rápidas sugeridas
    st.markdown("<div class='text-kicker'>Consultas frecuentes de veeduría:</div>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    pregunta_rapida = None
    if col1.button("Top entidades por monto", use_container_width=True):
        pregunta_rapida = "¿Cuáles son las 5 entidades con mayor valor contratado?"
    if col2.button("Contratos con prórrogas", use_container_width=True):
        pregunta_rapida = "¿Cuántos contratos tuvieron prórrogas o días adicionados y cuál es el promedio?"
    if col3.button("Contratación directa", use_container_width=True):
        pregunta_rapida = "¿Cuáles son las causales de contratación directa según la Ley 1150?"
    if col4.button("Capacidad residual", use_container_width=True):
        pregunta_rapida = "¿Cómo se define la capacidad residual según el Decreto 1082?"

    # Renderizar historial previo
    for msg in st.session_state.mensajes_rag:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "metadatos" in msg and msg["metadatos"]:
                meta = msg["metadatos"]
                st.caption(
                    f"⏱️ Latencia: {meta.get('latencia', 0.0):.2f}s · Modo: {meta.get('modo', 'local')} · Ámbito: {meta.get('tipo', 'general')}"
                )

    # Captura de input (por chat o botón rápido)
    entrada_usuario = st.chat_input("Escribe tu consulta sobre normas o contratos...")
    pregunta_final = pregunta_rapida or entrada_usuario

    if pregunta_final:
        # 1. Guardar y mostrar mensaje de usuario
        st.session_state.mensajes_rag.append({"role": "user", "content": pregunta_final})
        with st.chat_message("user"):
            st.markdown(pregunta_final)

        # 2. Obtener respuesta del asistente
        with st.chat_message("assistant"):
            with st.spinner("Analizando registros y normativa..."):
                resp: RespuestaAsistente = asistente.responder(
                    pregunta=pregunta_final,
                    filtro_documento=doc_filtro_param,
                    top_k=top_k,
                )

            st.markdown(resp.respuesta)
            st.caption(
                f"⏱️ Latencia: {resp.latencia_segundos:.2f}s · Modo: {resp.modo_utilizado} · Ámbito: {resp.tipo_consulta}"
            )

            meta_dict = {
                "tipo": resp.tipo_consulta,
                "latencia": resp.latencia_segundos,
                "modo": resp.modo_utilizado,
            }

        # Guardar en sesión
        st.session_state.mensajes_rag.append({
            "role": "assistant",
            "content": resp.respuesta,
            "metadatos": meta_dict,
        })
