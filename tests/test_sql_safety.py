"""Pruebas para garantizar que el ejecutor SQL rechace modificaciones e inyecciones (RF-8, Sección 6.2)."""

import pytest
from observatorio.data.database import validar_sql_solo_lectura


def test_select_simple_agrega_limit() -> None:
    sql = "SELECT id_contrato, valor_del_contrato FROM contratos"
    resultado = validar_sql_solo_lectura(sql, max_rows=50)
    assert resultado == "SELECT id_contrato, valor_del_contrato FROM contratos LIMIT 50"


def test_bloquea_drop_y_delete() -> None:
    with pytest.raises(ValueError):
        validar_sql_solo_lectura("DROP TABLE contratos")

    with pytest.raises(ValueError):
        validar_sql_solo_lectura("SELECT * FROM contratos; DELETE FROM contratos")

