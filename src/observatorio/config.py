"""Configuración centralizada, rutas del proyecto y variables de entorno."""

from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

# Raíz del repositorio (2 niveles arriba de src/observatorio/config.py)
PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]

# Cargar variables de entorno desde .env si existe
load_dotenv(PROJECT_ROOT / ".env")

# Semilla global de reproducibilidad (RF-ML / RNF)
RANDOM_SEED: int = 42

# Directorios de datos y modelos
DATA_DIR: Path = PROJECT_ROOT / "data"
CORPUS_DIR: Path = DATA_DIR / "corpus_normativo"
RAW_DATA_DIR: Path = DATA_DIR / "raw"
PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
EVALUATION_DIR: Path = DATA_DIR / "evaluation"
MODELS_DIR: Path = PROJECT_ROOT / "models"

# Archivos principales
SQLITE_DB_PATH: Path = PROCESSED_DATA_DIR / "secop_contratos.sqlite"
MODEL_ARTIFACT_PATH: Path = MODELS_DIR / "pipeline_prorrogas.joblib"
MODEL_METADATA_PATH: Path = MODELS_DIR / "model_metadata.json"

# Parámetros Socrata / SECOP II
SOCRATA_DATASET_ID: str = os.getenv("SOCRATA_DATASET_ID", "jbjy-vk9h")
SOCRATA_APP_TOKEN: str | None = os.getenv("SOCRATA_APP_TOKEN") or None
SECOP_DEPARTAMENTO: str = os.getenv("SECOP_DEPARTAMENTO", "Valle del Cauca")
SECOP_FECHA_INICIO: str = os.getenv("SECOP_FECHA_INICIO", "2023-01-01T00:00:00")
SECOP_FECHA_FIN: str = os.getenv("SECOP_FECHA_FIN", "2026-10-31T23:59:59")

# Parámetros Qdrant Cloud y Gemini
QDRANT_URL: str | None = os.getenv("QDRANT_URL")
QDRANT_API_KEY: str | None = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME: str = os.getenv("QDRANT_COLLECTION_NAME", "normativa_contratacion")

GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
GEMINI_EMBEDDING_MODEL: str = os.getenv("GEMINI_EMBEDDING_MODEL", "models/gemini-embedding-exp-03-07")
GEMINI_LLM_MODEL: str = os.getenv("GEMINI_LLM_MODEL", "gemini-2.5-flash")
EMBEDDING_DIMENSION: int = 768

# Límites de seguridad para consultas y demo pública
MAX_QUERIES_PER_SESSION: int = int(os.getenv("MAX_QUERIES_PER_SESSION", "15"))
SQL_MAX_ROWS_LIMIT: int = int(os.getenv("SQL_MAX_ROWS_LIMIT", "100"))
