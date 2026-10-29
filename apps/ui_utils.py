"""Componentes compartidos de interfaz, avisos de uso responsable y atribución CC BY-SA 4.0."""

from __future__ import annotations

import streamlit as st


def renderizar_aviso_uso_responsable() -> None:
    """Muestra el aviso obligatorio de uso responsable (Sección 1 y RF-ML7)."""
    st.info(
        "⚠️ **Uso Responsable:** Los resultados de este observatorio describen patrones estadísticos "
        "y **no constituyen evidencia de irregularidades**. Toda alerta debe verificarse en el "
        "proceso oficial disponible en el campo `urlproceso` de SECOP II."
    )


def renderizar_pie_licencia(fecha_corte: str = "Pendiente de actualización") -> None:
    """Muestra la atribución exigida por la licencia CC BY-SA 4.0 (Sección 6.3)."""
    st.divider()
    st.caption(
        f"**Atribución de Datos (CC BY-SA 4.0):** Datos originarios de *«SECOP II – Contratos Electrónicos»*, "
        f"Colombia Compra Eficiente (Agencia Nacional de Contratación Pública), Portal Nacional de Datos Abiertos "
        f"(https://www.datos.gov.co/Estad-sticas-Nacionales/SECOP-II-Contratos-Electr-nicos/jbjy-vk9h). "
        f"Licencia: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). "
        f"Fecha de corte: `{fecha_corte}`. Este proyecto no está afiliado ni respaldado por Colombia Compra Eficiente."
    )

