"""Descarga reproducible del subconjunto de SECOP II vía API Socrata (RF-2 / RF-ML1)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import pandas as pd
import requests

from observatorio.config import (
    SOCRATA_DATASET_ID,
    SOCRATA_APP_TOKEN,
    SECOP_DEPARTAMENTO,
    SECOP_FECHA_INICIO,
    SECOP_FECHA_FIN,
)

# Columnas requeridas para el Componente A (SQL) y el Componente B (ML)
# Excluye explícitamente datos personales y bancarios desde el origen (Ley 1581 de 2012)
COLUMNAS_SELECCIONADAS: list[str] = [
    "id_contrato",
    "nombre_entidad",
    "departamento",
    "ciudad",
    "sector",
    "rama",
    "orden",
    "estado_contrato",
    "tipo_de_contrato",
    "modalidad_de_contratacion",
    "fecha_de_firma",
    "fecha_de_inicio_del_contrato",
    "fecha_de_fin_del_contrato",
    "valor_del_contrato",
    "dias_adicionados",
    "es_pyme",
    "es_grupo",
    "habilita_pago_adelantado",
    "origen_de_los_recursos",
    "codigo_de_categoria_principal",
    "tipodocproveedor",
    "proveedor_adjudicado",
    "descripcion_del_proceso",
    "objeto_del_contrato",
    "urlproceso",
]


def construir_endpoint_socrata(dataset_id: str = SOCRATA_DATASET_ID) -> str:
    """Retorna la URL del recurso JSON en Datos Abiertos Colombia."""
    return f"https://www.datos.gov.co/resource/{dataset_id}.json"


def descargar_subconjunto_secop(
    departamento: str = SECOP_DEPARTAMENTO,
    fecha_inicio: str = SECOP_FECHA_INICIO,
    fecha_fin: str = SECOP_FECHA_FIN,
    batch_size: int = 10000,
    max_records: int = 100000,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """
    Descarga de forma paginada el subconjunto de contratos desde la API Socrata
    y registra la fecha exacta de consulta para trazabilidad.
    """
    endpoint = construir_endpoint_socrata()
    headers: dict[str, str] = {}
    if SOCRATA_APP_TOKEN:
        headers["X-App-Token"] = SOCRATA_APP_TOKEN

    where_clause = (
        f"departamento='{departamento}' "
        f"AND fecha_de_firma >= '{fecha_inicio}' "
        f"AND fecha_de_firma <= '{fecha_fin}'"
    )

    registros: list[dict[str, Any]] = []
    offset = 0
    fecha_consulta = datetime.now(timezone.utc).isoformat()

    while offset < max_records:
        params = {
            "$select": ", ".join(COLUMNAS_SELECCIONADAS),
            "$where": where_clause,
            "$order": "id_contrato ASC",
            "$limit": min(batch_size, max_records - offset),
            "$offset": offset,
        }
        response = requests.get(endpoint, params=params, headers=headers, timeout=60)
        response.raise_for_status()
        lote = response.json()
        if not lote:
            break
        registros.extend(lote)
        offset += len(lote)
        if len(lote) < batch_size:
            break

    df = pd.DataFrame(registros)
    metadatos_descarga = {
        "fecha_consulta_utc": fecha_consulta,
        "departamento": departamento,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "total_registros_descargados": len(df),
        "dataset_id": SOCRATA_DATASET_ID,
    }
    return df, metadatos_descarga

