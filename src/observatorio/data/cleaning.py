"""Limpieza general, conversión de tipos y protección de datos personales (PII)."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import pandas as pd

from observatorio.config import CLEAN_CSV_PATH

# Columnas prohibidas por contener datos personales o bancarios (Sección 3 y 6.2)
COLUMNAS_PII_PROHIBIDAS: set[str] = {
    "documento_proveedor",
    "nombre_representante_legal",
    "identificaci_n_representante_legal",
    "domicilio_representante_legal",
    "nombre_supervisor",
    "numero_de_documento_supervisor",
    "nombre_ordenador_del_gasto",
    "numero_de_documento_ordenador_del_gasto",
    "nombre_del_banco",
    "tipo_de_cuenta",
    "numero_de_cuenta",
}

# Diccionario de las columnas seleccionadas (basado en la Ficha Técnica de Colombia Compra Eficiente)
DICCIONARIO_COLUMNAS: list[dict[str, str]] = [
    {"columna": "id_contrato", "tipo": "Texto (PK)", "uso": "Identificador único del contrato electrónico en SECOP II."},
    {"columna": "nombre_entidad", "tipo": "Categórica", "uso": "Nombre oficial de la entidad estatal contratante."},
    {"columna": "departamento", "tipo": "Categórica", "uso": "Departamento de ejecución o registro de la entidad."},
    {"columna": "ciudad", "tipo": "Categórica", "uso": "Municipio o ciudad asociada a la entidad contratante."},
    {"columna": "sector", "tipo": "Categórica", "uso": "Sector administrativo al que pertenece la entidad."},
    {"columna": "rama", "tipo": "Categórica", "uso": "Rama del poder público (Ejecutiva, Legislativa, Judicial, etc.)."},
    {"columna": "orden", "tipo": "Categórica", "uso": "Nivel administrativo (Nacional, Territorial)."},
    {"columna": "estado_contrato", "tipo": "Categórica", "uso": "Estado actual del contrato (solo para consultas SQL, excluido de ML por leakage)."},
    {"columna": "tipo_de_contrato", "tipo": "Categórica", "uso": "Tipología contractual (Prestación de servicios, Obra, Suministro, etc.)."},
    {"columna": "modalidad_de_contratacion", "tipo": "Categórica", "uso": "Modalidad legal de selección (Contratación directa, Licitación, Mínima cuantía, etc.)."},
    {"columna": "fecha_de_firma", "tipo": "Fecha", "uso": "Fecha de perfeccionamiento/firma del contrato (base de la partición temporal)."},
    {"columna": "fecha_de_inicio_del_contrato", "tipo": "Fecha", "uso": "Fecha prevista de inicio de ejecución."},
    {"columna": "fecha_de_fin_del_contrato", "tipo": "Fecha", "uso": "Fecha de terminación registrada del contrato."},
    {"columna": "valor_del_contrato", "tipo": "Numérica (COP)", "uso": "Valor cuantificado del contrato en pesos colombianos."},
    {"columna": "dias_adicionados", "tipo": "Numérica", "uso": "Días de prórroga adicionados al contrato (base de la variable objetivo: > 0)."},
    {"columna": "es_pyme", "tipo": "Categórica", "uso": "Indica si el proveedor adjudicado está clasificado como Mipyme."},
    {"columna": "es_grupo", "tipo": "Categórica", "uso": "Indica si el contratista es un consorcio o unión temporal."},
    {"columna": "habilita_pago_adelantado", "tipo": "Categórica", "uso": "Indica si el contrato contempla pago anticipado o anticipo."},
    {"columna": "origen_de_los_recursos", "tipo": "Categórica", "uso": "Fuente de financiación (Recursos propios, SGP, Regalías, Presupuesto Nacional, etc.)."},
    {"columna": "codigo_de_categoria_principal", "tipo": "Categórica", "uso": "Código del clasificador de bienes y servicios UNSPSC."},
    {"columna": "tipodocproveedor", "tipo": "Categórica", "uso": "Tipo de documento del proveedor (permite distinguir NIT de persona natural)."},
    {"columna": "proveedor_adjudicado", "tipo": "Texto", "uso": "Razón social del contratista (anonimizado si no es NIT)."},
    {"columna": "descripcion_del_proceso", "tipo": "Texto", "uso": "Descripción general del proceso de contratación."},
    {"columna": "objeto_del_contrato", "tipo": "Texto", "uso": "Objeto específico pactado en el contrato."},
    {"columna": "urlproceso", "tipo": "URL", "uso": "Enlace verificable al expediente electrónico oficial en SECOP II."},
]


def obtener_diccionario_columnas() -> pd.DataFrame:
    """Devuelve el diccionario de columnas como un DataFrame listo para mostrar en el Notebook."""
    return pd.DataFrame(DICCIONARIO_COLUMNAS)


def limpiar_contratos_secop(
    df: pd.DataFrame,
    guardar_csv: bool = True,
    ruta_csv_limpio: Path = CLEAN_CSV_PATH,
) -> pd.DataFrame:
    """
    Limpia el DataFrame descargado de SECOP II y guarda el CSV limpio en `data/processed/`:
    1. Elimina cualquier columna en la lista negra de PII/datos bancarios.
    2. Elimina duplicados por `id_contrato`.
    3. Convierte tipos numéricos (`valor_del_contrato`, `dias_adicionados`) y fechas.
    4. Extrae la URL en texto plano si `urlproceso` viene como diccionario JSON de Socrata.
    5. Anonimiza el nombre de `proveedor_adjudicado` cuando no sea persona jurídica (NIT).
    """
    df_clean = df.copy()

    # 1. Garantizar ausencia de columnas sensibles
    cols_a_eliminar = [c for c in df_clean.columns if c in COLUMNAS_PII_PROHIBIDAS]
    if cols_a_eliminar:
        df_clean = df_clean.drop(columns=cols_a_eliminar)

    # 2. Eliminar duplicados por llave única
    if "id_contrato" in df_clean.columns:
        df_clean = df_clean.drop_duplicates(subset=["id_contrato"], keep="first")

    # 3. Conversión de tipos numéricos
    for col_num in ["valor_del_contrato", "dias_adicionados"]:
        if col_num in df_clean.columns:
            df_clean[col_num] = pd.to_numeric(df_clean[col_num], errors="coerce").fillna(0.0)

    # 4. Conversión de fechas (en formato ISO YYYY-MM-DD para compatibilidad con CSV y SQLite)
    for col_fecha in ["fecha_de_firma", "fecha_de_inicio_del_contrato", "fecha_de_fin_del_contrato"]:
        if col_fecha in df_clean.columns:
            fechas_dt = pd.to_datetime(df_clean[col_fecha], errors="coerce")
            df_clean[col_fecha] = fechas_dt.dt.strftime("%Y-%m-%d")

    # 5. Normalizar `urlproceso` si viene como dict `{'url': '...'}` desde Socrata JSON
    if "urlproceso" in df_clean.columns:
        df_clean["urlproceso"] = df_clean["urlproceso"].apply(
            lambda x: x.get("url", "") if isinstance(x, dict) else str(x) if pd.notna(x) else ""
        )

    # 6. Protección de personas naturales en proveedor_adjudicado (Sección 6.2)
    if "tipodocproveedor" in df_clean.columns and "proveedor_adjudicado" in df_clean.columns:
        es_persona_juridica = (
            df_clean["tipodocproveedor"]
            .astype(str)
            .str.upper()
            .str.contains("NIT", na=False)
        )
        df_clean.loc[~es_persona_juridica, "proveedor_adjudicado"] = "PERSONA NATURAL (ANONIMIZADO)"

    df_clean = df_clean.reset_index(drop=True)

    # 7. Guardar archivo CSV limpio para validación
    if guardar_csv:
        ruta_csv_limpio.parent.mkdir(parents=True, exist_ok=True)
        df_clean.to_csv(ruta_csv_limpio, index=False, encoding="utf-8-sig")

    return df_clean


def generar_resumen_validacion(df_raw: pd.DataFrame, df_clean: pd.DataFrame) -> pd.DataFrame:
    """Genera una tabla comparativa entre el dataset original y el limpio para validación."""
    duplicados_raw = int(df_raw.duplicated(subset=["id_contrato"]).sum()) if "id_contrato" in df_raw.columns else 0
    duplicados_clean = int(df_clean.duplicated(subset=["id_contrato"]).sum()) if "id_contrato" in df_clean.columns else 0

    anonimizados_clean = 0
    if "proveedor_adjudicado" in df_clean.columns:
        anonimizados_clean = int((df_clean["proveedor_adjudicado"] == "PERSONA NATURAL (ANONIMIZADO)").sum())

    resumen: list[dict[str, Any]] = [
        {"Métrica de Validación": "Total de filas (registros)", "CSV Original (Raw)": len(df_raw), "CSV Limpio (Processed)": len(df_clean)},
        {"Métrica de Validación": "Total de columnas", "CSV Original (Raw)": df_raw.shape[1], "CSV Limpio (Processed)": df_clean.shape[1]},
        {"Métrica de Validación": "Duplicados por id_contrato", "CSV Original (Raw)": duplicados_raw, "CSV Limpio (Processed)": duplicados_clean},
        {"Métrica de Validación": "Proveedores Persona Natural anonimizados", "CSV Original (Raw)": "Sin anonimizar (0)", "CSV Limpio (Processed)": anonimizados_clean},
        {"Métrica de Validación": "Nulos en valor_del_contrato", "CSV Original (Raw)": int(df_raw["valor_del_contrato"].isna().sum()) if "valor_del_contrato" in df_raw.columns else 0, "CSV Limpio (Processed)": int(df_clean["valor_del_contrato"].isna().sum()) if "valor_del_contrato" in df_clean.columns else 0},
        {"Métrica de Validación": "Nulos en dias_adicionados", "CSV Original (Raw)": int(df_raw["dias_adicionados"].isna().sum()) if "dias_adicionados" in df_raw.columns else 0, "CSV Limpio (Processed)": int(df_clean["dias_adicionados"].isna().sum()) if "dias_adicionados" in df_clean.columns else 0},
    ]
    return pd.DataFrame(resumen)
