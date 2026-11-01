"""Módulo de conversión de documentos PDF a Markdown, extracción de metadatos y fragmentación del corpus normativo.

Permite estructurar las leyes, decretos y manuales de contratación estatal en fragmentos analizables
mediante estrategias recursivas y semánticas, preservando la trazabilidad de artículos y documentos.
"""

from __future__ import annotations

import logging
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
import time

import pandas as pd
from langchain_core.embeddings import Embeddings
from langchain_experimental.text_splitter import SemanticChunker
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from markitdown import MarkItDown

from observatorio.config import (
    CORPUS_DIR,
    CORPUS_MARKDOWN_DIR,
    GEMINI_API_KEY,
    GEMINI_EMBEDDING_MODEL,
    MODELO_EMBEDDING_LOCAL,
    USAR_EMBEDDINGS_LOCAL,
)

# Silenciar advertencias ruidosas de fuentes PDF (FontBBox) emitidas por pdfminer
logging.getLogger("pdfminer").setLevel(logging.ERROR)


# ============================================================================
# 1. MODELOS DE DATOS DEL DOMINIO NORMATIVO
# ============================================================================


@dataclass
class MetadatosNormativos:
    """Metadatos verificables extraídos de un documento normativo."""

    documento: str
    tipo_fuente: str
    tema: str
    fecha: str

    def to_dict(self) -> dict[str, str]:
        """Convierte los metadatos a un diccionario estándar."""
        return asdict(self)


@dataclass
class FragmentoNormativo:
    """Representa un fragmento de normativa con sus metadatos de trazabilidad."""

    texto: str
    documento: str
    tipo_fuente: str
    tema: str
    fecha: str
    articulo: str
    chunk_id: int = 0
    longitud_caracteres: int = 0

    def to_dict(self) -> dict[str, Any]:
        """Convierte el fragmento a diccionario compatible con indexación en Qdrant."""
        return asdict(self)


# ============================================================================
# 2. EXTRACCIÓN AUTOMÁTICA DE METADATOS DESDE TEXTO MARKDOWN
# ============================================================================


