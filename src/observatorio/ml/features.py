"""Definición de variables permitidas al firmar y prevención de Data Leakage (Sección 5.2, RF-ML2)."""

from __future__ import annotations

import numpy as np
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


COLUMNA_OBJETIVO: str = "prorroga"


def construir_dataset_modelado(df: pd.DataFrame, fecha_corte: str | None = None) -> pd.DataFrame:
    """
    Prepara la tabla de modelado a partir de los contratos limpios:

    1. Crea la variable objetivo `prorroga` (1 si `dias_adicionados > 0`).
    2. Deriva variables conocidas el día de la firma (valor en log, mes/año, duración planeada, segmento UNSPSC).
    3. Excluye contratos "censurados": los que aún no llegan a su fecha de fin planeada,
       porque todavía no han tenido oportunidad de pedir prórroga (serían falsos negativos).
    """
    datos = df.copy()

    # Fechas a tipo datetime
    for col in ["fecha_de_firma", "fecha_de_inicio_del_contrato", "fecha_de_fin_del_contrato"]:
        datos[col] = pd.to_datetime(datos[col], errors="coerce")

    # Variable objetivo binaria
    datos[COLUMNA_OBJETIVO] = (datos["dias_adicionados"].fillna(0) > 0).astype(int)

    # Valor del contrato en escala logarítmica (los montos están muy sesgados)
    datos["valor_contrato_log"] = np.log1p(datos["valor_del_contrato"].clip(lower=0))

    # Calendario de la firma
    datos["mes_firma"] = datos["fecha_de_firma"].dt.month
    datos["anio_firma"] = datos["fecha_de_firma"].dt.year

    # Duración planeada: fin pactado - inicio (si no hay inicio se usa la firma)
    inicio = datos["fecha_de_inicio_del_contrato"].fillna(datos["fecha_de_firma"])
    duracion = (datos["fecha_de_fin_del_contrato"] - inicio).dt.days
    # Duraciones negativas son errores de captura -> se dejan como nulo para imputarlas
    datos["duracion_planeada_dias"] = duracion.where(duracion >= 0)

    # Segmento UNSPSC = 2 primeros dígitos del código (ej: 'V1.80111600' -> '80')
    codigo = datos["codigo_de_categoria_principal"].astype(str).str.extract(r"(\d{2})")[0]
    datos["segmento_unspsc"] = codigo.fillna("DESCONOCIDO")

    # Quitar contratos cuyo plazo aún no termina (censura a la derecha)
    corte = pd.Timestamp(fecha_corte) if fecha_corte else datos["fecha_de_firma"].max()
    datos = datos[datos["fecha_de_fin_del_contrato"] < corte]

    return datos.sort_values("fecha_de_firma").reset_index(drop=True)


def verificar_ausencia_leakage(columnas_entrada: list[str] | pd.Index) -> None:
    """Lanza un ValueError si alguna columna de entrada pertenece a las excluidas por fuga."""
    interseccion = set(columnas_entrada).intersection(VARIABLES_EXCLUIDAS_LEAKAGE)
    if interseccion:
        raise ValueError(
            f"¡Alerta de Data Leakage! Se detectaron variables post-firma prohibidas: {sorted(interseccion)}"
        )

