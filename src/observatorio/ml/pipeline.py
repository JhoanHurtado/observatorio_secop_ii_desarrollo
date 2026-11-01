"""Construcción del Pipeline de preprocesamiento y modelado clásico en scikit-learn (RF-ML2, RF-ML3)."""

from __future__ import annotations

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from observatorio.config import RANDOM_SEED
from observatorio.ml.features import (
    FEATURES_CATEGORICAS_PERMITIDAS,
    FEATURES_NUMERICAS_PERMITIDAS,
)


def construir_preprocesador(
    features_num: list[str] = FEATURES_NUMERICAS_PERMITIDAS,
    features_cat: list[str] = FEATURES_CATEGORICAS_PERMITIDAS,
) -> ColumnTransformer:
    """
    Crea el `ColumnTransformer` que se ajusta únicamente sobre el conjunto de entrenamiento:
    - Imputación de mediana y escalado estándar para numéricas.
    - Imputación de constante y OneHotEncoder con agrupación de categorías poco frecuentes para categóricas.
    """
    transformador_numerico = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    transformador_categorico = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value="DESCONOCIDO")),
            (
                "onehot",
                OneHotEncoder(
                    handle_unknown="infrequent_if_exist",
                    min_frequency=0.01,
                    sparse_output=False,
                ),
            ),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", transformador_numerico, features_num),
            ("cat", transformador_categorico, features_cat),
        ],
        remainder="drop",
    )


def construir_modelos() -> dict[str, Pipeline]:
    """
    Devuelve los 4 pipelines a comparar. Cada uno incluye su propio preprocesador,
    así el escalado/encoding se ajusta solo con los datos de entrenamiento.
    `class_weight="balanced"` compensa que las prórrogas son la clase minoritaria.
    """
    clasificadores = {
        # Línea base: predice siempre la proporción observada (no aprende nada)
        "Baseline": DummyClassifier(strategy="prior"),
        "Regresión Logística": LogisticRegression(
            class_weight="balanced", max_iter=2000, random_state=RANDOM_SEED
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=300,
            min_samples_leaf=5,
            class_weight="balanced_subsample",
            n_jobs=-1,
            random_state=RANDOM_SEED,
        ),
        "Gradient Boosting": HistGradientBoostingClassifier(
            learning_rate=0.1,
            max_iter=300,
            class_weight="balanced",
            random_state=RANDOM_SEED,
        ),
    }
    return {
        nombre: Pipeline([("preprocesador", construir_preprocesador()), ("modelo", clf)])
        for nombre, clf in clasificadores.items()
    }


def evaluar_modelo(modelo: Pipeline, X: pd.DataFrame, y: pd.Series, umbral: float = 0.5) -> dict[str, float]:
    """Calcula las métricas clave en un conjunto (PR-AUC es la principal por el desbalance)."""
    prob = modelo.predict_proba(X)[:, 1]
    pred = (prob >= umbral).astype(int)
    return {
        "PR-AUC": average_precision_score(y, prob),
        "ROC-AUC": roc_auc_score(y, prob),
        "Precision": precision_score(y, pred, zero_division=0),
        "Recall": recall_score(y, pred, zero_division=0),
        "F1": f1_score(y, pred, zero_division=0),
    }
