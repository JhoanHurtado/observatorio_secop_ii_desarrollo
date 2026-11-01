"""Módulo de entrenamiento, comparación y evaluación de modelos ML (RF-ML3, RF-ML4).

Encapsula el ciclo de vida del modelo de estimación de riesgo de prórroga:
- Validación cruzada temporal (TimeSeriesSplit).
- Búsqueda de hiperparámetros (GridSearchCV).
- Cálculo de métricas en conjunto de prueba temporal (PR-AUC, ROC-AUC, F1, etc.).
- Análisis de importancia por permutación y segmentación de errores por modalidad.
- Serialización de artefactos (.joblib) y metadatos (.json).
"""

from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit, cross_val_score
from sklearn.pipeline import Pipeline

from observatorio.config import (
    MODEL_ARTIFACT_PATH,
    MODEL_METADATA_PATH,
    RANDOM_SEED,
)
from observatorio.ml.features import (
    FEATURES_CATEGORICAS_PERMITIDAS,
    FEATURES_NUMERICAS_PERMITIDAS,
)
from observatorio.ml.pipeline import construir_modelos, evaluar_modelo


def entrenar_y_comparar_modelos(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    n_splits: int = 3,
) -> tuple[dict[str, Pipeline], dict[str, float], str, Pipeline]:
    """
    Entrena los modelos candidatos con validación cruzada temporal (PR-AUC)
    y ajusta hiperparámetros del ensamble de Gradient Boosting.

    Returns:
        modelos: Diccionario con todos los pipelines entrenados.
        resultados_cv: Diccionario {nombre: pr_auc_cv_mean}.
        nombre_ganador: Nombre del modelo con mejor desempeño en CV.
        modelo_ganador: El pipeline ganador listo para evaluar.
    """
    cv_temporal = TimeSeriesSplit(n_splits=n_splits)
    modelos = construir_modelos()
    resultados_cv: dict[str, float] = {}

    for nombre, modelo in modelos.items():
        puntajes = cross_val_score(modelo, X_train, y_train, cv=cv_temporal, scoring="average_precision")
        resultados_cv[nombre] = float(puntajes.mean())
        modelo.fit(X_train, y_train)

    # Búsqueda compacta de hiperparámetros para Gradient Boosting
    busqueda = GridSearchCV(
        modelos["Gradient Boosting"],
        param_grid={
            "modelo__learning_rate": [0.05, 0.1],
            "modelo__max_leaf_nodes": [15, 31],
        },
        cv=cv_temporal,
        scoring="average_precision",
        n_jobs=-1,
    )
    busqueda.fit(X_train, y_train)
    modelos["Gradient Boosting (ajustado)"] = busqueda.best_estimator_
    resultados_cv["Gradient Boosting (ajustado)"] = float(busqueda.best_score_)

    nombre_ganador = max(resultados_cv, key=resultados_cv.get)
    modelo_ganador = modelos[nombre_ganador]

    return modelos, resultados_cv, nombre_ganador, modelo_ganador


def generar_tabla_comparativa_prueba(
    modelos: dict[str, Pipeline],
    X_test: pd.DataFrame,
    y_test: pd.Series,
    resultados_cv: dict[str, float],
) -> pd.DataFrame:
    """Genera la tabla comparativa de métricas en prueba contra la línea base."""
    filas = {}
    for nombre, m in modelos.items():
        m_eval = evaluar_modelo(m, X_test, y_test)
        filas[nombre] = m_eval

    df_res = pd.DataFrame(filas).T
    df_res.insert(0, "PR-AUC (CV train)", pd.Series(resultados_cv))
    return df_res.round(3)


def calcular_importancia_variables(
    modelo: Pipeline,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    n_repeats: int = 5,
) -> pd.Series:
    """Calcula la importancia por permutación sobre la métrica PR-AUC."""
    imp = permutation_importance(
        modelo,
        X_test,
        y_test,
        scoring="average_precision",
        n_repeats=n_repeats,
        random_state=RANDOM_SEED,
        n_jobs=-1,
    )
    return pd.Series(imp.importances_mean, index=X_test.columns).sort_values(ascending=False)


def analizar_errores_por_modalidad(
    modelo: Pipeline,
    df_test: pd.DataFrame,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> pd.DataFrame:
    """Segmenta falsos positivos y falsos negativos por modalidad de contratación."""
    analisis = df_test[["modalidad_de_contratacion"]].copy()
    analisis["real"] = y_test.values
    analisis["pred"] = modelo.predict(X_test)
    analisis["falso_positivo"] = (analisis["pred"] == 1) & (analisis["real"] == 0)
    analisis["falso_negativo"] = (analisis["pred"] == 0) & (analisis["real"] == 1)

    return (
        analisis.groupby("modalidad_de_contratacion")
        .agg(
            contratos=("real", "size"),
            tasa_real_prorroga=("real", "mean"),
            falsos_positivos=("falso_positivo", "sum"),
            falsos_negativos=("falso_negativo", "sum"),
        )
        .sort_values("contratos", ascending=False)
        .round(3)
    )


def guardar_artefacto_y_metadatos(
    modelo: Pipeline,
    nombre_modelo: str,
    df_train: pd.DataFrame,
    df_test: pd.DataFrame,
    df_metricas: pd.DataFrame,
    ruta_modelo: Path = MODEL_ARTIFACT_PATH,
    ruta_meta: Path = MODEL_METADATA_PATH,
) -> dict[str, Any]:
    """Serializa el modelo y genera el archivo JSON de metadatos auditable."""
    ruta_modelo.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(modelo, ruta_modelo)

    y_train = df_train["prorroga"] if "prorroga" in df_train.columns else df_train.iloc[:, -1]
    metadatos = {
        "modelo": nombre_modelo,
        "fecha_entrenamiento": datetime.now().isoformat(timespec="seconds"),
        "features_numericas": FEATURES_NUMERICAS_PERMITIDAS,
        "features_categoricas": FEATURES_CATEGORICAS_PERMITIDAS,
        "periodo_entrenamiento": [
            str(df_train["fecha_de_firma"].min().date()),
            str(df_train["fecha_de_firma"].max().date()),
        ],
        "periodo_prueba": [
            str(df_test["fecha_de_firma"].min().date()),
            str(df_test["fecha_de_firma"].max().date()),
        ],
        "tasa_prorroga_train": round(float(y_train.mean()), 4),
        "metricas_prueba": {k: round(float(v), 4) for k, v in df_metricas.loc[nombre_modelo].items()},
        "umbrales_riesgo": {"alto": 0.60, "medio": 0.30},
        "semilla": RANDOM_SEED,
    }
    ruta_meta.write_text(json.dumps(metadatos, indent=2, ensure_ascii=False), encoding="utf-8")
    return metadatos