class ExtractorMetadatosNormativos:
    """
    Analiza el texto de un documento convertido a Markdown y genera automáticamente
    sus metadatos (`documento`, `tipo_fuente`, `tema`, `fecha`) a partir de su portada
    y encabezado, sin necesidad de ingresarlos manualmente archivo por archivo.
    """

    MESES_ES: tuple[str, ...] = (
        "enero",
        "febrero",
        "marzo",
        "abril",
        "mayo",
        "junio",
        "julio",
        "agosto",
        "septiembre",
        "setiembre",
        "octubre",
        "noviembre",
        "diciembre",
    )

    def __init__(self, max_chars_analisis: int = 3500) -> None:
        self.max_chars_analisis = max_chars_analisis

    def extraer(self, texto_md: str) -> dict[str, str]:
        """Extrae `documento`, `tipo_fuente`, `tema` y `fecha` desde el texto Markdown."""
        muestra = self._limpiar_muestra(texto_md[: self.max_chars_analisis])
        portada = muestra[:900]

        documento, tipo_fuente, anio_base = self._detectar_documento_y_tipo(portada, muestra)
        fecha = self._detectar_fecha(portada, muestra, anio_respaldo=anio_base)
        tema = self._detectar_tema(muestra, documento=documento)

        return MetadatosNormativos(
            documento=documento,
            tipo_fuente=tipo_fuente,
            tema=tema,
            fecha=fecha,
        ).to_dict()

    def _limpiar_muestra(self, texto: str) -> str:
        """Limpia separadores de tablas Markdown (`|`), años espaciados (`2 0 2 6`) y espacios."""
        lineas_limpias: list[str] = []
        for linea in texto.splitlines():
            # Omitir líneas de separación de tablas Markdown (| --- | --- |)
            if re.match(r"^[\s|\-:]+$", linea):
                continue
            sin_pipes = linea.replace("|", " ")
            # Unir años espaciados en portadas como "2 0 2 6" -> "2026"
            sin_pipes = re.sub(r"\b(1\s*9\s*\d\s*\d|2\s*0\s*[0-3]\s*\d)\b", lambda m: re.sub(r"\s+", "", m.group(0)), sin_pipes)
            limpia = re.sub(r"[ \t]+", " ", sin_pipes).strip()
            if limpia and limpia.lower() not in {"a", "menú", "menu", "inicio", "artículo", "siguiente"}:
                lineas_limpias.append(limpia)
        return "\n".join(lineas_limpias)

    def _detectar_documento_y_tipo(self, portada: str, muestra: str) -> tuple[str, str, str]:
        """Identifica el título del documento priorizando la portada antes que citas en el cuerpo."""
        portada_unida = re.sub(r"\s+", " ", portada)

        # 1. Diccionario de Datos (portada)
        if re.search(r"Diccionario\s+de\s+Datos", portada_unida, flags=re.IGNORECASE):
            return (
                "Diccionario de Datos SECOP II - Registros Administrativos",
                "Diccionario Técnico de Datos",
                "",
            )

        # 2. Circular Externa Única (portada)
        if re.search(r"CIRCULAR\s+EXTERNA\s+[ÚU]NICA", portada_unida, flags=re.IGNORECASE):
            return (
                "Circular Externa Única de Colombia Compra Eficiente",
                "Circular Externa Reglamentaria",
                "",
            )

        # 3. Guías operativas de SECOP II por modalidad ("SECOP II - Modalidades de Contratación: ...")
        match_secop_mod = re.search(
            r"SECOP\s*II\s*[-–—]?\s*Modalidades\s+de\s+Contrataci[óo]n:\s*([^\n]{5,90})",
            portada_unida,
            flags=re.IGNORECASE,
        )
        if match_secop_mod:
            subtitulo = re.split(
                r"(?:GU[ÍI]A|GGUU|CCE-|INDICE|V1\.)",
                match_secop_mod.group(1),
                flags=re.IGNORECASE,
            )[0].strip(" :-–—")
            return (
                f"Guía SECOP II - Modalidades de Contratación: {subtitulo}",
                "Guía Operativa Colombia Compra Eficiente",
                "",
            )

        # 4. Manuales o Guías de Colombia Compra Eficiente cuyo título inicia con Manual / Guía en portada
        match_guia_portada = re.search(
            r"\b((?:Manual|Gu[íi]a)\s+(?:para|de|sobre|del|de\s+la)\s+[^\n]{10,140})",
            portada_unida,
            flags=re.IGNORECASE,
        )
        if match_guia_portada:
            candidato = match_guia_portada.group(1)
            # Cortar antes de metadatos institucionales o códigos de versión en la portada
            candidato = re.split(
                r"\b(?:AGENCIA\s+NACIONAL|Directora\s+General|Subdirector|Versi[óo]n|G-[A-Z]{2,}|CCE-|con\s+el\s+objetivo|20[12]\d)\b",
                candidato,
                flags=re.IGNORECASE,
            )[0]
            titulo = self._limpiar_titulo(candidato)
            es_manual = titulo.lower().startswith("manual")
            tipo = (
                "Manual Técnico Colombia Compra Eficiente"
                if es_manual
                else "Guía Operativa Colombia Compra Eficiente"
            )
            return titulo, tipo, ""

        # 5. Decretos Reglamentarios en portada (ej. Decreto 1082 de 2015)
        match_decreto = re.search(
            r"\bDECRETO\s+(?:ÚNICO\s+REGLAMENTARIO\s+|NÚMERO\s+)?0*(\d{3,4})\s+DE\s+(\d{4})\b",
            portada,
            flags=re.IGNORECASE,
        )
        if match_decreto:
            num_dec, anio = match_decreto.group(1), match_decreto.group(2)
            return f"Decreto {num_dec} de {anio}", "Decreto Reglamentario", anio

        # 6. Leyes de la República en portada (ej. LEY 80 DE 1993, [LEY_0080_1993], Ley 1150 de 2007)
        match_ley = re.search(
            r"\bLEY[_\s]+0*(\d{1,4})[_\s]+(?:DE\s+)?(\d{4})\b",
            portada,
            flags=re.IGNORECASE,
        )
        if match_ley:
            num_ley, anio = match_ley.group(1), match_ley.group(2)
            return f"Ley {num_ley} de {anio}", "Ley de la República", anio

        # 7. Fallback: primera línea informativa de la portada
        for linea in portada.splitlines()[:10]:
            limpia = self._limpiar_titulo(linea)
            if len(limpia) >= 8 and not re.match(r"^\d{1,2}/\d{1,2}/\d{2,4}", limpia):
                return limpia[:110], "Documento Normativo / Técnico", ""

        return "Documento Normativo SECOP II", "Documento Normativo / Técnico", ""

    def _detectar_fecha(self, portada: str, muestra: str, anio_respaldo: str = "") -> str:
        """Extrae la fecha oficial de expedición o publicación priorizando Diario Oficial y portada."""
        meses_regex = "|".join(self.MESES_ES)

        # 1. Diario Oficial (fuente exacta de expedición en leyes): "Diario Oficial No. ... de 28 de octubre de 1993"
        match_diario = re.search(
            rf"Diario\s+Oficial\s+No\.?\s*[\d.]+\s+de\s+(\d{{1,2}})\s+de\s+({meses_regex})\s+de\s+(\d{{4}})",
            muestra,
            flags=re.IGNORECASE,
        )
        if match_diario:
            dia, mes, anio = match_diario.groups()
            return f"{int(dia)} de {mes.lower()} de {anio}"

        # 2. Fecha entre paréntesis tras el título de la norma: "(Mayo 26)" o "(octubre 28)" + año de la norma
        match_parentesis = re.search(
            rf"\(\s*({meses_regex})\s+(\d{{1,2}})(?:\s+de\s+(\d{{4}}))?\s*\)",
            portada,
            flags=re.IGNORECASE,
        )
        if match_parentesis:
            mes, dia, anio_p = match_parentesis.groups()
            anio_final = anio_p or anio_respaldo
            if anio_final:
                return f"{int(dia)} de {mes.lower()} de {anio_final}"

        # 3. Fecha explícita en portada: "27 de diciembre de 2023" o "Septiembre 30 de 2020"
        match_dia_mes_anio = re.search(
            rf"\b(\d{{1,2}})\s+de\s+({meses_regex})\s+de(?:l)?\s+(\d{{4}})\b",
            portada,
            flags=re.IGNORECASE,
        )
        if match_dia_mes_anio and "actualización" not in portada[: match_dia_mes_anio.start()].lower():
            dia, mes, anio = match_dia_mes_anio.groups()
            return f"{int(dia)} de {mes.lower()} de {anio}"

        match_mes_dia_anio = re.search(
            rf"\b({meses_regex})\s+(\d{{1,2}})\s+de(?:l)?\s+(\d{{4}})\b",
            portada,
            flags=re.IGNORECASE,
        )
        if match_mes_dia_anio:
            mes, dia, anio = match_mes_dia_anio.groups()
            return f"{int(dia)} de {mes.lower()} de {anio}"

        # 4. Mes y año en portada: "Fecha: agosto 2025" o "agosto de 2025"
        match_mes_anio = re.search(
            rf"\b({meses_regex})\s+(?:de(?:l)?\s+)?(\d{{4}})\b",
            portada,
            flags=re.IGNORECASE,
        )
        if match_mes_anio:
            mes, anio = match_mes_anio.groups()
            return f"{mes.capitalize()} de {anio}"

        # 5. Fecha numérica en portada (DD/MM/YYYY o DD-MM-YYYY)
        match_numerica = re.search(r"\b(\d{2}[/-]\d{2}[/-]\d{4})\b", portada)
        if match_numerica:
            return match_numerica.group(1)

        if anio_respaldo:
            return anio_respaldo

        # 6. Año de publicación de 4 dígitos aislado en portada
        match_anio = re.search(r"\b(199\d|20[0-2]\d)\b", portada)
        return match_anio.group(1) if match_anio else "Fecha no especificada"

    def _detectar_tema(self, muestra: str, documento: str) -> str:
        """Extrae el epígrafe jurídico completo o sintetiza el tema central del documento."""
        muestra_continua = re.sub(r"\s+", " ", muestra)

        # 1. Epígrafe oficial de leyes y decretos ("Por la cual se...", "Por medio del cual se...")
        match_epigrafe = re.search(
            r"(Por\s+(?:medio\s+de\s+la\s+cual|medio\s+del\s+cual|la\s+cual|el\s+cual)\s+[^.\"]{20,260})",
            muestra_continua,
            flags=re.IGNORECASE,
        )
        if match_epigrafe:
            epigrafe = match_epigrafe.group(1).strip(" .;:\"'")
            # Cortar si se coló "Resumen de Notas" o "EL CONGRESO"
            epigrafe = re.split(
                r"\b(?:Resumen\s+de\s+Notas|EL\s+CONGRESO|EL\s+PRESIDENTE|DECRETA)\b",
                epigrafe,
                flags=re.IGNORECASE,
            )[0].strip(" .;:\"'")
            return epigrafe[0].upper() + epigrafe[1:]

        # 2. Clasificación temática según contenido y título del documento
        texto_busqueda = f"{documento} {muestra_continua[:1500]}"
        temas_clave = [
            (r"diccionario\s+de\s+datos", "Definición de variables, cobertura y estructura de registros administrativos de SECOP II"),
            (r"circular\s+externa\s+[úu]nica", "Directrices y lineamientos obligatorios sobre el sistema de compra pública"),
            (r"datos\s+abiertos", "Lineamientos de consulta, uso y aprovechamiento de datos abiertos del SECOP"),
            (r"m[íi]nima\s+cuant[íi]a", "Procedimiento y reglas de la modalidad de selección de mínima cuantía"),
            (r"contrataci[óo]n\s+directa", "Lineamientos operativos de la modalidad de contratación directa en SECOP II"),
            (r"subasta\s+inversa|selecci[óo]n\s+abreviada", "Procedimiento de selección abreviada y subasta inversa electrónica en SECOP II"),
            (r"supervisi[óo]n\s+e\s+interventor[íi]a", "Ejercicio de las funciones de supervisión e interventoría en contratos estatales"),
            (r"liquidaci[óo]n", "Lineamientos para la liquidación de contratos y procesos de contratación estatal"),
            (r"sancionatorio", "Procedimiento administrativo sancionatorio contractual en entidades estatales"),
            (r"mipymes", "Promoción de la participación de las Mipymes en procesos de compra y contratación pública"),
            (r"control\s+social", "Guía para el ejercicio del control social y veeduría ciudadana en la contratación pública"),
            (r"codificaci[óo]n\s+de\s+bienes|unspsc", "Codificación de bienes y servicios de acuerdo con el clasificador estándar UNSPSC"),
        ]
        for fuente_texto in (documento, muestra_continua[:1500]):
            for patron, descripcion_tema in temas_clave:
                if re.search(patron, fuente_texto, flags=re.IGNORECASE):
                    return descripcion_tema

        return f"Lineamientos normativos y técnicos de contratación pública ({documento})"

    @staticmethod
    def _limpiar_titulo(linea: str) -> str:
        """Normaliza caracteres de formato Markdown de un título."""
        limpia = re.sub(r"^[#>*\-\d.\s]+", "", linea)
        limpia = re.sub(r"[*_`~]+", "", limpia)
        return re.sub(r"\s+", " ", limpia).strip(" :-–—")


