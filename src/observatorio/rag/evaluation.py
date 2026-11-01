"""Módulo de evaluación cuantitativa y cualitativa del Asistente Híbrido.

Provee el banco de preguntas de validación (normativas, cuantitativas, coloquiales,
mixtas y fuera de alcance), la ejecución automatizada y el cálculo de métricas:
- Precisión de clasificación de intención (SQL vs RAG vs Mixta vs Fuera de alcance).
- Acierto Top-1 y Top-3 de recuperación documental.
- Tiempo de respuesta (latencia en segundos).
- Verificación de ausencia de alucinaciones en preguntas trampa.
"""

from __future__ import annotations

import time
from typing import Any
import pandas as pd

from observatorio.rag.assistant import AsistenteHibrido, RespuestaAsistente


# Banco estructurado de 12 preguntas de prueba con su comportamiento esperado
BANCO_PREGUNTAS_EVALUACION: list[dict[str, Any]] = [
    # 1. Normativas directas
    {
        "id": "EVAL-01",
        "categoria": "normativa_directa",
        "pregunta": "¿Qué inhabilidades existen para contratar con el Estado según la Ley 80 de 1993?",
        "tipo_esperado": "normativa",
        "fuente_esperada": "Ley 80 de 1993",
        "terminos_clave": ["inhabilidad", "incompatibilidad", "servidor público"],
    },
    {
        "id": "EVAL-02",
        "categoria": "normativa_directa",
        "pregunta": "¿Cuáles son las causales de contratación directa según la Ley 1150 de 2007?",
        "tipo_esperado": "normativa",
        "fuente_esperada": "Ley 1150 de 2007",
        "terminos_clave": ["urgencia manifiesta", "empréstito", "prestación de servicios"],
    },
    {
        "id": "EVAL-03",
        "categoria": "normativa_directa",
        "pregunta": "¿Cómo se define la capacidad residual en contratos de obra pública según el Decreto 1082?",
        "tipo_esperado": "normativa",
        "fuente_esperada": "Decreto 1082 de 2015",
        "terminos_clave": ["capacidad residual", "k de contratación", "experiencia"],
    },
    # 2. Normativas coloquiales
    {
        "id": "EVAL-04",
        "categoria": "normativa_coloquial",
        "pregunta": "Si soy servidor público, ¿puedo ganarme un contrato con la alcaldía de mi pueblo?",
        "tipo_esperado": "normativa",
        "fuente_esperada": "Ley 80 de 1993",
        "terminos_clave": ["inhabilidad", "prohibición", "servidor"],
    },
    {
        "id": "EVAL-05",
        "categoria": "normativa_coloquial",
        "pregunta": "¿Hasta cuánta plata se puede contratar a dedo o por mínima cuantía?",
        "tipo_esperado": "normativa",
        "fuente_esperada": "MANUAL DE LA MODALIDAD DE SELECCIÓN DE MÍNIMA CUANTÍA",
        "terminos_clave": ["mínima cuantía", "presupuesto", "salarios"],
    },
    # 3. Cuantitativas puras (SQL sobre SECOP II)
    {
        "id": "EVAL-06",
        "categoria": "cuantitativa_sql",
        "pregunta": "¿Cuáles son las 5 entidades públicas con mayor valor contratado en el departamento?",
        "tipo_esperado": "cuantitativa",
        "fuente_esperada": "contratos (SQLite)",
        "terminos_clave": ["nombre_entidad", "valor_total", "total_contratos"],
    },
    {
        "id": "EVAL-07",
        "categoria": "cuantitativa_sql",
        "pregunta": "¿Cuántos contratos se adjudicaron por modalidad de contratación directa y cuál es su cuantía total?",
        "tipo_esperado": "cuantitativa",
        "fuente_esperada": "contratos (SQLite)",
        "terminos_clave": ["directa", "total_contratos", "valor_total"],
    },
    {
        "id": "EVAL-08",
        "categoria": "cuantitativa_sql",
        "pregunta": "¿Cuántos contratos tuvieron prórrogas o días adicionados y cuál es el promedio de días?",
        "tipo_esperado": "cuantitativa",
        "fuente_esperada": "contratos (SQLite)",
        "terminos_clave": ["dias_adicionados", "promedio_dias", "total_con_adiciones"],
    },
    # 4. Consultas mixtas (Cifras reales contrastadas con el marco legal)
    {
        "id": "EVAL-09",
        "categoria": "mixta",
        "pregunta": "¿Cuántos contratos fueron por contratación directa y qué causales de la ley justifican esta modalidad?",
        "tipo_esperado": "mixta",
        "fuente_esperada": "contratos (SQLite) + Ley 1150 de 2007",
        "terminos_clave": ["total_contratos_directa", "causal", "ley 1150"],
    },
    {
        "id": "EVAL-10",
        "categoria": "mixta",
        "pregunta": "¿Qué porcentaje de contratos se dieron a PYMES y qué dice la regulación para incentivar su participación?",
        "tipo_esperado": "mixta",
        "fuente_esperada": "contratos (SQLite) + Decreto 1082 de 2015",
        "terminos_clave": ["es_pyme", "mipymes", "puntaje adicional"],
    },
    # 5. Consultas trampa / Fuera de alcance (Control estricto de alucinaciones)
    {
        "id": "EVAL-11",
        "categoria": "fuera_de_alcance",
        "pregunta": "¿Cuál es la receta tradicional para preparar una torta de chocolate esponjosa?",
        "tipo_esperado": "fuera_de_alcance",
        "fuente_esperada": "Ninguna (Rechazo formal por dominio)",
        "terminos_clave": ["fuera de alcance", "observatorio", "contratación estatal"],
    },
    {
        "id": "EVAL-12",
        "categoria": "fuera_de_alcance",
        "pregunta": "¿Quién ganó el último partido del mundial de fútbol y cuántos goles anotaron?",
        "tipo_esperado": "fuera_de_alcance",
        "fuente_esperada": "Ninguna (Rechazo formal por dominio)",
        "terminos_clave": ["fuera de alcance", "observatorio"],
    },
]


