"""Carga del artefacto .joblib e inferencia individual para Streamlit (< 2 segundos, RF-ML6)."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import joblib
import pandas as pd

from observatorio.config import MODEL_ARTIFACT_PATH
from observatorio.ml.features import verificar_ausencia_leakage


def cargar_modelo_prorrogas(ruta_modelo: Path = MODEL_ARTIFACT_PATH) -> Any:
    """Carga el pipeline entrenado desde disco sin reentrenar."""
    if not ruta_modelo.exists():
        raise FileNotFoundError(
            f"No se encontró el artefacto del modelo en {ruta_modelo}. "
            "Ejecuta primero la Etapa 4 del notebook para exportarlo."
        )
    return joblib.load(ruta_modelo)


def predecir_riesgo_prorroga(modelo: Any, datos_contrato: dict[str, Any]) -> dict[str, Any]:
    """
    Evalúa un registro de contrato individual y devuelve la probabilidad estimada
    y el nivel orientativo de riesgo de prórroga.
    """
    df_input = pd.DataFrame([datos_contrato])
    verificar_ausencia_leakage(df_input.columns)

    probabilidad = float(modelo.predict_proba(df_input)[0, 1])
    if probabilidad >= 0.60:
        nivel = "Alto (Priorizar revisión preventiva)"
    elif probabilidad >= 0.30:
        nivel = "Medio (Seguimiento recomendado)"
    else:
        nivel = "Bajo"

    return {
        "probabilidad_prorroga": round(probabilidad, 4),
        "nivel_riesgo": nivel,
    }

