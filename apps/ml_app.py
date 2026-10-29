"""Componente B: Interfaz de Exploración y Predicción de Prórrogas con 4 pestañas (RF-ML5, RF-ML6)."""

from __future__ import annotations

import streamlit as st


def renderizar_vista_ml() -> None:
    """Renderiza las 4 pestañas requeridas por RF-ML5: Contexto, Exploración, Predicción y Métricas."""
    st.header("📈 Componente B: Estimación de Riesgo de Prórroga de Plazo")

    tab_contexto, tab_exploracion, tab_prediccion, tab_metricas = st.tabs(
        ["1. Contexto", "2. Exploración", "3. Predicción de Riesgo", "4. Métricas del Modelo"]
    )

    with tab_contexto:
        st.subheader("Contexto y Fuente de Datos")
        st.markdown(
            "- **Objetivo:** Estimar al momento de la firma la probabilidad de que un contrato requiera prórroga (`dias_adicionados > 0`).\n"
            "- **Prevención de Fuga de Información:** Solo se emplean variables conocidas al firmar el contrato."
        )

    with tab_exploracion:
        st.subheader("Exploración Interactiva del Subconjunto SECOP II")
        st.info("Los filtros por departamento, modalidad y año se activarán al generar `secop_contratos.sqlite`.")

    with tab_prediccion:
        st.subheader("Simulador de Riesgo de Prórroga al Momento de la Firma")
        st.info("El formulario cargará el artefacto `models/pipeline_prorrogas.joblib` generado en el Notebook.")

    with tab_metricas:
        st.subheader("Desempeño en Prueba Temporal y Comparación contra Baseline")
        st.info("Aquí se visualizará la tabla comparativa de modelos, la matriz de confusión y las curvas PR-AUC.")


if __name__ == "__main__":
    renderizar_vista_ml()