def evaluar_asistente(
    asistente: AsistenteHibrido,
    banco: list[dict[str, Any]] = BANCO_PREGUNTAS_EVALUACION,
    top_k: int = 3,
) -> pd.DataFrame:
    """
    Ejecuta el banco de pruebas sobre el asistente y recopila métricas operativas por pregunta.
    """
    filas = []

    for item in banco:
        p_id = item["id"]
        pregunta = item["pregunta"]
        categoria = item["categoria"]
        tipo_esp = item["tipo_esperado"]
        fuente_esp = item["fuente_esperada"]

        # Ejecución
        t0 = time.perf_counter()
        respuesta: RespuestaAsistente = asistente.responder(pregunta, top_k=top_k)
        latencia = round(time.perf_counter() - t0, 3)

        tipo_obt = respuesta.tipo_consulta
        acierto_tipo = tipo_obt == tipo_esp

        # Auditoría de fuentes normativas
        fuentes_nom = [f.get("documento", "") for f in respuesta.fuentes_normativas]
        top1_match = False
        top3_match = False
        score_max = 0.0

        if respuesta.fuentes_normativas:
            score_max = round(respuesta.fuentes_normativas[0].get("score_coseno", 0.0), 4)
            # Normalizar nombres para comparación flexible
            fuente_norm = fuente_esp.lower()
            if any(term in fuentes_nom[0].lower() for term in fuente_norm.split("+")[0].split()):
                top1_match = True
            for fn in fuentes_nom[:top_k]:
                if any(term in fn.lower() for term in fuente_norm.split("+")[0].split()):
                    top3_match = True
                    break

        if tipo_esp == "cuantitativa":
            acierto_fuente = respuesta.sql_ejecutado is not None and len(respuesta.sql_ejecutado) > 5
        elif tipo_esp == "fuera_de_alcance":
            acierto_fuente = tipo_obt == "fuera_de_alcance"
        elif tipo_esp == "mixta":
            acierto_fuente = (respuesta.sql_ejecutado is not None) and len(respuesta.fuentes_normativas) > 0
        else:
            acierto_fuente = top3_match

        snippet = (respuesta.respuesta[:140] + "...") if len(respuesta.respuesta) > 140 else respuesta.respuesta

        filas.append(
            {
                "id": p_id,
                "categoria": categoria,
                "pregunta": pregunta,
                "tipo_esperado": tipo_esp,
                "tipo_obtenido": tipo_obt,
                "acierto_tipo": acierto_tipo,
                "acierto_fuente": acierto_fuente,
                "score_max": score_max,
                "latencia_s": latencia,
                "sql_ejecutado": respuesta.sql_ejecutado or "N/A",
                "fuentes_doc": ", ".join(set(fuentes_nom)) if fuentes_nom else "N/A",
                "respuesta_resumen": snippet.replace("\n", " "),
            }
        )

    return pd.DataFrame(filas)


def calcular_metricas_resumen(df_eval: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula las métricas agregadas consolidadas de rendimiento del asistente:
    - Precisión de clasificación de intención (Router accuracy).
    - Tasa de recuperación de fuentes correctas (Retrieval accuracy).
    - Robustez contra alucinaciones (Control en preguntas fuera de alcance).
    - Latencia promedio y máxima.
    """
    total = len(df_eval)
    acc_tipo = df_eval["acierto_tipo"].mean() * 100
    acc_fuente = df_eval["acierto_fuente"].mean() * 100

    df_fuera = df_eval[df_eval["categoria"] == "fuera_de_alcance"]
    tasa_rechazo = (df_fuera["acierto_tipo"].mean() * 100) if not df_fuera.empty else 100.0

    lat_prom = df_eval["latencia_s"].mean()
    lat_p95 = df_eval["latencia_s"].quantile(0.95)

    resumen = [
        {"Métrica": "Total de preguntas evaluadas", "Valor": f"{total}"},
        {"Métrica": "Precisión Clasificación de Intención (Router)", "Valor": f"{acc_tipo:.1f}%"},
        {"Métrica": "Tasa de Acierto en Fuentes / SQL", "Valor": f"{acc_fuente:.1f}%"},
        {"Métrica": "Control de Alucinación (Rechazo Fuera de Alcance)", "Valor": f"{tasa_rechazo:.1f}%"},
        {"Métrica": "Latencia Promedio", "Valor": f"{lat_prom:.3f} s"},
        {"Métrica": "Latencia Percentil 95 (P95)", "Valor": f"{lat_p95:.3f} s"},
    ]
    return pd.DataFrame(resumen)


def ejecutar_evaluacion_completa(asistente: AsistenteHibrido) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Ejecuta el protocolo de validación completo y retorna (detalle, resumen)."""
    df_detalle = evaluar_asistente(asistente)
    df_resumen = calcular_metricas_resumen(df_detalle)
    return df_detalle, df_resumen

