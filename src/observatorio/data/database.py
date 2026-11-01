"""Módulo de persistencia local en SQLite y motor de ejecución de consultas SQL de solo lectura.

Implementa mecanismos de seguridad activa para evitar inyección SQL, bloquea sentencias destructivas
(DDL/DML) y fuerza la apertura de conexiones en modo estrictamente de solo lectura (`mode=ro`).
"""

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
    """
    Persiste el conjunto de datos limpio en una base de datos relacional SQLite y genera índices.

    Qué hace:
        Guarda los registros tabulares en la tabla `contratos` y genera índices sobre columnas
        frecuentemente consultadas para optimizar el tiempo de respuesta.

    Cómo lo hace:
        1. Crea el directorio padre si no existe y conecta a la base de datos SQLite en modo lectura/escritura.
        2. Vuelca el DataFrame reemplazando la tabla existente (`to_sql` con `if_exists="replace"`).
        3. Ejecuta sentencias `CREATE INDEX IF NOT EXISTS` sobre `departamento`, `modalidad_de_contratacion`,
           `tipo_de_contrato`, `fecha_de_firma` y `nombre_entidad`.
        4. Confirma la transacción y cuenta el total de registros insertados.

    Args:
        df: DataFrame de contratos depurado.
        db_path: Ruta del archivo SQLite de destino.

    Returns:
        Número total de registros confirmados en la tabla.
    """
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
    Audita y restringe una consulta SQL para garantizar que sea de solo lectura y segura.

    Qué hace:
        Verifica que la sentencia comience por `SELECT`, prohíbe sentencias múltiples o destructivas
        (DROP, DELETE, UPDATE, etc.) y limita el número máximo de filas devueltas.

    Cómo lo hace:
        1. Limpia espacios en blanco y punto y coma final.
        2. Rechaza consultas encadenadas que contengan `;`.
        3. Verifica que la primera palabra reservada sea `SELECT`.
        4. Evalúa una expresión regular de palabras prohibidas de modificación y DDL.
        5. Inyecta una cláusula `LIMIT <max_rows>` si el usuario no incluyó un límite explícito.

    Args:
        sql_query: Cadena con la consulta SQL generada o enviada.
        max_rows: Límite superior de filas permitido.

    Returns:
        Sentencia SQL depurada y segura lista para ejecución.

    Raises:
        ValueError: Si la consulta no inicia con SELECT o contiene comandos prohibidos.
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
    """
    Ejecuta una consulta SQL segura abriendo la base de datos exclusivamente en modo lectura.

    Qué hace:
        Valida la consulta mediante `validar_sql_solo_lectura` y la ejecuta contra la base de datos
        utilizando el parámetro URI `?mode=ro`, que previene cualquier mutación a nivel del motor.

    Cómo lo hace:
        1. Valida y sanitiza la consulta SQL.
        2. Abre una conexión SQLite mediante URI estándar `file:<path>?mode=ro`.
        3. Carga el conjunto de resultados directamente en un DataFrame de pandas.

    Args:
        sql_query: Consulta SQL a ejecutar.
        db_path: Ruta a la base de datos SQLite.

    Returns:
        Tupla con el DataFrame de resultados y la consulta SQL efectivamente ejecutada.
    """
    sql_seguro = validar_sql_solo_lectura(sql_query)
    uri = f"file:{db_path.as_posix()}?mode=ro"
    with sqlite3.connect(uri, uri=True) as conn:
        df_res = pd.read_sql_query(sql_seguro, conn)
    return df_res, sql_seguro