# ============================================================================
# 3. CONVERSIÓN PDF -> MARKDOWN E INYECCIÓN DE METADATOS AL INICIO
# ============================================================================


class ProcesadorCorpusMarkdown:
    """
    Convierte archivos PDF del corpus normativo a Markdown, genera automáticamente
    sus metadatos a partir del texto convertido y los estampa al inicio de cada `.md`.
    """

    DELIMITADOR_METADATOS: str = "---"

    def __init__(
        self,
        corpus_dir: str | Path = CORPUS_DIR,
        corpus_markdown_dir: str | Path = CORPUS_MARKDOWN_DIR,
        extractor: ExtractorMetadatosNormativos | None = None,
    ) -> None:
        self.corpus_dir = Path(corpus_dir)
        self.corpus_markdown_dir = Path(corpus_markdown_dir)
        self.extractor = extractor or ExtractorMetadatosNormativos()
        self._conversor_md: MarkItDown | None = None

    def convertir_pdf_a_markdown(self, ruta_pdf: str | Path) -> str:
        """Convierte un archivo PDF a texto Markdown utilizando `MarkItDown`."""
        if self._conversor_md is None:
            self._conversor_md = MarkItDown()
        resultado = self._conversor_md.convert(str(ruta_pdf))
        texto_md = getattr(resultado, "text_content", str(resultado))
        return texto_md.strip()

    def agregar_metadatos_a_documento(
        self,
        texto_md: str,
        metadatos: dict[str, str] | None = None,
    ) -> tuple[str, dict[str, str]]:
        """
        Extrae automáticamente los metadatos desde el texto Markdown (si no se pasan)
        y los coloca al inicio del documento `.md`. Devuelve `(texto_con_metadatos, metadatos)`.
        """
        cuerpo, meta_existente = self.separar_encabezado_y_cuerpo(texto_md)
        meta_final = metadatos or meta_existente or self.extractor.extraer(cuerpo)

        lineas_meta = [f"**{clave}**: {valor}" for clave, valor in meta_final.items()]
        bloque_metadatos = "\n".join(
            [self.DELIMITADOR_METADATOS, *lineas_meta, self.DELIMITADOR_METADATOS]
        )
        texto_con_metadatos = f"{bloque_metadatos}\n\n{cuerpo.lstrip()}"
        return texto_con_metadatos, meta_final

    def separar_encabezado_y_cuerpo(self, texto_md: str) -> tuple[str, dict[str, str]]:
        """
        Separa el bloque de metadatos del inicio de un archivo `.md` y devuelve
        `(cuerpo_sin_metadatos, diccionario_metadatos)`.
        """
        texto_limpio = texto_md.lstrip()
        patron_bloque = re.compile(
            r"^---\s*\n((?:\*\*[^*]+\*\*\s*:\s*[^\n]+\n?)+)---\s*\n*",
            flags=re.MULTILINE,
        )
        match_bloque = patron_bloque.match(texto_limpio)
        if match_bloque:
            metadatos: dict[str, str] = {}
            for linea in match_bloque.group(1).splitlines():
                m = re.match(r"^\*\*([^*]+)\*\*\s*:\s*(.+)$", linea.strip())
                if m:
                    metadatos[m.group(1).strip()] = m.group(2).strip()
            cuerpo = texto_limpio[match_bloque.end() :]
            return cuerpo, metadatos

        return texto_md, {}

    def procesar_directorio_corpus(
        self,
        directorio_raiz: str | Path | None = None,
        directorio_salida_md: str | Path | None = None,
        forzar_reconversion: bool = False,
    ) -> list[tuple[str, dict[str, str]]]:
        """
        Convierte todos los PDFs del directorio a Markdown, genera automáticamente sus
        metadatos desde el texto, los escribe al inicio de cada archivo `.md` en
        `directorio_salida_md` y devuelve el corpus `[(texto_md_con_metadatos, metadatos), ...]`.
        """
        raiz = Path(directorio_raiz) if directorio_raiz else self.corpus_dir
        dir_salida = Path(directorio_salida_md) if directorio_salida_md else self.corpus_markdown_dir
        dir_salida.mkdir(parents=True, exist_ok=True)

        archivos_pdf = sorted(raiz.rglob("*.pdf"))
        corpus: list[tuple[str, dict[str, str]]] = []

        for ruta_pdf in archivos_pdf:
            ruta_md = dir_salida / f"{ruta_pdf.stem}.md"

            if ruta_md.exists() and not forzar_reconversion:
                contenido_existente = ruta_md.read_text(encoding="utf-8")
                cuerpo, _ = self.separar_encabezado_y_cuerpo(contenido_existente)
            else:
                cuerpo = self.convertir_pdf_a_markdown(ruta_pdf)

            texto_con_metadatos, metadatos = self.agregar_metadatos_a_documento(cuerpo)
            ruta_md.write_text(texto_con_metadatos, encoding="utf-8")
            corpus.append((texto_con_metadatos, metadatos))

        return corpus


