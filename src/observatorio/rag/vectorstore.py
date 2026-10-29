"""Vectorización con Gemini Embedding 2 (prefijos oficiales) y gestión de Qdrant Cloud (RF-1, RF-5, RF-6)."""

from __future__ import annotations

from observatorio.config import (
    EMBEDDING_DIMENSION,
    QDRANT_COLLECTION_NAME,
)


def formatear_texto_documento_embedding(documento: str, articulo: str, texto: str) -> str:
    """
    Aplica el prefijo requerido por `gemini-embedding-2` para documentos (Sección 4.4):
    `title: <documento - artículo> | text: <contenido>`
    """
    titulo = f"{documento} - {articulo}".strip(" -")
    return f"title: {titulo} | text: {texto}"


def formatear_query_embedding(pregunta: str) -> str:
    """
    Aplica el prefijo requerido por `gemini-embedding-2` para consultas (Sección 4.4):
    `task: search result | query: <pregunta>`
    """
    return f"task: search result | query: {pregunta}"


__all__ = [
    "EMBEDDING_DIMENSION",
    "QDRANT_COLLECTION_NAME",
    "formatear_texto_documento_embedding",
    "formatear_query_embedding",
]

