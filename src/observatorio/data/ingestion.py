"""Módulo de ingesta y descarga reproducible del conjunto de contratos de SECOP II vía API Socrata."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any
import pandas as pd
import requests

from observatorio.config import (
    RAW_CSV_PATH,
    RAW_METADATA_PATH,
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
    guardar_csv: bool = True,
    ruta_csv: Path = RAW_CSV_PATH,
    ruta_metadatos: Path = RAW_METADATA_PATH,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """
    Descarga de forma paginada y controlada el registro de contratos públicos desde la API Socrata.

    Qué hace:
        Consulta el catálogo de Datos Abiertos Colombia mediante filtros geográficos y temporales,
        recupera los registros en lotes paginados y genera un archivo CSV original acompañado de metadatos.

    Cómo lo hace:
        1. Configura cabeceras con el token de aplicación de Socrata (si está definido).
        2. Construye una cláusula WHERE de SoQL filtrando por departamento y rango de firma.
        3. Realiza peticiones GET iterativas incrementando el parámetro $offset hasta completar el cupo.
        4. Serializa el DataFrame consolidado a disco y guarda un archivo JSON de trazabilidad.

    Args:
        departamento: Nombre oficial del departamento territorial a filtrar.
        fecha_inicio: Fecha ISO mínima de la firma del contrato (YYYY-MM-DD).
        fecha_fin: Fecha ISO máxima de la firma del contrato (YYYY-MM-DD).
        batch_size: Cantidad de registros a solicitar por llamada HTTP.
        max_records: Límite superior global de contratos a descargar.
        guardar_csv: Si es True, persiste el resultado en disco.
        ruta_csv: Ruta de destino del archivo CSV con datos crudos.
        ruta_metadatos: Ruta del archivo JSON con la fecha y parámetros de consulta.

    Returns:
        Tupla con el DataFrame descargado y el diccionario de metadatos de auditoría.
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
    metadatos_descarga: dict[str, Any] = {
        "fecha_consulta_utc": fecha_consulta,
        "departamento": departamento,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "total_registros_descargados": len(df),
        "columnas_descargadas": list(df.columns),
        "dataset_id": SOCRATA_DATASET_ID,
        "ruta_csv_original": str(ruta_csv) if guardar_csv else None,
    }

    if guardar_csv:
        ruta_csv.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(ruta_csv, index=False, encoding="utf-8-sig")
        ruta_metadatos.parent.mkdir(parents=True, exist_ok=True)
        ruta_metadatos.write_text(
            json.dumps(metadatos_descarga, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    return df, metadatos_descarga