# ============================================================================
# 4. FRAGMENTACIÓN DEL CORPUS (RECURSIVA Y SEMÁNTICA)
# ============================================================================


class EmbeddingsLocalesSentenceTransformer(Embeddings):
    """
    Cliente de embeddings local con `sentence-transformers` compatible con la interfaz
    `Embeddings` de LangChain. Permite ejecutar la fragmentación semántica y las evaluaciones
    100% en local, sin conexión a internet ni consumo de cuota de API.
    """

    _MODELO_CACHE: dict[str, Any] = {}

    def __init__(
        self,
        model_name: str = MODELO_EMBEDDING_LOCAL or "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
    ) -> None:
        self.model_name = model_name
        if model_name not in self._MODELO_CACHE:
            try:
                from sentence_transformers import SentenceTransformer

                try:
                    modelo = SentenceTransformer(model_name, local_files_only=True)
                except Exception:
                    modelo = SentenceTransformer(model_name)
                self._MODELO_CACHE[model_name] = modelo
            except Exception as exc:
                raise ImportError(
                    "Para utilizar embeddings locales necesitas tener instalada la librería 'sentence-transformers'.\n"
                    "Instálala ejecutando: pip install sentence-transformers"
                ) from exc
        self.model = self._MODELO_CACHE[model_name]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        textos_limpios = [t if t.strip() else " " for t in texts]
        vectores = self.model.encode(textos_limpios, normalize_embeddings=True, show_progress_bar=False)
        return [v.tolist() for v in vectores]

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]


