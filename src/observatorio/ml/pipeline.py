"""Construcción del Pipeline de preprocesamiento y modelado clásico en scikit-learn (RF-ML2, RF-ML3)."""

from __future__ import annotations

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

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

