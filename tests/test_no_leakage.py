"""Pruebas para garantizar que ninguna variable post-firma ingrese al modelo ML (RF-ML2)."""

import pytest
from observatorio.ml.features import (
    FEATURES_CATEGORICAS_PERMITIDAS,
    FEATURES_NUMERICAS_PERMITIDAS,
    verificar_ausencia_leakage,
)


def test_variables_permitidas_pasan_validacion() -> None:
    todas_permitidas = FEATURES_CATEGORICAS_PERMITIDAS + FEATURES_NUMERICAS_PERMITIDAS
    verificar_ausencia_leakage(todas_permitidas)


def test_detecta_fuga_de_informacion() -> None:
    columnas_con_fuga = ["tipo_de_contrato", "valor_pagado", "estado_contrato"]
    with pytest.raises(ValueError, match="Data Leakage"):
        verificar_ausencia_leakage(columnas_con_fuga)

