"""Fragmentación del corpus normativo por artículo y evaluación de tamaños (RF-3, RF-4)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter


@dataclass
class FragmentoNormativo:
    """Representa un fragmento de normativa con sus metadatos verificables."""

    texto: str
    documento: str
    tipo_fuente: str
    tema: str
    fecha: str
    articulo: str


def fragmentar_documento(
    texto: str,
    metadatos_base: dict[str, str],
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
) -> list[dict[str, Any]]:
    """
    Fragmenta un documento normativo con `RecursiveCharacterTextSplitter`
    evitando cortes a mitad de palabra (RF-4).
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n## ", "\n### ", "\nArtículo ", "\nARTÍCULO ", "\n\n", "\n", " "],
        keep_separator=True,
    )
    textos = splitter.split_text(texto)
    fragmentos: list[dict[str, Any]] = []
    for idx, frag in enumerate(textos):
        fragmentos.append(
            {
                "chunk_id": idx,
                "texto": frag.strip(),
                "longitud_caracteres": len(frag.strip()),
                **metadatos_base,
            }
        )
    return fragmentos


def comparar_configuraciones_chunking(
    corpus: list[tuple[str, dict[str, str]]],
    configuraciones: list[tuple[int, int]] | None = None,
) -> pd.DataFrame:
    """
    Compara al menos tres tamaños de chunking y devuelve una tabla con número de fragmentos,
    longitud media, mínima y máxima (RF-4).
    """
    if configuraciones is None:
        configuraciones = [(600, 100), (1000, 150), (1600, 250)]

    filas = []
    for chunk_size, chunk_overlap in configuraciones:
        todos: list[dict[str, Any]] = []
        for texto, meta in corpus:
            todos.extend(fragmentar_documento(texto, meta, chunk_size, chunk_overlap))
        longitudes = [f["longitud_caracteres"] for f in todos]
        filas.append(
            {
                "chunk_size": chunk_size,
                "chunk_overlap": chunk_overlap,
                "num_fragmentos": len(longitudes),
                "longitud_media": round(sum(longitudes) / max(len(longitudes), 1), 1),
                "longitud_minima": min(longitudes) if longitudes else 0,
                "longitud_maxima": max(longitudes) if longitudes else 0,
            }
        )
    return pd.DataFrame(filas)

