"""Definición de variables permitidas al firmar y prevención de Data Leakage (Sección 5.2, RF-ML2)."""

from __future__ import annotations

import pandas as pd

# Variables conocidas exclusivamente al momento de la firma del contrato (Sección 5.2)
FEATURES_CATEGORICAS_PERMITIDAS: list[str] = [
    "tipo_de_contrato",
    "modalidad_de_contratacion",
    "sector",
    "rama",
    "orden",
    "departamento",
    "es_pyme",
    "es_grupo",
    "habilita_pago_adelantado",
    "origen_de_los_recursos",
    "segmento_unspsc",
]

FEATURES_NUMERICAS_PERMITIDAS: list[str] = [
    "valor_contrato_log",
    "mes_firma",
    "anio_firma",
    "duracion_planeada_dias",
]

# Variables estrictamente excluidas por causar fuga de información (post-firma o target)
VARIABLES_EXCLUIDAS_LEAKAGE: set[str] = {
    "dias_adicionados",
    "prorroga",
    "valor_pagado",
    "valor_facturado",
    "valor_pendiente_de_pago",
    "valor_de_pago_adelantado",
    "valor_amortizado",
    "estado_contrato",
    "liquidaci_n",
    "fecha_ini_ejecucion",
    "fecha_fin_ejecucion",
    "reversion",
    "saldo_cdp",
}


def verificar_ausencia_leakage(columnas_entrada: list[str] | pd.Index) -> None:
    """Lanza un ValueError si alguna columna de entrada pertenece a las excluidas por fuga."""
    interseccion = set(columnas_entrada).intersection(VARIABLES_EXCLUIDAS_LEAKAGE)
    if interseccion:
        raise ValueError(
            f"¡Alerta de Data Leakage! Se detectaron variables post-firma prohibidas: {sorted(interseccion)}"
        )

