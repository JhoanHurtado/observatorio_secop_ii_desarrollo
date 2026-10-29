"""Punto de entrada unificado de la aplicación Streamlit del Observatorio SECOP II."""

from __future__ import annotations

import sys
from pathlib import Path

# Garantizar que la raíz del proyecto y `src/` estén en sys.path al ejecutar `streamlit run apps/Home.py`
PROJECT_ROOT = Path(__file__).resolve().parents[1]
for ruta in (PROJECT_ROOT, PROJECT_ROOT / "src"):
    if str(ruta) not in sys.path:
        sys.path.insert(0, str(ruta))

import streamlit as st
from apps.ui_utils import renderizar_aviso_uso_responsable, renderizar_pie_licencia
from apps.rag_app import renderizar_vista_rag
from apps.ml_app import renderizar_vista_ml

st.set_page_config(
    page_title="Observatorio Ciudadano SECOP II",
    page_icon="🏛️",
    layout="wide",
)

st.title("🏛️ Observatorio Ciudadano de Contratación Pública (SECOP II)")
renderizar_aviso_uso_responsable()

modulo = st.sidebar.radio(
    "Selecciona el Componente:",
    options=[
        "A. Asistente Híbrido (RAG Normativo + SQL)",
        "B. Explorador y Predictor de Prórrogas (ML)",
    ],
)

if modulo.startswith("A."):
    renderizar_vista_rag()
else:
    renderizar_vista_ml()

renderizar_pie_licencia()

