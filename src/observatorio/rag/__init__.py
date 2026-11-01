"""Subpaquete RAG para procesamiento normativo, Qdrant Cloud y asistente híbrido."""

from observatorio.rag.assistant import AsistenteHibrido, RespuestaAsistente
from observatorio.rag.evaluation import (
    BANCO_PREGUNTAS_EVALUACION,
    calcular_metricas_resumen,
    ejecutar_evaluacion_completa,
    evaluar_asistente,
)
from observatorio.rag.vectorstore import IndexadorQdrant

__all__ = [
    "AsistenteHibrido",
    "RespuestaAsistente",
    "IndexadorQdrant",
    "BANCO_PREGUNTAS_EVALUACION",
    "evaluar_asistente",
    "calcular_metricas_resumen",
    "ejecutar_evaluacion_completa",
]
