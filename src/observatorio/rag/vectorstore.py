"""Módulo de indexación vectorial y búsqueda semántica sobre la base de conocimiento normativo.

Administra la colección en Qdrant (Cloud y local), la vectorización por lotes con respaldo
incremental en Parquet y la búsqueda por similitud coseno con filtrado por metadatos.
Soporta embeddings de Google Gemini y ejecución autónoma con modelos locales de SentenceTransformers.
"""

from __future__ import annotations

import logging
import os
import re
import time
from pathlib import Path
from typing import Any

import pandas as pd
from dotenv import load_dotenv
from google import genai
from google.genai import types
from qdrant_client import QdrantClient

logger = logging.getLogger(__name__)
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PayloadSchemaType,
    PointStruct,
    VectorParams,
)

from observatorio.config import (
    EMBEDDING_DIMENSION,
    EMBEDDINGS_BACKUP_PATH,
    GEMINI_API_KEY,
    GEMINI_EMBEDDING_MODEL,
    MAX_REINTENTOS,
    MODELO_EMBEDDING_LOCAL,
    PROJECT_ROOT,
    QDRANT_API_KEY,
    QDRANT_COLLECTION_NAME,
    QDRANT_URL,
    USAR_EMBEDDINGS_LOCAL,
)


def formatear_texto_documento_embedding(
    documento: str, articulo: str, texto: str
) -> str:
    """
    Aplica el prefijo requerido para documentos normativos (Sección 4.4):
    `title: <documento - artículo> | text: <contenido>`
    """
    titulo = f"{documento} - {articulo}".strip(" -")
    return f"title: {titulo} | text: {texto}"


def formatear_query_embedding(pregunta: str) -> str:
    """
    Aplica el prefijo requerido para consultas de búsqueda (Sección 4.4):
    `task: search result | query: <pregunta>`
    """
    return f"task: search result | query: {pregunta}"


