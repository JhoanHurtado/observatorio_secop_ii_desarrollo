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

# Inicializar datos y modelo si no existen (primera ejecución en Streamlit Cloud)
try:
    from setup_data import inicializar_datos
    inicializar_datos(verbose=False)
except Exception as _e:
    st.warning(f"⚠️ No se pudo completar la inicialización de datos: {_e}")

from apps.ui_utils import (
    aplicar_estilo_minimalista,
    renderizar_aviso_uso_responsable,
    renderizar_encabezado_institucional,
    renderizar_pie_licencia,
)
from apps.rag_app import renderizar_vista_rag
from apps.ml_app import renderizar_vista_ml

st.set_page_config(
    page_title="Observatorio Ciudadano SECOP II",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilo editorial sobrio
aplicar_estilo_minimalista()

# Selección de módulo en la barra lateral
st.sidebar.markdown(
    """
    <div class="text-kicker">
        Navegación del Observatorio
    </div>
    """,
    unsafe_allow_html=True,
)

modulo = st.sidebar.radio(
    "Selecciona el Módulo:",
    options=[
        "1. Asistente Híbrido (RAG Normativo + SQL)",
        "2. Predictor de Riesgo de Prórroga (ML)",
    ],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div class="text-muted">
        <strong>Alcance Territorial:</strong> Valle del Cauca<br>
        <strong>Periodo:</strong> 2023 - 2026<br>
        <strong>Datos:</strong> datos.gov.co (SECOP II)
    </div>
    """,
    unsafe_allow_html=True,
)

if modulo.startswith("1."):
    renderizar_encabezado_institucional("Módulo A: Asistente Normativo y Consultas Analíticas")
    renderizar_aviso_uso_responsable()
    renderizar_vista_rag()
else:
    renderizar_encabezado_institucional("Módulo B: Estimador de Riesgo de Prórroga al Momento de la Firma")
    renderizar_aviso_uso_responsable()
    renderizar_vista_ml()

renderizar_pie_licencia(fecha_corte="2026-10-31")