class EmbeddingsGeminiConCuota(GoogleGenerativeAIEmbeddings):
    """
    Extensión de `GoogleGenerativeAIEmbeddings` que respeta el límite de la capa
    gratuita de Google AI Studio (100 textos embebidos por minuto), enviando sub-lotes
    controlados y reintentando automáticamente si recibe `429 RESOURCE_EXHAUSTED`.
    Si se agotan los reintentos o falla la red, conmuta transparentemente al modelo
    local de sentence-transformers para garantizar que ningún fragmento quede sin vector.
    """

    def embed_documents(
        self,
        texts: list[str],
        batch_size: int = 80,
        task_type: str | None = None,
        titles: list[str] | None = None,
        output_dimensionality: int | None = None,
    ) -> list[list[float]]:
        tamano_sublote = min(batch_size, 80)
        todos_los_vectores: list[list[float]] = []
        textos_en_ventana = 0
        inicio_ventana = time.monotonic()

        for i in range(0, len(texts), tamano_sublote):
            sublote = texts[i : i + tamano_sublote]
            subtitulos = titles[i : i + tamano_sublote] if titles else None

            # Si este sub-lote superaría los 90 textos en el minuto actual, pausar preventivamente
            transcurrido = time.monotonic() - inicio_ventana
            if textos_en_ventana + len(sublote) > 90 and transcurrido < 62.0:
                espera = max(62.0 - transcurrido, 5.0)
                print(
                    f"⏳ Control de cuota gratuita Gemini (90/100 textos/min): "
                    f"pausando {espera:.0f}s antes del siguiente lote ({i}/{len(texts)})..."
                )
                time.sleep(espera)
                inicio_ventana = time.monotonic()
                textos_en_ventana = 0

            # Reintento ante 429 RESOURCE_EXHAUSTED con fallback a embeddings locales si se supera el límite
            exito = False
            for intento in range(3):
                try:
                    vectores = super().embed_documents(
                        sublote,
                        batch_size=tamano_sublote,
                        task_type=task_type,
                        titles=subtitulos,
                        output_dimensionality=output_dimensionality,
                    )
                    todos_los_vectores.extend(vectores)
                    textos_en_ventana += len(sublote)
                    exito = True
                    break
                except Exception as exc:
                    msg = str(exc)
                    if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                        match_retry = re.search(r"retry in (\d+(?:\.\d+)?)s", msg, flags=re.IGNORECASE)
                        espera_429 = (float(match_retry.group(1)) + 4.0) if match_retry else 25.0
                        print(
                            f"⏳ Cuota de API alcanzada (429). Esperando {espera_429:.0f}s "
                            f"(intento {intento + 1}/3)..."
                        )
                        time.sleep(espera_429)
                        inicio_ventana = time.monotonic()
                        textos_en_ventana = 0
                    else:
                        print(f"⚠️ Error al consultar Gemini API ({exc}). Conmutando lote a modelo local...")
                        break

            if not exito:
                # Fallback al modelo local: garantiza len(todos_los_vectores) == len(texts)
                print("ℹ️ Procesando lote de fragmentos con embeddings locales de sentence-transformers...")
                local_emb = EmbeddingsLocalesSentenceTransformer()
                vectores_locales = local_emb.embed_documents(sublote)
                todos_los_vectores.extend(vectores_locales)

        return todos_los_vectores


