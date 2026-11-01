"""Pruebas unitarias para el Asistente Híbrido RAG + SQL (RF-6, RF-8, RF-9)."""

import pytest
from observatorio.rag.assistant import AsistenteHibrido, RespuestaAsistente


def test_clasificacion_consultas() -> None:
    # No instanciamos Qdrant en este test; solo probamos la lógica de enrutamiento
    asistente = AsistenteHibrido.__new__(AsistenteHibrido)
    asistente.PATRONES_SQL = AsistenteHibrido.PATRONES_SQL
    asistente.PATRONES_RAG = AsistenteHibrido.PATRONES_RAG
    asistente.PATRONES_DOMINIO = AsistenteHibrido.PATRONES_DOMINIO
    asistente.PATRONES_FUERA_ALCANCE = AsistenteHibrido.PATRONES_FUERA_ALCANCE

    # Cuantitativa
    assert asistente.clasificar_consulta("¿Cuáles son las 5 entidades con mayor cuantía contratada?") == "cuantitativa"
    assert asistente.clasificar_consulta("¿Cuántos contratos tuvieron prórrogas o días adicionados?") == "cuantitativa"

    # Normativa
    assert asistente.clasificar_consulta("¿Qué dice la Ley 80 sobre la liquidación de contratos?") == "normativa"
    assert asistente.clasificar_consulta("¿Qué causales de selección abreviada prevé el Decreto 1082?") == "normativa"

    # Mixta
    assert asistente.clasificar_consulta("¿Cuántos contratos fueron por contratación directa y qué causal de la ley aplica?") == "mixta"

    # Fuera de alcance
    assert asistente.clasificar_consulta("¿Cómo preparar una torta de chocolate?") == "fuera_de_alcance"
    assert asistente.clasificar_consulta("¿Quién ganó el partido de fútbol?") == "fuera_de_alcance"
    assert asistente.clasificar_consulta("Dame la receta para cocinar pasta carbonara") == "fuera_de_alcance"


def test_generacion_sql_local_segura() -> None:
    asistente = AsistenteHibrido.__new__(AsistenteHibrido)

    sql_entidades = asistente.generar_sql_local("¿Cuáles son las entidades con mayor valor contratado?")
    assert sql_entidades.upper().startswith("SELECT")
    assert "FROM contratos" in sql_entidades
    assert "ORDER BY valor_total DESC" in sql_entidades

    sql_directa = asistente.generar_sql_local("¿Cuántos contratos por contratación directa existen?")
    assert "DIRECTA" in sql_directa.upper()

    sql_adiciones = asistente.generar_sql_local("¿Cuántos contratos tienen prórroga o días adicionados?")
    assert "dias_adicionados > 0" in sql_adiciones


def test_banco_preguntas_y_metricas_resumen() -> None:
    from observatorio.rag.evaluation import BANCO_PREGUNTAS_EVALUACION, calcular_metricas_resumen
    import pandas as pd

    assert len(BANCO_PREGUNTAS_EVALUACION) >= 10

    # Simular evaluación rápida
    df_dummy = pd.DataFrame([
        {
            "id": "EVAL-01",
            "categoria": "normativa_directa",
            "pregunta": "¿Qué inhabilidades existen?",
            "tipo_esperado": "normativa",
            "tipo_obtenido": "normativa",
            "acierto_tipo": True,
            "acierto_fuente": True,
            "score_max": 0.75,
            "latencia_s": 0.12,
            "sql_ejecutado": "N/A",
            "fuentes_doc": "Ley 80 de 1993",
            "respuesta_resumen": "Respuesta resumen",
        },
        {
            "id": "EVAL-11",
            "categoria": "fuera_de_alcance",
            "pregunta": "¿Cómo hacer torta?",
            "tipo_esperado": "fuera_de_alcance",
            "tipo_obtenido": "fuera_de_alcance",
            "acierto_tipo": True,
            "acierto_fuente": True,
            "score_max": 0.0,
            "latencia_s": 0.01,
            "sql_ejecutado": "N/A",
            "fuentes_doc": "N/A",
            "respuesta_resumen": "Fuera de alcance",
        },
    ])
    resumen = calcular_metricas_resumen(df_dummy)
    assert not resumen.empty
    assert "Métrica" in resumen.columns
    assert "Valor" in resumen.columns