class IndexadorQdrant:
    """
    Gestiona el ciclo de vida de la base vectorial de normas y la recuperación Top-k.

    Qué hace:
        Crea colecciones vectoriales con distancia coseno, calcula embeddings para fragmentos jurídicos,
        los respalda incrementalmente en Parquet, realiza upsert en Qdrant y ejecuta búsquedas semánticas.

    Cómo lo hace:
        1. Inicializa el cliente Qdrant (Cloud con token o conexión de respaldo local).
        2. Configura el proveedor de embeddings (Gemini API o SentenceTransformers local según configuración/cuota).
        3. Realiza vectorización en lotes gestionando reintentos con backoff exponencial.
        4. Inserta puntos con payload indexado (`documento`, `articulo`, `tipo_fuente`) para soportar filtros exactos.
    """

    # Caché estática a nivel de clase para que no se descargue ni recargue en memoria
    # si se crean múltiples instancias de IndexadorQdrant
    _MODELOS_LOCALES_CACHE: dict[str, Any] = {}

    def __init__(
        self,
        qdrant_url: str | None = None,
        qdrant_api_key: str | None = None,
        collection_name: str | None = None,
        gemini_api_key: str | None = None,
        embedding_model: str | None = None,
        usar_local: bool | None = None,
        modelo_local_nombre: str | None = None,
        max_intentos_cuota: int = 2,
    ) -> None:
        # Recargar siempre el .env fresco por si el usuario lo modificó en disco
        load_dotenv(PROJECT_ROOT / ".env", override=True)

        url = qdrant_url or os.getenv("QDRANT_URL")
        key = qdrant_api_key or os.getenv("QDRANT_API_KEY")
        gkey = gemini_api_key or os.getenv("GEMINI_API_KEY")
        coll = collection_name or os.getenv("QDRANT_COLLECTION_NAME", "normativa_contratacion")
        model = embedding_model or os.getenv("GEMINI_EMBEDDING_MODEL", "models/gemini-embedding-001")

        # Limpiar comillas, barras o espacios accidentales
        url = url.strip().strip("'\"").rstrip("/") if url else ""
        key = key.strip().strip("'\"") if key else ""
        gkey = (gkey or "").strip().strip("'\"")

        self.collection_name = coll
        self.embedding_dimension = EMBEDDING_DIMENSION
        self.embedding_model = (
            "models/gemini-embedding-001"
            if "gemini-embedding-exp" in model
            else model
        )

        # Configuración de modo local
        if usar_local is None:
            self.usar_local = USAR_EMBEDDINGS_LOCAL
        else:
            self.usar_local = usar_local

        # Si no hay credenciales Qdrant, forzar modo local automáticamente
        if not url or not key:
            if not self.usar_local:
                print("⚠️ Faltan QDRANT_URL o QDRANT_API_KEY. Activando modo 100% local (Parquet + sentence-transformers).")
            self.usar_local = True

        self.modelo_local_nombre = (
            modelo_local_nombre or MODELO_EMBEDDING_LOCAL or "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
        )
        self.max_intentos_cuota = max_intentos_cuota
        self._modelo_local = None

        print(f"🔍 Inicializando IndexadorQdrant en colección '{self.collection_name}'.")
        if url:
            print(f"   Qdrant URL: {url}")
        print(f"   Modo inicial de embeddings: {'LOCAL (' + self.modelo_local_nombre + ')' if self.usar_local else 'NUBE (Gemini: ' + self.embedding_model + ' con fallback a local)'}")

        self.client = QdrantClient(url=url, api_key=key, timeout=60) if (url and key) else None
        self.ai_client = genai.Client(api_key=gkey) if gkey else None
        self.backup_path: Path = Path(EMBEDDINGS_BACKUP_PATH)
        self._df_parquet_cache: pd.DataFrame | None = None
        self._crear_coleccion_si_no_existe()

    def _obtener_modelo_local(self) -> Any:
        """
        Carga o descarga el modelo de `sentence-transformers` una única vez (lazy loading).
        Si ya fue descargado previamente por esta o cualquier otra instancia, reutiliza la caché.
        """
        if self._modelo_local is not None:
            return self._modelo_local

        if self.modelo_local_nombre in IndexadorQdrant._MODELOS_LOCALES_CACHE:
            self._modelo_local = IndexadorQdrant._MODELOS_LOCALES_CACHE[self.modelo_local_nombre]
            return self._modelo_local

        print(f"📦 Descargando/cargando modelo local '{self.modelo_local_nombre}'...")
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise ImportError(
                "Para utilizar embeddings locales necesitas tener instalada la librería 'sentence-transformers'.\n"
                "Instálala ejecutando: pip install sentence-transformers"
            ) from exc

        try:
            modelo = SentenceTransformer(self.modelo_local_nombre, local_files_only=True)
        except Exception:
            modelo = SentenceTransformer(self.modelo_local_nombre)
        IndexadorQdrant._MODELOS_LOCALES_CACHE[self.modelo_local_nombre] = modelo
        self._modelo_local = modelo
        print(f"✅ Modelo local '{self.modelo_local_nombre}' listo en memoria.")
        return self._modelo_local

    def _crear_coleccion_si_no_existe(self) -> None:
        """
        Verifica y crea la colección en Qdrant con distancia coseno y dimensión configurada,
        además del índice sobre el campo `documento` para filtrado estructurado.
        Maneja errores de conexión para permitir operación local offline si no hay red.
        """
        if self.client is None:
            print("ℹ️ Sin cliente Qdrant — operando exclusivamente sobre respaldo Parquet local.")
            return
        try:
            if not self.client.collection_exists(self.collection_name):
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.embedding_dimension,
                        distance=Distance.COSINE,
                    ),
                )
                print(
                    f"Colección '{self.collection_name}' verificada/creada en Qdrant ({self.embedding_dimension} dim, COSINE)."
                )
            else:
                print(
                    f"La colección '{self.collection_name}' ya se encuentra activa en Qdrant."
                )

            # Asegurar índice de payload sobre `documento` para soportar filtros estructurados
            try:
                self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="documento",
                    field_schema=PayloadSchemaType.KEYWORD,
                )
            except Exception:
                pass
        except Exception as e:
            print(
                f"⚠️ Advertencia al conectar con Qdrant Cloud ({type(e).__name__}). "
                "Si estás sin conexión a internet o en modo local, las búsquedas vectoriales "
                "se resolverán usando el respaldo local en Parquet."
            )

    def _generar_embeddings_lote_local(self, textos: list[str]) -> list[list[float]]:
        """
        Genera embeddings localmente usando el modelo de `sentence-transformers`.
        Ajusta la dimensión con zero-padding si el modelo local entrega una dimensión
        menor a la esperada por Qdrant (768).
        """
        modelo = self._obtener_modelo_local()
        vectores = modelo.encode(
            textos,
            show_progress_bar=False,
            normalize_embeddings=True,
        )

        vectores_lista: list[list[float]] = []
        for vec in vectores:
            v = vec.tolist() if hasattr(vec, "tolist") else list(vec)
            # Asegurar compatibilidad de dimensión con la colección de Qdrant (768)
            if len(v) < self.embedding_dimension:
                v = v + [0.0] * (self.embedding_dimension - len(v))
            elif len(v) > self.embedding_dimension:
                v = v[: self.embedding_dimension]
            vectores_lista.append(v)

        return vectores_lista

    def _generar_embeddings_lote(self, textos: list[str]) -> list[list[float]]:
        """
        Genera embeddings de dimensión `EMBEDDING_DIMENSION` (768) para un lote de textos.

        Comportamiento inteligente:
        - Si `self.usar_local` está activo: usa directamente el modelo local.
        - Si está en modo nube: intenta con Gemini. Si la cuota falla (429/RESOURCE_EXHAUSTED)
          o se agotan los reintentos, activa el fallback automático al modelo local para este
          lote y los siguientes.
        """
        # Si ya se activó el modo local (por bandera o por fallback previo)
        if self.usar_local:
            return self._generar_embeddings_lote_local(textos)

        # Intentar con la API de Gemini
        if self.ai_client is None:
            print("⚠️ No hay GEMINI_API_KEY configurada. Cambiando a modelo local...")
            self.usar_local = True
            return self._generar_embeddings_lote_local(textos)

        for intento in range(1, MAX_REINTENTOS + 1):
            try:
                embedding_response = self.ai_client.models.embed_content(
                    model=self.embedding_model,
                    contents=textos,
                    config=types.EmbedContentConfig(
                        output_dimensionality=self.embedding_dimension,
                    ),
                )
                if not embedding_response.embeddings:
                    raise RuntimeError("La API de Gemini devolvió una respuesta vacía de embeddings.")
                return [list(emb.values) for emb in embedding_response.embeddings]

            except Exception as e:
                msg = str(e)
                es_error_cuota = "429" in msg or "RESOURCE_EXHAUSTED" in msg

                if es_error_cuota:
                    match_seg = re.search(r"retry in ([0-9.]+)s", msg, re.IGNORECASE)
                    espera = int(float(match_seg.group(1))) + 5 if match_seg else 30

                    # Reintentar un número controlado de veces antes de conmutar a local
                    if intento < self.max_intentos_cuota:
                        print(
                            f"⏳ [Cuota Gemini Free Tier] Pausando {espera}s antes de reintentar "
                            f"(intento {intento}/{self.max_intentos_cuota})..."
                        )
                        time.sleep(espera)
                    else:
                        print(
                            f"\n⚠️ Se alcanzó el límite de reintentos por cuota en Gemini ({intento}/{self.max_intentos_cuota}).\n"
                            f"🔄 Conmutando AUTOMÁTICAMENTE a modelo local '{self.modelo_local_nombre}' para continuar sin pausas..."
                        )
                        self.usar_local = True
                        return self._generar_embeddings_lote_local(textos)
                else:
                    # En otros errores de API (ej. problema de red o permisos), hacer fallback también
                    print(
                        f"\n⚠️ Error al conectar con la API de Gemini: {e}.\n"
                        f"🔄 Activando FALLBACK automático a modelo local '{self.modelo_local_nombre}'..."
                    )
                    self.usar_local = True
                    return self._generar_embeddings_lote_local(textos)

        # Por seguridad, si el loop termina sin retornar
        self.usar_local = True
        return self._generar_embeddings_lote_local(textos)

    def _generate_embedding(self, texto: str) -> list[float]:
        """Genera un único vector de embedding (768 dim) para un texto o consulta."""
        return self._generar_embeddings_lote([texto])[0]

    def _realizar_respaldo_de_embedings(
        self,
        fragmentos: list[dict[str, Any]],
        ruta_respaldo: str | Path = EMBEDDINGS_BACKUP_PATH,
        batch_size: int = 80,
        forzar_recalculo: bool = False,
        usar_local: bool | None = None,
    ) -> pd.DataFrame:
        """
        Vectoriza los fragmentos por lotes respetando límites de tasa y guardando avance en Parquet.
        Si el archivo de respaldo ya existe en disco, retoma automáticamente desde el último lote procesado.
        """
        if usar_local is not None:
            self.usar_local = usar_local

        ruta = Path(ruta_respaldo)
        ruta.parent.mkdir(parents=True, exist_ok=True)

        # Preparar DataFrame base con el texto formateado para cada fragmento
        registros: list[dict[str, Any]] = []
        for idx, frag in enumerate(fragmentos):
            documento = str(frag.get("documento", "Documento Normativo"))
            articulo = str(frag.get("articulo", "Sección General"))
            texto = str(frag.get("texto", ""))
            registros.append(
                {
                    "point_id": idx,
                    "documento": documento,
                    "tipo_fuente": str(frag.get("tipo_fuente", "")),
                    "tema": str(frag.get("tema", "")),
                    "fecha": str(frag.get("fecha", "")),
                    "articulo": articulo,
                    "chunk_id": int(frag.get("chunk_id", idx)),
                    "longitud_caracteres": int(
                        frag.get("longitud_caracteres", len(texto))
                    ),
                    "texto": texto,
                    "texto_embedding": formatear_texto_documento_embedding(
                        documento, articulo, texto
                    ),
                }
            )
        df_actual = pd.DataFrame(registros)

        # Cargar vectores ya calculados previamente si existe respaldo en disco
        vectores_guardados: dict[str, list[float]] = {}
        if ruta.exists() and not forzar_recalculo:
            try:
                df_previo = pd.read_parquet(ruta)
                if (
                    "texto_embedding" in df_previo.columns
                    and "embedding" in df_previo.columns
                ):
                    for _, fila in df_previo.dropna(subset=["embedding"]).iterrows():
                        vec = fila["embedding"]
                        if hasattr(vec, "tolist"):
                            vec = vec.tolist()
                        if isinstance(vec, list) and len(vec) == self.embedding_dimension:
                            vectores_guardados[str(fila["texto_embedding"])] = vec
                    if vectores_guardados:
                        print(
                            f"📂 Respaldo local detectado: {len(vectores_guardados):,} vectores cargados desde {ruta.name}."
                        )
            except Exception as exc:
                print(
                    f"⚠️ No se pudo leer el respaldo previo ({exc}); se recalcularán los embeddings."
                )

        # Identificar qué fragmentos aún no tienen vector calculado
        pendientes_idx = [
            i
            for i, row in df_actual.iterrows()
            if row["texto_embedding"] not in vectores_guardados
        ]

        if not pendientes_idx:
            print(
                f"✅ Todos los {len(df_actual):,} fragmentos ya cuentan con embeddings en disco."
            )
            df_actual["embedding"] = df_actual["texto_embedding"].map(
                vectores_guardados
            )
            return df_actual

        proveedor = f"modelo local '{self.modelo_local_nombre}'" if self.usar_local else f"API Gemini '{self.embedding_model}'"
        print(
            f"🚀 Vectorizando {len(pendientes_idx):,} fragmentos pendientes usando {proveedor}..."
        )

        tamano_lote = min(batch_size, 80) if not self.usar_local else min(batch_size, 256)
        textos_en_ventana = 0
        inicio_ventana = time.monotonic()

        for pos in range(0, len(pendientes_idx), tamano_lote):
            indices_lote = pendientes_idx[pos : pos + tamano_lote]
            textos_lote = [
                str(df_actual.loc[idx, "texto_embedding"]) for idx in indices_lote
            ]

            # Control preventivo de cuota solo si estamos consumiendo la API de Gemini
            if not self.usar_local:
                transcurrido = time.monotonic() - inicio_ventana
                if textos_en_ventana + len(textos_lote) > 90 and transcurrido < 62.0:
                    espera = max(62.0 - transcurrido, 5.0)
                    print(
                        f"⏳ Pausa preventiva de cuota gratuita ({espera:.0f}s) | "
                        f"Avance: {pos:,}/{len(pendientes_idx):,} fragmentos..."
                    )
                    time.sleep(espera)
                    inicio_ventana = time.monotonic()
                    textos_en_ventana = 0

            vectores_lote = self._generar_embeddings_lote(textos_lote)
            for texto_emb, vector in zip(textos_lote, vectores_lote):
                vectores_guardados[texto_emb] = vector

            textos_en_ventana += len(textos_lote)

            # Guardar checkpoint incremental en disco tras cada lote
            df_actual["embedding"] = df_actual["texto_embedding"].map(
                vectores_guardados
            )
            df_actual.to_parquet(ruta, index=False)
            print(
                f"  ✔️ Lote completado: {min(pos + tamano_lote, len(pendientes_idx)):,}/{len(pendientes_idx):,} "
                f"(respaldo actualizado en {ruta.name})"
            )

        return df_actual

    def _realizar_upsert_a_qdrant(
        self,
        puntos: list[PointStruct],
        batch_size: int = 100,
    ) -> None:
        """Realiza inserción/actualización por lotes en Qdrant con reintentos y tolerancia a fallos."""
        if self.client is None:
            print("⚠️ Sin cliente Qdrant — upsert omitido (modo local).")
            return
        for i in range(0, len(puntos), batch_size):
            lote_puntos = puntos[i : i + batch_size]
            for intento in range(1, MAX_REINTENTOS + 1):
                try:
                    self.client.upsert(
                        collection_name=self.collection_name,
                        points=lote_puntos,
                        wait=True,
                    )
                    break
                except Exception as e:
                    if intento < MAX_REINTENTOS:
                        espera = 2**intento
                        print(
                            f"Error en upsert lote {i // batch_size + 1} (intento {intento}/{MAX_REINTENTOS}): {e}. Reintentando en {espera}s..."
                        )
                        time.sleep(espera)
                    else:
                        raise

    def indexar_fragmentos(
        self,
        fragmentos: list[dict[str, Any]],
        ruta_respaldo: str | Path = EMBEDDINGS_BACKUP_PATH,
        batch_size: int = 80,
        forzar_recalculo: bool = False,
        usar_local: bool | None = None,
    ) -> int:
        """
        Flujo consolidado de indexación vectorial:
        1. Genera los embeddings por lotes (vía Gemini API o modelo local) y persiste respaldo en Parquet.
        2. Construye las estructuras PointStruct con metadatos de documento, artículo y texto.
        3. Realiza la carga de puntos a Qdrant mediante upsert paginado.
        4. Verifica y retorna el total de puntos indexados.
        """
        df_emb = self._realizar_respaldo_de_embedings(
            fragmentos=fragmentos,
            ruta_respaldo=ruta_respaldo,
            batch_size=batch_size,
            forzar_recalculo=forzar_recalculo,
            usar_local=usar_local,
        )

        puntos: list[PointStruct] = []
        for _, fila in df_emb.iterrows():
            vector = fila["embedding"]
            if hasattr(vector, "tolist"):
                vector = vector.tolist()
            payload = {
                "documento": fila["documento"],
                "tipo_fuente": fila["tipo_fuente"],
                "tema": fila["tema"],
                "fecha": fila["fecha"],
                "articulo": fila["articulo"],
                "chunk_id": int(fila["chunk_id"]),
                "longitud_caracteres": int(fila["longitud_caracteres"]),
                "texto": fila["texto"],
            }
            puntos.append(
                PointStruct(
                    id=int(fila["point_id"]),
                    vector=vector,
                    payload=payload,
                )
            )

        print(
            f"☁️ Subiendo {len(puntos):,} puntos a Qdrant Cloud en colección '{self.collection_name}'..."
        )
        self._realizar_upsert_a_qdrant(puntos, batch_size=100)

        total_en_qdrant = self.contar_puntos()
        print(
            f"✅ Indexación finalizada: {total_en_qdrant:,} puntos activos en Qdrant Cloud."
        )
        return total_en_qdrant

    def contar_puntos(self) -> int:
        """Devuelve la cantidad exacta de puntos almacenados en la colección de Qdrant."""
        if self.client is None:
            return 0
        return int(
            self.client.count(collection_name=self.collection_name, exact=True).count
        )

    def _buscar_similares_en_parquet_local(
        self,
        vector_query: list[float],
        top_k: int = 5,
        filtro_documento: str | None = None,
    ) -> pd.DataFrame:
        """
        Búsqueda vectorial offline por similitud coseno directa sobre el archivo Parquet de respaldo.
        """
        if not self.backup_path.exists():
            return pd.DataFrame()

        if self._df_parquet_cache is None:
            self._df_parquet_cache = pd.read_parquet(self.backup_path)

        df = self._df_parquet_cache
        if filtro_documento:
            df = df[df["documento"] == filtro_documento]

        if df.empty or "embedding" not in df.columns:
            return pd.DataFrame()

        import numpy as np

        embeddings = np.array(df["embedding"].tolist(), dtype=np.float32)
        q_vec = np.array(vector_query, dtype=np.float32)

        q_norm = np.linalg.norm(q_vec)
        if q_norm > 0:
            q_vec = q_vec / q_norm

        emb_norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        emb_normed = embeddings / np.maximum(emb_norms, 1e-12)

        sims = (emb_normed @ q_vec).flatten()
        k = min(top_k, len(df))
        top_indices = np.argsort(sims)[-k:][::-1]

        filas: list[dict[str, Any]] = []
        for rank, idx in enumerate(top_indices, start=1):
            row = df.iloc[idx]
            filas.append(
                {
                    "rank": rank,
                    "score_coseno": round(float(sims[idx]), 4),
                    "documento": str(row.get("documento", "")),
                    "articulo": str(row.get("articulo", "")),
                    "tipo_fuente": str(row.get("tipo_fuente", "")),
                    "fecha": str(row.get("fecha", "")),
                    "texto": str(row.get("texto", "")),
                }
            )
        return pd.DataFrame(filas)

    def buscar_similares(
        self,
        pregunta: str,
        top_k: int = 5,
        filtro_documento: str | None = None,
        usar_local: bool | None = None,
    ) -> pd.DataFrame:
        """
        Calcula el vector de la pregunta, consulta los Top-k fragmentos más cercanos por similitud coseno
        con filtro opcional por documento normativo y devuelve un DataFrame con puntuación y texto.
        En caso de indisponibilidad de conexión remota, resuelve la búsqueda directamente sobre el respaldo local en Parquet.
        """
        if usar_local is not None:
            self.usar_local = usar_local

        query_formateada = formatear_query_embedding(pregunta)
        vector_query = self._generate_embedding(query_formateada)

        filtro_qdrant = None
        if filtro_documento:
            filtro_qdrant = Filter(
                must=[
                    FieldCondition(
                        key="documento",
                        match=MatchValue(value=filtro_documento),
                    )
                ]
            )

        if self.client is None:
            return self._buscar_similares_en_parquet_local(
                vector_query=vector_query,
                top_k=top_k,
                filtro_documento=filtro_documento,
            )

        try:
            respuesta = self.client.query_points(
                collection_name=self.collection_name,
                query=vector_query,
                query_filter=filtro_qdrant,
                limit=top_k,
                with_payload=True,
            )

            filas: list[dict[str, Any]] = []
            for rank, punto in enumerate(respuesta.points, start=1):
                payload = punto.payload or {}
                filas.append(
                    {
                        "rank": rank,
                        "score_coseno": round(float(punto.score), 4),
                        "documento": payload.get("documento", ""),
                        "articulo": payload.get("articulo", ""),
                        "tipo_fuente": payload.get("tipo_fuente", ""),
                        "fecha": payload.get("fecha", ""),
                        "texto": payload.get("texto", ""),
                    }
                )
            return pd.DataFrame(filas)
        except Exception as e:
            logger.warning(
                "No se pudo consultar Qdrant Cloud (%s). Resolviendo búsqueda vectorial sobre Parquet local.", e
            )
            return self._buscar_similares_en_parquet_local(
                vector_query=vector_query,
                top_k=top_k,
                filtro_documento=filtro_documento,
            ) 

__all__ = [
    "EMBEDDING_DIMENSION",
    "EMBEDDINGS_BACKUP_PATH",
    "QDRANT_COLLECTION_NAME",
    "formatear_texto_documento_embedding",
    "formatear_query_embedding",
    "IndexadorQdrant",
]