class FragmentadorNormativo:
    """
    Divide los documentos Markdown del corpus en fragmentos (chunks) ya sea respetando
    la estructura por artículos (`RecursiveCharacterTextSplitter`) o mediante corte
    semántico con embeddings de Gemini (`SemanticChunker`), conservando sus metadatos.
    """

    SEPARADORES_NORMATIVOS: list[str] = [
        "\n## ",
        "\n### ",
        "\nArtículo ",
        "\nARTÍCULO ",
        "\nARTICULO ",
        "\n\n",
        "\n",
        " ",
    ]

    def __init__(self, procesador_md: ProcesadorCorpusMarkdown | None = None) -> None:
        self.procesador_md = procesador_md or ProcesadorCorpusMarkdown()

    def fragmentar_recursivo(
        self,
        texto: str,
        metadatos_base: dict[str, str] | None = None,
        chunk_size: int = 1000,
        chunk_overlap: int = 150,
    ) -> list[dict[str, Any]]:
        """Fragmenta un documento con `RecursiveCharacterTextSplitter` respetando límites de palabras y artículos."""
        cuerpo, meta_resuelta = self._resolver_cuerpo_y_metadatos(texto, metadatos_base)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=self.SEPARADORES_NORMATIVOS,
            keep_separator=True,
        )
        textos = splitter.split_text(cuerpo)
        return self._construir_lista_fragmentos(textos, meta_resuelta)

    @staticmethod
    def _normalizar_modelo_embeddings(model_name: str) -> str:
        """Reemplaza identificadores experimentales retirados por el modelo estable vigente."""
        if not model_name or "gemini-embedding-exp" in model_name:
            return "models/gemini-embedding-001"
        return model_name

    def crear_cliente_embeddings(
        self,
        model_name: str = GEMINI_EMBEDDING_MODEL,
        usar_local: bool | None = None,
    ) -> Embeddings:
        """
        Inicializa el cliente de embeddings.
        
        Si `usar_local=True`, `USAR_EMBEDDINGS_LOCAL=True` o si no se cuenta con `GEMINI_API_KEY`,
        devuelve `EmbeddingsLocalesSentenceTransformer` (100% local, offline y sin consumo de cuota).
        En caso contrario, utiliza `EmbeddingsGeminiConCuota` con fallback automático.
        """
        debe_usar_local = (
            usar_local if usar_local is not None else (USAR_EMBEDDINGS_LOCAL or not bool(GEMINI_API_KEY))
        )
        if debe_usar_local:
            return EmbeddingsLocalesSentenceTransformer()

        modelo_valido = self._normalizar_modelo_embeddings(model_name)
        return EmbeddingsGeminiConCuota(
            model=modelo_valido,
            google_api_key=GEMINI_API_KEY,
        )

    @staticmethod
    def agrupar_unidades_normativas(texto: str, min_chars_unidad: int = 450) -> list[str]:
        """
        Agrupa líneas y párrafos cortos en bloques normativos (~450 caracteres) respetando
        los inicios de Artículo/Sección. Evita que `SemanticChunker` corte en cada punto (`.`)
        de abreviaturas como 'Art. 1.' o 'No. 41.094' y reduce 8x las llamadas a la API.
        """
        parrafos = [p.strip() for p in re.split(r"\n\s*\n+", texto) if p.strip()]
        unidades: list[str] = []
        actual: list[str] = []
        longitud_actual = 0

        for parrafo in parrafos:
            es_nuevo_articulo = bool(
                re.match(r"^(?:#{1,3}\s+|ART[ÍI]CULO\s+\d+)", parrafo, flags=re.IGNORECASE)
            )
            if actual and (
                longitud_actual + len(parrafo) > min_chars_unidad
                or (es_nuevo_articulo and longitud_actual >= 180)
            ):
                unidades.append("\n\n".join(actual))
                actual = [parrafo]
                longitud_actual = len(parrafo)
            else:
                actual.append(parrafo)
                longitud_actual += len(parrafo)

        if actual:
            unidades.append("\n\n".join(actual))
        return unidades

    def fragmentar_semantico(
        self,
        texto: str,
        metadatos_base: dict[str, str] | None = None,
        breakpoint_percentile: int = 95,
        model_name: str = GEMINI_EMBEDDING_MODEL,
        embeddings: Embeddings | None = None,
        usar_local: bool | None = None,
    ) -> list[dict[str, Any]]:
        """Fragmenta un documento detectando discontinuidades semánticas mediante cálculo de distancias coseno."""
        cuerpo, meta_resuelta = self._resolver_cuerpo_y_metadatos(texto, metadatos_base)
        unidades = self.agrupar_unidades_normativas(cuerpo)
        if len(unidades) <= 1:
            return self._construir_lista_fragmentos([cuerpo], meta_resuelta)

        modelo_embeddings = embeddings or self.crear_cliente_embeddings(model_name, usar_local=usar_local)
        splitter = SemanticChunker(
            embeddings=modelo_embeddings,
            breakpoint_threshold_type="percentile",
            breakpoint_threshold_amount=breakpoint_percentile,
        )

        distances, sentences = splitter._calculate_sentence_distances(unidades)
        umbral, arreglo_bp = splitter._calculate_breakpoint_threshold(distances)
        indices_corte = [i for i, val in enumerate(arreglo_bp) if val > umbral]

        textos: list[str] = []
        inicio = 0
        for idx_corte in indices_corte:
            grupo = sentences[inicio : idx_corte + 1]
            textos.append("\n\n".join(d["sentence"] for d in grupo))
            inicio = idx_corte + 1
        if inicio < len(sentences):
            textos.append("\n\n".join(d["sentence"] for d in sentences[inicio:]))

        return self._construir_lista_fragmentos(textos, meta_resuelta)

    def fragmentar_corpus(
        self,
        corpus: list[tuple[str, dict[str, str]]],
        metodo: str = "recursivo",
        chunk_size: int = 1000,
        chunk_overlap: int = 150,
        breakpoint_percentile: int = 95,
        model_name: str = GEMINI_EMBEDDING_MODEL,
        usar_local: bool | None = None,
    ) -> list[dict[str, Any]]:
        """
        Fragmenta todos los documentos del corpus con la estrategia elegida (`'recursivo'`
        o `'semantico'`) y devuelve la lista consolidada de fragmentos lista para Qdrant.
        """
        todos_los_fragmentos: list[dict[str, Any]] = []
        es_semantico = metodo.lower() in ("semantico", "semantic")
        embeddings = (
            self.crear_cliente_embeddings(model_name, usar_local=usar_local)
            if es_semantico
            else None
        )

        for texto_md, meta in corpus:
            if es_semantico:
                frags = self.fragmentar_semantico(
                    texto_md,
                    metadatos_base=meta,
                    breakpoint_percentile=breakpoint_percentile,
                    model_name=model_name,
                    embeddings=embeddings,
                    usar_local=usar_local,
                )
            else:
                frags = self.fragmentar_recursivo(
                    texto_md,
                    metadatos_base=meta,
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap,
                )
            todos_los_fragmentos.extend(frags)

        return todos_los_fragmentos

    def _resolver_cuerpo_y_metadatos(
        self,
        texto: str,
        metadatos_base: dict[str, str] | None,
    ) -> tuple[str, dict[str, str]]:
        """Separa el encabezado de metadatos del cuerpo para no duplicarlo en el texto de los chunks."""
        cuerpo, meta_encabezado = self.procesador_md.separar_encabezado_y_cuerpo(texto)
        meta_final = metadatos_base or meta_encabezado or self.procesador_md.extractor.extraer(cuerpo)
        return cuerpo, meta_final

    def _construir_lista_fragmentos(
        self,
        textos: list[str],
        metadatos_base: dict[str, str],
    ) -> list[dict[str, Any]]:
        """Empaqueta cada fragmento detectando el artículo o sección al que pertenece."""
        fragmentos: list[dict[str, Any]] = []
        ultimo_articulo = "Sección General / Preliminar"

        for idx, frag in enumerate(textos):
            texto_limpio = frag.strip()
            if not texto_limpio:
                continue

            articulo_detectado = self._detectar_articulo_o_seccion(texto_limpio)
            if articulo_detectado:
                ultimo_articulo = articulo_detectado

            fragmentos.append(
                {
                    "chunk_id": idx,
                    "texto": texto_limpio,
                    "longitud_caracteres": len(texto_limpio),
                    **metadatos_base,
                    "articulo": metadatos_base.get("articulo") or ultimo_articulo,
                }
            )
        return fragmentos

    @staticmethod
    def _detectar_articulo_o_seccion(texto_fragmento: str) -> str | None:
        """Identifica si el fragmento contiene un número de artículo o encabezado de sección."""
        match_art = re.search(
            r"\bART[ÍI]CULO\s+(\d+\s*[°ºo.]?(?:\s*[A-Za-z])?)",
            texto_fragmento,
            flags=re.IGNORECASE,
        )
        if match_art:
            numero = re.sub(r"[°ºo.]", "", match_art.group(1)).strip()
            return f"Artículo {numero}"

        match_seccion = re.search(
            r"^(?:#{1,3})\s+([^\n]{3,80})",
            texto_fragmento,
            flags=re.MULTILINE,
        )
        if match_seccion:
            return match_seccion.group(1).strip()

        return None


