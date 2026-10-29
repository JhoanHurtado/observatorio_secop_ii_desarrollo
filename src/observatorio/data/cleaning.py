"""Limpieza general, conversión de tipos y protección de datos personales (PII)."""

from __future__ import annotations

import pandas as pd

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


def limpiar_contratos_secop(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia el DataFrame descargado de SECOP II:
    1. Elimina cualquier columna en la lista negra de PII/datos bancarios.
    2. Elimina duplicados por `id_contrato`.
    3. Convierte tipos numéricos (`valor_del_contrato`, `dias_adicionados`) y fechas.
    4. Anonimiza el nombre de `proveedor_adjudicado` cuando no sea persona jurídica (NIT).
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

    # 4. Conversión de fechas
    for col_fecha in ["fecha_de_firma", "fecha_de_inicio_del_contrato", "fecha_de_fin_del_contrato"]:
        if col_fecha in df_clean.columns:
            df_clean[col_fecha] = pd.to_datetime(df_clean[col_fecha], errors="coerce")

    # 5. Protección de personas naturales en proveedor_adjudicado (Sección 6.2)
    if "tipodocproveedor" in df_clean.columns and "proveedor_adjudicado" in df_clean.columns:
        es_persona_juridica = (
            df_clean["tipodocproveedor"]
            .astype(str)
            .str.upper()
            .str.contains("NIT", na=False)
        )
        df_clean.loc[~es_persona_juridica, "proveedor_adjudicado"] = "PERSONA NATURAL (ANONIMIZADO)"

    return df_clean.reset_index(drop=True)

