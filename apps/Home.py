"""Punto de entrada unificado de la aplicación Streamlit del Observatorio SECOP II."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
for ruta in (PROJECT_ROOT, PROJECT_ROOT / "src"):
    if str(ruta) not in sys.path:
        sys.path.insert(0, str(ruta))

import streamlit as st

st.set_page_config(
    page_title="Observatorio Ciudadano SECOP II",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

from apps.ui_utils import (
    aplicar_estilo_minimalista,
    renderizar_aviso_uso_responsable,
    renderizar_encabezado_institucional,
    renderizar_pie_licencia,
)
from apps.rag_app import renderizar_vista_rag
from apps.ml_app import renderizar_vista_ml

aplicar_estilo_minimalista()

# ── Navegación ────────────────────────────────────────────────────────────────
st.sidebar.markdown(
    '<div class="text-kicker">Navegación del Observatorio</div>',
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

# ── Panel de inicialización de datos ─────────────────────────────────────────
st.sidebar.markdown("---")

from observatorio.config import SQLITE_DB_PATH, MODEL_ARTIFACT_PATH

db_ok = SQLITE_DB_PATH.exists()
ml_ok = MODEL_ARTIFACT_PATH.exists()

with st.sidebar.expander("⚙️ Datos y Modelo", expanded=not (db_ok and ml_ok)):
    st.markdown(
        f"**Base de datos:** {'✅ lista' if db_ok else '❌ no generada'}  \n"
        f"**Modelo ML:** {'✅ listo' if ml_ok else '❌ no entrenado'}"
    )

    if st.button("🔄 Inicializar / Actualizar datos", use_container_width=True):
        from setup_data import inicializar_datos

        log = st.empty()
        msgs: list[str] = []

        class _StreamlitLogger:
            """Redirige print() al widget de log en tiempo real."""
            def write(self, msg: str) -> None:
                stripped = msg.strip()
                if stripped:
                    msgs.append(stripped)
                    log.code("\n".join(msgs))
            def flush(self) -> None:
                pass

        import sys as _sys
        _orig = _sys.stdout
        _sys.stdout = _StreamlitLogger()
        try:
            inicializar_datos(verbose=True)
            st.success("Inicialización completada.")
            st.cache_resource.clear()
            st.rerun()
        except Exception as exc:
            st.error(f"Error: {exc}")
        finally:
            _sys.stdout = _orig

# ── Contenido principal ───────────────────────────────────────────────────────
if modulo.startswith("1."):
    renderizar_encabezado_institucional("Módulo A: Asistente Normativo y Consultas Analíticas")
    renderizar_aviso_uso_responsable()
    renderizar_vista_rag()
else:
    renderizar_encabezado_institucional("Módulo B: Estimador de Riesgo de Prórroga al Momento de la Firma")
    renderizar_aviso_uso_responsable()
    renderizar_vista_ml()

renderizar_pie_licencia(fecha_corte="2026-10-31")
