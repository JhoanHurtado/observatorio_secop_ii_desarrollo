"""Gestión de SQLite e interfaz de consulta SQL segura en modo solo lectura (RF-2, RF-8)."""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path
import pandas as pd

from observatorio.config import SQLITE_DB_PATH, SQL_MAX_ROWS_LIMIT

PALABRAS_SQL_PROHIBIDAS = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|ATTACH|DETACH|REPLACE|TRUNCATE|PRAGMA)\b",
    re.IGNORECASE,
)


def guardar_en_sqlite(df: pd.DataFrame, db_path: Path = SQLITE_DB_PATH) -> int:
    """Guarda el DataFrame limpio en la tabla `contratos` y crea índices de consulta."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        df.to_sql("contratos", conn, if_exists="replace", index=False)
        cursor = conn.cursor()
        for col in [
            "departamento",
            "modalidad_de_contratacion",
            "tipo_de_contrato",
            "fecha_de_firma",
            "nombre_entidad",
        ]:
            if col in df.columns:
                cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_contratos_{col} ON contratos ({col});")
        conn.commit()
        total = cursor.execute("SELECT COUNT(*) FROM contratos;").fetchone()[0]
    return int(total)


def validar_sql_solo_lectura(sql_query: str, max_rows: int = SQL_MAX_ROWS_LIMIT) -> str:
    """
    Verifica que la consulta sea únicamente una sentencia SELECT sin comandos de modificación
    y garantiza que incluya una cláusula LIMIT segura (RF-8 y Sección 6.2).
    """
    limpia = sql_query.strip().rstrip(";")

    if ";" in limpia:
        raise ValueError("Solo se permite ejecutar una única sentencia SQL por consulta.")

    if not limpia.upper().startswith("SELECT"):
        raise ValueError("Operación bloqueada: solo se permiten consultas SELECT de lectura.")

    if PALABRAS_SQL_PROHIBIDAS.search(limpia):
        raise ValueError("Operación bloqueada: la consulta contiene palabras reservadas no permitidas.")

    if not re.search(r"\bLIMIT\s+\d+\b", limpia, re.IGNORECASE):
        limpia = f"{limpia} LIMIT {max_rows}"

    return limpia


def ejecutar_consulta_segura(sql_query: str, db_path: Path = SQLITE_DB_PATH) -> tuple[pd.DataFrame, str]:
    """Ejecuta una consulta SQL validada abriendo SQLite en modo solo lectura (`mode=ro`)."""
    sql_seguro = validar_sql_solo_lectura(sql_query)
    uri = f"file:{db_path.as_posix()}?mode=ro"
    with sqlite3.connect(uri, uri=True) as conn:
        df_res = pd.read_sql_query(sql_seguro, conn)
    return df_res, sql_seguro