# ============================================================================
# 5. EVALUACIÓN Y BENCHMARK DE CONFIGURACIONES DE FRAGMENTACIÓN
# ============================================================================


class EvaluadorChunking:
    """
    Compara empíricamente distintas configuraciones de fragmentación (recursiva por tamaños o
    semántica por percentiles) y devuelve un DataFrame con métricas cuantitativas consolidadas.
    """

    def __init__(self, fragmentador: FragmentadorNormativo | None = None) -> None:
        self.fragmentador = fragmentador or FragmentadorNormativo()

    def comparar_recursivo(
        self,
        corpus: list[tuple[str, dict[str, str]]],
        configuraciones: list[tuple[int, int]] | None = None,
    ) -> pd.DataFrame:
        """
        Evalúa múltiples tuplas (chunk_size, chunk_overlap) calculando número de fragmentos y distribución de longitud.

        Args:
            corpus: Lista de tuplas (texto_markdown, metadatos).
            configuraciones: Lista opcional de tuplas (chunk_size, chunk_overlap).

        Returns:
            DataFrame con columnas chunk_size, chunk_overlap, num_fragmentos, longitud_media, minima y maxima.
        """
        if configuraciones is None:
            configuraciones = [(600, 100), (1000, 150), (1600, 250)]

        filas: list[dict[str, Any]] = []
        for chunk_size, chunk_overlap in configuraciones:
            todos = self.fragmentador.fragmentar_corpus(
                corpus,
                metodo="recursivo",
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )
            filas.append(
                {
                    "chunk_size": chunk_size,
                    "chunk_overlap": chunk_overlap,
                    **self._calcular_metricas_longitud(todos),
                }
            )
        return pd.DataFrame(filas)

    def comparar_semantico(
        self,
        corpus: list[tuple[str, dict[str, str]]],
        percentiles_a_probar: list[int] | None = None,
        model_name: str = GEMINI_EMBEDDING_MODEL,
        max_chars_por_doc: int | None = 18000,
        usar_local: bool | None = None,
    ) -> pd.DataFrame:
        """
        Evalúa el impacto de distintos umbrales percentiles de corte semántico.

        Args:
            corpus: Lista de tuplas (texto_markdown, metadatos).
            percentiles_a_probar: Lista de percentiles a evaluar (por defecto [90, 95, 99]).
            model_name: Modelo de embeddings para la representación vectorial.
            max_chars_por_doc: Máximo de caracteres a muestrear por documento para acelerar el benchmark.
            usar_local: Si es True, utiliza el modelo local sin conexión a API externa.

        Returns:
            DataFrame con el resumen estadístico de chunks generados por percentil.
        """
        if percentiles_a_probar is None:
            percentiles_a_probar = [90, 95, 99]

        embeddings = self.fragmentador.crear_cliente_embeddings(model_name, usar_local=usar_local)
        splitter_base = SemanticChunker(
            embeddings=embeddings,
            breakpoint_threshold_type="percentile",
            breakpoint_threshold_amount=95,
        )

        # 1. Precalcular distancias semánticas una única vez por documento
        distancias_por_doc: list[tuple[list[float], list[dict[str, Any]]]] = []
        for texto_md, meta in corpus:
            cuerpo, _ = self.fragmentador._resolver_cuerpo_y_metadatos(texto_md, meta)
            muestra_cuerpo = cuerpo[:max_chars_por_doc] if max_chars_por_doc else cuerpo
            unidades = self.fragmentador.agrupar_unidades_normativas(muestra_cuerpo)

            if len(unidades) <= 1:
                distancias_por_doc.append(([], [{"sentence": muestra_cuerpo}]))
            else:
                distances, sentences = splitter_base._calculate_sentence_distances(unidades)
                distancias_por_doc.append((distances, sentences))

        # 2. Evaluar cada percentil sobre las distancias ya calculadas
        filas: list[dict[str, Any]] = []
        for percentile in percentiles_a_probar:
            splitter_base.breakpoint_threshold_amount = percentile
            longitudes_totales: list[int] = []

            for distances, sentences in distancias_por_doc:
                if not distances:
                    texto_unico = sentences[0]["sentence"].strip()
                    if texto_unico:
                        longitudes_totales.append(len(texto_unico))
                    continue

                umbral, arreglo_bp = splitter_base._calculate_breakpoint_threshold(distances)
                indices_corte = [i for i, val in enumerate(arreglo_bp) if val > umbral]

                inicio = 0
                for idx_corte in indices_corte:
                    grupo = sentences[inicio : idx_corte + 1]
                    bloque = "\n\n".join(d["sentence"] for d in grupo).strip()
                    if bloque:
                        longitudes_totales.append(len(bloque))
                    inicio = idx_corte + 1

                if inicio < len(sentences):
                    bloque_final = "\n\n".join(d["sentence"] for d in sentences[inicio:]).strip()
                    if bloque_final:
                        longitudes_totales.append(len(bloque_final))

            filas.append(
                {
                    "breakpoint_percentile": percentile,
                    "num_fragmentos": len(longitudes_totales),
                    "longitud_media": round(
                        sum(longitudes_totales) / max(len(longitudes_totales), 1), 1
                    ),
                    "longitud_minima": min(longitudes_totales) if longitudes_totales else 0,
                    "longitud_maxima": max(longitudes_totales) if longitudes_totales else 0,
                }
            )
        return pd.DataFrame(filas)

    @staticmethod
    def _calcular_metricas_longitud(fragmentos: list[dict[str, Any]]) -> dict[str, int | float]:
        """Calcula conteo, media, mínimo y máximo de caracteres de una lista de fragmentos."""
        longitudes = [f["longitud_caracteres"] for f in fragmentos]
        return {
            "num_fragmentos": len(longitudes),
            "longitud_media": round(sum(longitudes) / max(len(longitudes), 1), 1),
            "longitud_minima": min(longitudes) if longitudes else 0,
            "longitud_maxima": max(longitudes) if longitudes else 0,
        }


__all__ = [
    "MetadatosNormativos",
    "FragmentoNormativo",
    "ExtractorMetadatosNormativos",
    "ProcesadorCorpusMarkdown",
    "EmbeddingsGeminiConCuota",
    "EmbeddingsLocalesSentenceTransformer",
    "FragmentadorNormativo",
    "EvaluadorChunking",
]
