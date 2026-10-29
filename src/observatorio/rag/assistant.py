"""Orquestador híbrido RAG (Qdrant Cloud) + SQL (SQLite solo lectura) (RF-6, RF-8, RF-9)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class RespuestaAsistente:
    """Estructura estándar de respuesta del asistente con trazabilidad de fuentes."""

    respuesta: str
    sql_ejecutado: str | None = None
    fuentes_normativas: list[dict[str, Any]] = field(default_factory=list)
    latencia_segundos: float = 0.0

