"""Componentes compartidos de interfaz, avisos de uso responsable y diseño minimalista geométrico y recto."""

from __future__ import annotations

import streamlit as st


def aplicar_estilo_minimalista() -> None:
    """Aplica tipografía, espaciado y paleta editorial sin bordes redondeados y sin verdes."""
    st.markdown(
        """
        <style>
        /* ====================================================================
           REGLA MAESTRA DE GEOMETRÍA: BORDES RECTOS (0PX BORDER-RADIUS)
           ==================================================================== */
        * {
            border-radius: 0px !important;
        }

        /* Contenedor principal con márgenes equilibrados */
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2.5rem;
            max-width: 1120px;
        }

        /* Tipografía editorial de alta legibilidad */
        h1, h2, h3, h4, h5, h6 {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            font-weight: 600;
            color: var(--text-color, #0f172a) !important;
            letter-spacing: -0.025em;
        }
        
        p, li {
            color: var(--text-color, #1e293b);
            font-size: 0.94rem;
            line-height: 1.62;
        }

        /* Textos auxiliares */
        .text-muted {
            color: var(--text-color, #475569) !important;
            opacity: 0.8;
            font-size: 0.85rem;
            line-height: 1.45;
        }
        .text-kicker {
            font-size: 0.76rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 600;
            color: var(--text-color, #475569) !important;
            opacity: 0.85;
            margin-bottom: 0.35rem;
        }

        /* Encabezado Institucional sobrio */
        .header-container {
            border-bottom: 1px solid rgba(148, 163, 184, 0.35);
            padding-bottom: 0.85rem;
            margin-bottom: 1.25rem;
        }
        .header-title {
            font-size: 1.55rem;
            font-weight: 700;
            color: var(--text-color, #0f172a) !important;
            margin-top: 0.25rem;
            letter-spacing: -0.02em;
        }
        .header-badges {
            margin-top: 0.5rem;
            display: flex;
            flex-wrap: wrap;
            gap: 0.4rem;
        }

        /* Banner de Protocolo de Veeduría */
        .protocol-banner {
            background-color: var(--secondary-background-color, #f8fafc);
            border-left: 3px solid #1e3a8a;
            border-top: 1px solid rgba(148, 163, 184, 0.25);
            border-right: 1px solid rgba(148, 163, 184, 0.25);
            border-bottom: 1px solid rgba(148, 163, 184, 0.25);
            padding: 0.85rem 1.15rem;
            margin-bottom: 1.25rem;
        }
        .protocol-title {
            color: var(--text-color, #0f172a);
            font-size: 0.88rem;
            font-weight: 700;
        }
        .protocol-body {
            color: var(--text-color, #334155);
            opacity: 0.9;
            font-size: 0.88rem;
            line-height: 1.55;
        }

        /* Tarjetas de Métricas Rectas */
        .metric-card {
            background-color: var(--secondary-background-color, #f8fafc);
            border: 1px solid rgba(148, 163, 184, 0.3);
            padding: 1.1rem 1.25rem;
            margin-bottom: 0.85rem;
            box-shadow: none !important;
        }
        .metric-label {
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--text-color, #475569) !important;
            opacity: 0.8;
            margin-bottom: 0.35rem;
        }
        .metric-value {
            font-size: 1.65rem;
            font-weight: 700;
            color: var(--text-color, #0f172a) !important;
            line-height: 1.2;
        }
        .metric-subtext {
            font-size: 0.82rem;
            color: var(--text-color, #64748b) !important;
            opacity: 0.75;
            margin-top: 0.35rem;
        }

        /* Listas dentro de tarjetas de contexto */
        .card-list {
            font-size: 0.88rem;
            margin-bottom: 0;
            padding-left: 1.2rem;
            color: var(--text-color, #1e293b);
            line-height: 1.6;
        }
        .card-list-warning {
            color: #b91c1c !important;
        }

        /* Badges de Estado (Paleta sobria sin verdes) */
        .status-badge {
            display: inline-block;
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.22rem 0.6rem;
            letter-spacing: 0.02em;
        }
        .badge-neutral {
            background-color: rgba(100, 116, 139, 0.12);
            color: var(--text-color, #334155) !important;
            border: 1px solid rgba(100, 116, 139, 0.3);
        }
        .badge-primary {
            background-color: rgba(30, 58, 138, 0.10);
            color: #1e3a8a !important;
            border: 1px solid rgba(30, 58, 138, 0.35);
        }
        .badge-warning {
            background-color: rgba(217, 119, 6, 0.10);
            color: #b45309 !important;
            border: 1px solid rgba(217, 119, 6, 0.35);
        }
        .badge-danger {
            background-color: rgba(185, 28, 28, 0.10);
            color: #b91c1c !important;
            border: 1px solid rgba(185, 28, 28, 0.35);
        }

        /* ====================================================================
           DISEÑO DEL CHAT (PRECISO, EDITORIAL, SIN BORDES REDONDEADOS)
           ==================================================================== */
        [data-testid="stChatMessage"] {
            background-color: var(--secondary-background-color, #f8fafc) !important;
            border: 1px solid rgba(148, 163, 184, 0.28) !important;
            padding: 1.15rem 1.35rem !important;
            margin-bottom: 0.9rem !important;
        }

        [data-testid="stChatMessage"] p {
            font-size: 0.94rem;
            line-height: 1.65;
            color: var(--text-color) !important;
        }

        [data-testid="stChatMessage"] h3 {
            font-size: 1.15rem !important;
            margin-top: 0.4rem !important;
            margin-bottom: 0.65rem !important;
            border-bottom: 1px solid rgba(148, 163, 184, 0.2);
            padding-bottom: 0.35rem;
        }

        [data-testid="stChatMessage"] blockquote {
            border-left: 2px solid #1e3a8a !important;
            padding-left: 0.85rem !important;
            margin: 0.65rem 0 !important;
            background-color: rgba(100, 116, 139, 0.05);
            color: var(--text-color);
            opacity: 0.9;
        }

        /* Tablas Markdown limpias en el chat */
        [data-testid="stChatMessage"] table {
            width: 100%;
            border-collapse: collapse;
            margin: 0.85rem 0;
            font-size: 0.86rem;
            border: 1px solid rgba(148, 163, 184, 0.3);
        }
        [data-testid="stChatMessage"] th {
            background-color: rgba(100, 116, 139, 0.08);
            border: 1px solid rgba(148, 163, 184, 0.3);
            padding: 0.5rem 0.75rem;
            font-weight: 600;
            text-align: left;
        }
        [data-testid="stChatMessage"] td {
            border: 1px solid rgba(148, 163, 184, 0.25);
            padding: 0.45rem 0.75rem;
        }

        /* Botones del sistema y preguntas rápidas */
        .stButton>button {
            border: 1px solid rgba(148, 163, 184, 0.45) !important;
            background-color: var(--secondary-background-color) !important;
            color: var(--text-color) !important;
            font-weight: 500;
            font-size: 0.84rem;
            padding: 0.45rem 0.85rem;
            transition: all 0.15s ease-in-out;
        }
        .stButton>button:hover {
            border-color: #1e3a8a !important;
            background-color: rgba(30, 58, 138, 0.06) !important;
            color: #1e3a8a !important;
        }

        /* Campo de texto del chat */
        [data-testid="stChatInput"] {
            border: 1px solid rgba(148, 163, 184, 0.45) !important;
            background-color: var(--secondary-background-color) !important;
        }
        [data-testid="stChatInput"] textarea {
            font-size: 0.92rem;
            color: var(--text-color) !important;
        }

        /* Pie de página */
        .footer-container {
            margin-top: 3.5rem;
            padding-top: 1.25rem;
            border-top: 1px solid rgba(148, 163, 184, 0.25);
            font-size: 0.8rem;
            color: var(--text-color, #475569) !important;
            opacity: 0.8;
            line-height: 1.6;
        }
        .footer-container a {
            color: #1e3a8a !important;
            text-decoration: underline;
            font-weight: 500;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def renderizar_encabezado_institucional(subtitulo: str) -> None:
    """Encabezado sobrio de estilo prensa / observatorio institucional con bordes rectos."""
    st.markdown(
        f"""
        <div class="header-container">
            <div class="text-kicker">
                Observatorio Ciudadano de Contratación Pública · SECOP II
            </div>
            <div class="header-title">
                {subtitulo}
            </div>
            <div class="header-badges">
                <span class="status-badge badge-neutral">Valle del Cauca</span>
                <span class="status-badge badge-neutral">50.000 Contratos</span>
                <span class="status-badge badge-neutral">16 Normas CCE</span>
                <span class="status-badge badge-primary">Motor Autónomo</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def renderizar_aviso_uso_responsable() -> None:
    """Muestra el aviso de uso responsable con tono neutro y fundamentado."""
    st.markdown(
        """
        <div class="protocol-banner">
            <strong class="protocol-title">Protocolo de Veeduría Ciudadana:</strong>
            <span class="protocol-body">
                Las estimaciones de riesgo y las cifras presentadas describen patrones agregados de contratación.
                No constituyen imputaciones de irregularidad o juicio de responsabilidad. Toda consulta debe ser
                contrastada con el expediente contractual original en el enlace <code>urlproceso</code> de SECOP II.
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def renderizar_pie_licencia(fecha_corte: str = "2026-10-31") -> None:
    """Atribución formal bajo licencia Creative Commons CC BY-SA 4.0."""
    st.markdown(
        f"""
        <div class="footer-container">
            <strong>Atribución de Datos:</strong> Fuente de datos abierta <em>«SECOP II – Contratos Electrónicos»</em>,
            publicada por la Agencia Nacional de Contratación Pública (Colombia Compra Eficiente) en el portal
            <a href="https://www.datos.gov.co/Estad-sticas-Nacionales/SECOP-II-Contratos-Electr-nicos/jbjy-vk9h" target="_blank">datos.gov.co</a>.
            Contenido distribuido bajo licencia <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank">CC BY-SA 4.0</a>.
            Corte del dataset: <code>{fecha_corte}</code>. Proyecto civil independiente; no representa una comunicación oficial de Colombia Compra Eficiente.
        </div>
        """,
        unsafe_allow_html=True,
    )
