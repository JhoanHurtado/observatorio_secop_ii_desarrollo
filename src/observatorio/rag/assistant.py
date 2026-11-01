"""Orquestador híbrido RAG (búsqueda semántica en Qdrant) + SQL (consultas relacionales en SQLite).

Permite responder consultas ciudadanas y de veeduría integrando el registro histórico de SECOP II
con el marco regulatorio colombiano (Leyes, Decretos y Guías CCE). Soporta inferencia dual:
asistida por LLM en la nube o totalmente autónoma y local sin dependencia de APIs externas.
"""

from __future__ import annotations

import json
import logging
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

import pandas as pd

from observatorio.config import (
    GEMINI_API_KEY,
    GEMINI_LLM_MODEL,
    SQLITE_DB_PATH,
    SQL_MAX_ROWS_LIMIT,
)
from observatorio.data.database import ejecutar_consulta_segura, validar_sql_solo_lectura
from observatorio.rag.vectorstore import IndexadorQdrant

logger = logging.getLogger(__name__)


def formatear_df_a_markdown(df: pd.DataFrame) -> str:
    """Convierte un DataFrame a tabla Markdown sin depender obligatoriamente de 'tabulate'."""
    try:
        return df.to_markdown(index=False)
    except Exception:
        cols = [str(c) for c in df.columns]
        header = "| " + " | ".join(cols) + " |"
        sep = "| " + " | ".join(["---"] * len(cols)) + " |"
        filas = []
        for _, row in df.iterrows():
            val_strs = [str(row[c]).replace("\n", " ").replace("|", "\\|") for c in cols]
            filas.append("| " + " | ".join(val_strs) + " |")
        return "\n".join([header, sep] + filas)


@dataclass
class RespuestaAsistente:
    """Estructura estándar de respuesta del asistente con trazabilidad de fuentes."""

    respuesta: str
    tipo_consulta: str = "normativa"  # "normativa", "cuantitativa", "mixta", "fuera_de_alcance"
    sql_ejecutado: str | None = None
    datos_sql: list[dict[str, Any]] | None = None
    fuentes_normativas: list[dict[str, Any]] = field(default_factory=list)
    latencia_segundos: float = 0.0
    modo_utilizado: str = "local"  # "local", "gemini", "gemini_fallback_a_local"


class AsistenteHibrido:
    """
    Motor conversacional híbrido de consulta para contratación estatal.

    Qué hace:
        Clasifica la intención del usuario (cuantitativa, normativa, mixta o fuera de alcance),
        recupera artículos relevantes de la base de conocimiento vectorial y/o formula y ejecuta consultas
        analíticas seguras en SQL para generar respuestas interpretadas y estructuradas.

    Cómo lo hace:
        1. Clasifica la pregunta mediante expresiones regulares de dominio y palabras clave.
        2. Si la consulta involucra datos numéricos, traduce la pregunta a una sentencia SELECT segura
           con límites y ordenamiento dinámico, ejecutándola en SQLite en modo solo lectura.
        3. Si la consulta involucra normativa, calcula la similitud semántica contra los vectores de Qdrant.
        4. Sintetiza la respuesta en prosa explicativa y estructurada, ya sea de forma determinística local
           o mediante Gemini con fallback garantizado a local en caso de error de red o límite de cuota.
    """

    # Palabras clave para enrutamiento local
    PATRONES_SQL = re.compile(
        r"\b(cu[aá]ntos?|total|suma|promedio|monto|ranking|top|"
        r"adicion(?:es)?|pr[oó]rrogas?|d[ií]as adicionados|contratistas?|"
        r"estad[ií]sticas?|distribuci[oó]n|cu[aá]l fue el valor|cu[aá]nto se contrat[oó]|"
        r"cu[aá]nto dinero|mayor cuant[ií]a|mayor valor|m[aá]s contratos)\b",
        re.IGNORECASE,
    )

    PATRONES_RAG = re.compile(
        r"\b(ley|decreto|art[ií]culo|norma|cce|colombia compra eficiente|manual|gu[ií]a|"
        r"principio(?:s)?|plazo|liquidaci[oó]n|inhabilidad(?:es)?|incompatibilidad(?:es)?|"
        r"capacidad residual|pliego(?:s)?|supervisi[oó]n|interventor[ií]a|requisito(?:s)?|r[eé]gimen|"
        r"selecci[oó]n abreviada|m[ií]nima cuant[ií]a|concurso de m[eé]ritos|licitaci[oó]n p[uú]blica|"
        r"causal(?:es)?|justificaci[oó]n|qu[eé] dice|estatuto|servidor p[uú]blico|se puede|puedo|prohibid[oa])\b",
        re.IGNORECASE,
    )

    PATRONES_FUERA_ALCANCE = re.compile(
        r"\b(receta|cocina|comida|postre|torta|chocolate|f[uú]tbol|partido|mundial|gol|"
        r"pel[ií]cula|m[uú]sica|canci[oó]n|clima|tiempo|hor[oó]scopo|signo|visa|viaje|"
        r"turismo|medicina|s[ií]ntoma|remedio|videojuego|chiste|cuento|poema)\b",
        re.IGNORECASE,
    )

    PATRONES_DOMINIO = re.compile(
        r"\b(contrat|licita|secop|proveed|entidad|pliego|adjudica|cuant[ií]a|"
        r"estatal|p[uú]blic|compra|obra|suministro|servicios?|consultor|interventor|"
        r"supervis|ley|decreto|art[ií]culo|norma|cce|resoluci[oó]n|estatuto|inhabil|"
        r"presupuesto|recursos|pr[oó]rroga|adici[oó]n|d[ií]as adicionados|pyme|veedur|"
        r"concurso de m[eé]ritos|m[ií]nima cuant[ií]a|selecci[oó]n abreviada|colombia compra)\b",
        re.IGNORECASE,
    )

    def __init__(
        self,
        indexador_vectorial: IndexadorQdrant | None = None,
        db_path: Path | str = SQLITE_DB_PATH,
        usar_local: bool = False,
        use_local: bool | None = None,
        gemini_api_key: str | None = None,
        modelo_nombre: str = GEMINI_LLM_MODEL,
        top_k_default: int = 3,
        umbral_fuera_de_alcance: float = 0.25,
    ) -> None:
        """
        Inicializa el asistente híbrido.

        Args:
            indexador_vectorial: Instancia de IndexadorQdrant. Si es None, crea una con la config global.
            db_path: Ruta a la base de datos SQLite de contratos.
            usar_local: Si es True, opera 100% localmente sin llamar a Gemini.
            use_local: Alias de conveniencia en inglés para `usar_local`.
            gemini_api_key: API Key de Google Gemini (opcional, lee de GEMINI_API_KEY).
            modelo_nombre: Nombre del modelo LLM de Gemini (por defecto gemini-2.5-flash).
            top_k_default: Cantidad de fragmentos normativos a recuperar.
            umbral_fuera_de_alcance: Umbral de similitud coseno mínima para RAG.
        """
        self.db_path = Path(db_path)
        self.top_k_default = top_k_default
        self.umbral_fuera_de_alcance = umbral_fuera_de_alcance
        self.modelo_nombre = modelo_nombre

        # Resolver bandera local (soporta usar_local y use_local)
        if use_local is not None:
            self.usar_local = bool(use_local)
        else:
            self.usar_local = bool(usar_local)

        # Configurar Indexador Vectorial
        if indexador_vectorial is not None:
            self.indexador = indexador_vectorial
        else:
            self.indexador = IndexadorQdrant(usar_local=self.usar_local)

        # Configurar cliente Gemini solo si no está forzado a local
        self.gemini_client = None
        key = (gemini_api_key or GEMINI_API_KEY or "").strip().strip('"').strip("'")
        if not self.usar_local and key:
            try:
                from google import genai
                self.gemini_client = genai.Client(api_key=key)
            except Exception as e:
                logger.warning("No se pudo inicializar google.genai Client: %s. Operando en modo local.", e)
                self.usar_local = True
        else:
            self.usar_local = True

        modo_str = "100% LOCAL (sin Gemini)" if self.usar_local else f"HÍBRIDO con Gemini ({self.modelo_nombre})"
        print(f"🤖 AsistenteHibrido inicializado en modo: {modo_str}.")

    def clasificar_consulta(self, pregunta: str) -> Literal["normativa", "cuantitativa", "mixta", "fuera_de_alcance"]:
        """
        Clasifica la intención de la consulta del usuario entre:
        - `cuantitativa`: Preguntas sobre cifras, datos, rankings o montos de contratos.
        - `normativa`: Preguntas sobre leyes, decretos, artículos o manuales.
        - `mixta`: Preguntas que requieren contrastar datos reales con el marco legal.
        - `fuera_de_alcance`: Preguntas ajenas a contratación estatal o con temas no permitidos.
        """
        preg_limpia = pregunta.strip().lower()

        # Detección de fuera de alcance explícito
        if self.PATRONES_FUERA_ALCANCE.search(preg_limpia):
            return "fuera_de_alcance"

        tiene_sql = bool(self.PATRONES_SQL.search(preg_limpia))
        tiene_rag = bool(self.PATRONES_RAG.search(preg_limpia))
        tiene_dominio = bool(self.PATRONES_DOMINIO.search(preg_limpia))

        if not tiene_dominio and not tiene_sql and not tiene_rag:
            return "fuera_de_alcance"

        if tiene_sql and tiene_rag:
            return "mixta"
        if tiene_sql:
            return "cuantitativa"
        if tiene_rag:
            return "normativa"

        return "normativa" if tiene_dominio else "fuera_de_alcance"

    def _extraer_limite(self, pregunta: str, default: int = 5) -> int:
        """Extrae el número de elementos solicitados en la pregunta (ej. 'las 5 entidades', 'top 10')."""
        # Buscar patrones como "top 5", "las 5", "5 modalidades", "primeros 3"
        m = re.search(r"\b(?:top\s*|las?\s+|los?\s+|primer[oa]s?\s+)?(\d{1,2})\s*(?:entidades?|modalidades?|contratistas?|proveedores?|tipos?|contratos?|procesos?|empresas?)?\b", pregunta, re.IGNORECASE)
        if m and m.group(1):
            try:
                val = int(m.group(1))
                if 1 <= val <= 50:
                    return val
            except ValueError:
                pass
        return default

    def generar_sql_local(self, pregunta: str) -> str:
        """
        Genera una consulta SQL SELECT segura en modo local basada en patrones de lenguaje natural.
        Detecta filtros territoriales, temporales, cuantías y límites solicitados por el usuario.
        """
        p = pregunta.lower()

        # Filtros de ciudad detectables
        filtro_ciudad = ""
        ciudades = ["cali", "palmira", "buenaventura", "yumbo", "jamundí", "jamundi", "tuluá", "tulua", "cartago", "buga"]
        for c in ciudades:
            if c in p:
                c_sql = "Cali" if c == "cali" else c.title()
                filtro_ciudad = f" AND UPPER(ciudad) LIKE '%{c_sql.upper()}%'"
                break

        # Filtro de año
        filtro_anio = ""
        m_anio = re.search(r"\b(202[0-6])\b", p)
        if m_anio:
            anio = m_anio.group(1)
            filtro_anio = f" AND fecha_de_firma LIKE '{anio}%'"

        where_base = f"WHERE 1=1{filtro_ciudad}{filtro_anio}"

        # Detección de criterio de ordenación (cuantía económica vs volumen de contratos)
        quiere_valor = any(term in p for term in [
            "cuantía", "cuantia", "valor", "monto", "dinero", "plata", "pesos", 
            "adjudicada", "adjudicado", "mayor valor", "mayor cuantía", "presupuesto", "recursos"
        ])

        # 1. Prórrogas / Adiciones de tiempo
        if any(term in p for term in ["prórroga", "prorroga", "adicion", "adición", "días adicionados", "dias adicionados"]):
            return (
                f"SELECT COUNT(*) AS total_con_adiciones, "
                f"ROUND(AVG(dias_adicionados), 1) AS promedio_dias_adicionados, "
                f"MAX(dias_adicionados) AS max_dias_adicionados, "
                f"ROUND(SUM(valor_del_contrato), 2) AS valor_total_adicionados "
                f"FROM contratos {where_base} AND dias_adicionados > 0;"
            )

        # 2. Modalidades de contratación
        if any(term in p for term in ["modalidad", "modalidades"]):
            limite = self._extraer_limite(p, default=5)
            orden = "valor_total DESC" if quiere_valor else "total_contratos DESC"
            return (
                f"SELECT modalidad_de_contratacion, COUNT(*) AS total_contratos, "
                f"ROUND(SUM(valor_del_contrato), 2) AS valor_total, "
                f"ROUND(AVG(valor_del_contrato), 2) AS valor_promedio "
                f"FROM contratos {where_base} "
                f"GROUP BY modalidad_de_contratacion "
                f"ORDER BY {orden} LIMIT {limite};"
            )

        # 3. Contratación directa específicamente
        if "directa" in p and not any(term in p for term in ["modalidades", "entidades", "top"]):
            return (
                f"SELECT COUNT(*) AS total_contratos_directa, "
                f"ROUND(SUM(valor_del_contrato), 2) AS valor_total, "
                f"ROUND(AVG(valor_del_contrato), 2) AS valor_promedio "
                f"FROM contratos {where_base} AND UPPER(modalidad_de_contratacion) LIKE '%DIRECTA%';"
            )

        # 4. Entidades con mayor cuantía / presupuesto / más contratos
        if any(term in p for term in ["entidad", "entidades", "alcaldía", "gobernación"]):
            limite = self._extraer_limite(p, default=5)
            orden = "valor_total DESC" if quiere_valor else "total_contratos DESC"
            return (
                f"SELECT nombre_entidad, COUNT(*) AS total_contratos, "
                f"ROUND(SUM(valor_del_contrato), 2) AS valor_total "
                f"FROM contratos {where_base} "
                f"GROUP BY nombre_entidad "
                f"ORDER BY {orden} LIMIT {limite};"
            )

        # 5. PYMES
        if "pyme" in p:
            return (
                f"SELECT es_pyme, COUNT(*) AS total_contratos, "
                f"ROUND(SUM(valor_del_contrato), 2) AS valor_total "
                f"FROM contratos {where_base} "
                f"GROUP BY es_pyme;"
            )

        # 6. Proveedores / Contratistas
        if any(term in p for term in ["proveedor", "contratista"]):
            limite = self._extraer_limite(p, default=5)
            orden = "valor_total DESC" if quiere_valor else "total_contratos DESC"
            return (
                f"SELECT proveedor_adjudicado, COUNT(*) AS total_contratos, "
                f"ROUND(SUM(valor_del_contrato), 2) AS valor_total "
                f"FROM contratos {where_base} AND proveedor_adjudicado IS NOT NULL AND proveedor_adjudicado != '' "
                f"GROUP BY proveedor_adjudicado "
                f"ORDER BY {orden} LIMIT {limite};"
            )

        # 7. Tipos de contrato (obra, consultoría, etc.)
        if any(term in p for term in ["tipo de contrato", "tipos de contrato", "obra", "servicio"]):
            limite = self._extraer_limite(p, default=5)
            orden = "valor_total DESC" if quiere_valor else "total_contratos DESC"
            return (
                f"SELECT tipo_de_contrato, COUNT(*) AS total_contratos, "
                f"ROUND(SUM(valor_del_contrato), 2) AS valor_total "
                f"FROM contratos {where_base} "
                f"GROUP BY tipo_de_contrato "
                f"ORDER BY {orden} LIMIT {limite};"
            )

        # Consulta general por defecto (totales globales)
        return (
            f"SELECT COUNT(*) AS total_contratos, "
            f"ROUND(SUM(valor_del_contrato), 2) AS valor_total, "
            f"ROUND(AVG(valor_del_contrato), 2) AS valor_promedio "
            f"FROM contratos {where_base};"
        )

    def ejecutar_sql_seguro(self, query_sql: str) -> tuple[pd.DataFrame, str]:
        """Ejecuta una consulta SQL SELECT en modo de solo lectura sobre la base de contratos."""
        return ejecutar_consulta_segura(query_sql, self.db_path)

    def buscar_normas(
        self,
        pregunta: str,
        top_k: int = 3,
        filtro_documento: str | None = None,
    ) -> list[dict[str, Any]]:
        """Recupera fragmentos normativos relevantes desde Qdrant con sus metadatos."""
        df_res = self.indexador.buscar_similares(
            pregunta=pregunta,
            top_k=top_k,
            filtro_documento=filtro_documento,
        )
        if df_res.empty:
            return []
        return df_res.to_dict(orient="records")

    def _sintetizar_respuesta_local(
        self,
        pregunta: str,
        tipo: str,
        fuentes: list[dict[str, Any]],
        df_sql: pd.DataFrame | None,
        sql_ejecutado: str | None,
    ) -> str:
        """Sintetiza una respuesta contextualizada, analítica y fluida sin mostrar código SQL técnico."""
        if tipo == "fuera_de_alcance":
            return (
                f"ℹ️ **Consulta fuera de alcance**: La pregunta *\"{pregunta}\"* no se relaciona con la contratación "
                "estatal colombiana, la normativa aplicable (Ley 80 de 1993, Ley 1150 de 2007, Decreto 1082 de 2015) "
                "ni con los registros de contratos públicos de SECOP II. Por principios de precisión y control "
                "de alucinaciones, el sistema orienta sus respuestas exclusivamente al ámbito de la compra pública."
            )

        lineas: list[str] = []
        p_lower = pregunta.lower()

        # =====================================================================
        # 1. SECCIÓN CUANTITATIVA (DATOS SECOP II)
        # =====================================================================
        if df_sql is not None and not df_sql.empty:
            cols = df_sql.columns.tolist()

            # Caso A: Prórrogas / Adiciones temporales
            if "total_con_adiciones" in cols:
                tot_ad = int(df_sql["total_con_adiciones"].iloc[0] or 0)
                prom_dias = float(df_sql["promedio_dias_adicionados"].iloc[0] or 0.0)
                max_dias = int(df_sql["max_dias_adicionados"].iloc[0] or 0)
                val_tot = float(df_sql["valor_total_adicionados"].iloc[0] or 0.0)

                lineas.append("### 📊 Análisis de Prórrogas y Modificaciones Temporales")
                lineas.append(
                    f"En el conjunto analizado de **50.000 contratos de SECOP II** para el departamento del Valle del Cauca, "
                    f"se identificaron **{tot_ad:,} contratos que requirieron adiciones de tiempo** (prórrogas posteriores a la firma).\n"
                )
                lineas.append(f"- **Plazo promedio adicionado:** {prom_dias:.1f} días por contrato sobre el cronograma inicial.")
                lineas.append(f"- **Extensión máxima registrada:** {max_dias:,} días adicionales en un solo proceso contractual.")
                lineas.append(f"- **Cuantía total comprometida en contratos prorrogados:** ${val_tot:,.2f} COP.\n")
                lineas.append(
                    "📌 **Contexto de Veeduría:** En la gestión contractual pública, las adiciones de plazo reiteradas suelen "
                    "reflejar demoras imprevistas en la entrega de terrenos, modificaciones de especificaciones técnicas o "
                    "ajustes en la etapa de planeación de los estudios previos."
                )

            # Caso B: Agrupación por Modalidad de Contratación
            elif "modalidad_de_contratacion" in cols:
                cant = len(df_sql)
                criterio = "mayor cuantía total adjudicada" if "cuant" in p_lower or "valor" in p_lower or "monto" in p_lower else "mayor volumen de contratos"
                lineas.append(f"### 📊 Modalidades de Contratación en el Valle del Cauca")
                lineas.append(
                    f"Con base en los registros del Observatorio, a continuación se presentan las **{cant} modalidades de contratación** "
                    f"con {criterio}:\n"
                )
                # Resumen contextual de los primeros lugares
                for i, (_, row) in enumerate(df_sql.iterrows(), start=1):
                    mod = row["modalidad_de_contratacion"]
                    tot_c = int(row.get("total_contratos", 0))
                    val_t = float(row.get("valor_total", 0.0))
                    val_p = float(row.get("valor_promedio", 0.0))
                    lineas.append(f"{i}. **{mod}**: Concentra **${val_t:,.2f} COP** a través de **{tot_c:,} contratos** (promedio: ${val_p:,.2f} COP).")

                lineas.append("\n**Consolidado de Datos:**")
                lineas.append(formatear_df_a_markdown(df_sql))
                lineas.append(
                    "\n📌 **Contexto de Veeduría:** La contratación directa y los regímenes especiales suelen representar "
                    "una alta concentración presupuestal y de volumen. La normativa exige que las causales de contratación "
                    "directa cuenten siempre con justificación técnica rigurosa."
                )

            # Caso C: Agrupación por Entidad Estatal
            elif "nombre_entidad" in cols:
                cant = len(df_sql)
                lineas.append("### 📊 Entidades con Mayor Contratación Pública")
                lineas.append(
                    f"De acuerdo con los contratos registrados en el Valle del Cauca, las **{cant} entidades** con mayor cuantía corresponden a:\n"
                )
                for i, (_, row) in enumerate(df_sql.iterrows(), start=1):
                    ent = row["nombre_entidad"]
                    tot_c = int(row.get("total_contratos", 0))
                    val_t = float(row.get("valor_total", 0.0))
                    lineas.append(f"{i}. **{ent}**: **${val_t:,.2f} COP** distribuidos en **{tot_c:,} contratos**.")

                lineas.append("\n**Consolidado de Datos:**")
                lineas.append(formatear_df_a_markdown(df_sql))
                lineas.append(
                    "\n📌 **Contexto de Veeduría:** Estas entidades concentran los mayores presupuestos de inversión "
                    "y funcionamiento territorial en sectores esenciales como educación, salud y bienestar social."
                )

            # Caso D: Tipo de Contrato
            elif "tipo_de_contrato" in cols:
                cant = len(df_sql)
                lineas.append(f"### 📊 Tipología Contractual en SECOP II")
                lineas.append(f"A continuación se detallan los **{cant} principales tipos de contrato** según su volumen y valor:\n")
                lineas.append(formatear_df_a_markdown(df_sql))

            # Caso E: Contratación Directa específica
            elif "total_contratos_directa" in cols:
                tot_dir = int(df_sql["total_contratos_directa"].iloc[0] or 0)
                val_dir = float(df_sql["valor_total"].iloc[0] or 0.0)
                val_prom = float(df_sql["valor_promedio"].iloc[0] or 0.0)
                lineas.append("### 📊 Balance de Contratación Directa")
                lineas.append(
                    f"En el departamento del Valle del Cauca se registran **{tot_dir:,} contratos suscritos bajo la modalidad de Contratación Directa**, "
                    f"con una cuantía total de **${val_dir:,.2f} COP** y un valor promedio por contrato de **${val_prom:,.2f} COP**.\n"
                )
                lineas.append(
                    "📌 **Contexto de Veeduría:** Esta modalidad se aplica predominantemente en contratos de prestación "
                    "de servicios profesionales y de apoyo a la gestión, así como en convenios interadministrativos."
                )

            # Caso F: Totales generales o genéricos
            else:
                lineas.append("### 📊 Cifras del Observatorio (SECOP II)")
                lineas.append(formatear_df_a_markdown(df_sql))

        # =====================================================================
        # 2. SECCIÓN NORMATIVA (MARCO JURÍDICO EXPLICADO)
        # =====================================================================
        if fuentes:
            if lineas:
                lineas.append("\n---\n")

            # Detectar temas normativos frecuentes para generar síntesis sustantiva
            if any(term in p_lower for term in ["urgencia manifiesta", "urgencia"]):
                lineas.append("### ⚖️ Marco y Requisitos de la Urgencia Manifiesta")
                lineas.append(
                    "La **urgencia manifiesta** es una causal extraordinaria de contratación directa regulada por el "
                    "**artículo 42 de la Ley 80 de 1993** y el **Decreto 1082 de 2015**. Se concibe como una excepción al "
                    "deber de licitación pública cuando la continuidad de un servicio esencial o situaciones de desastre "
                    "y fuerza mayor impiden adelantar los plazos de una convocatoria pública ordinaria.\n"
                )
                lineas.append(
                    "**Causales y Requisitos Esenciales:**\n"
                    "1. **Situación Inaplazable:** Hechos de calamidad, fuerza mayor, desastres o situaciones imprevistas que comprometan de forma inmediata el servicio público.\n"
                    "2. **Acto Administrativo Motivado:** La entidad debe expedir un acto administrativo que declare formalmente la urgencia manifiesta; este acto sustituye la elaboración previa de estudios de mercado y pliegos ordinarios.\n"
                    "3. **Control Posterior Obligatorio:** La entidad tiene la obligación legal de enviar inmediatamente el acto y los contratos suscritos a la Contraloría territorial o General para su auditoría y control de legalidad posterior."
                )
            elif any(term in p_lower for term in ["contratación directa", "contratacion directa", "causales de contratación directa"]):
                lineas.append("### ⚖️ Marco Legal y Causales de Contratación Directa")
                lineas.append(
                    "La **Ley 1150 de 2007 (artículo 2, numeral 4)** y el **Decreto 1082 de 2015** delimitan taxativamente "
                    "las circunstancias en que las entidades estatales pueden contratar sin licitación o convocatoria pública previa:\n"
                )
                lineas.append(
                    "- **Urgencia manifiesta:** Para atender contingencias o calamidades inaplazables.\n"
                    "- **Contratos y convenios interadministrativos:** Entre entidades públicas, respetando las excepciones de ley.\n"
                    "- **Prestación de servicios profesionales y apoyo a la gestión:** Con personas naturales o jurídicas idóneas.\n"
                    "- **Bienes o servicios con proveedor exclusivo:** Titularidad de patentes o derechos de autor exclusivos.\n"
                    "- **Arrendamiento o adquisición de inmuebles:** Previa justificación de conveniencia y avalúo técnico.\n"
                    "- **Créditos y empréstitos:** Con entidades financieras autorizadas."
                )
            elif any(term in p_lower for term in ["capacidad residual", "k de contratacion", "k de contratación"]):
                lineas.append("### ⚖️ Capacidad Residual (K de Contratación)")
                lineas.append(
                    "Regulada por el **Decreto 1082 de 2015** y los manuales de Colombia Compra Eficiente, la **capacidad residual** "
                    "mide la aptitud real que tiene un contratista para asumir nuevas obras públicas considerando sus compromisos contractuales vigentes.\n"
                )
                lineas.append(
                    "- **Factores evaluados:** Experiencia en obra, capacidad financiera (liquidez, endeudamiento), capacidad técnica (personal) y saldos de contratos en ejecución."
                )
            elif any(term in p_lower for term in ["mínima cuantía", "minima cuantia"]):
                lineas.append("### ⚖️ Procedimiento de Selección de Mínima Cuantía")
                lineas.append(
                    "Aplica para adquisiciones que no superen el 10% de la menor cuantía de la entidad (Ley 1150 de 2007, Ley 1474 de 2011, Decreto 1082 de 2015).\n"
                    "- **Regla de Adjudicación:** Se adjudica exclusivamente al **menor precio**, verificando únicamente el cumplimiento de los requisitos habilitantes."
                )
            else:
                lineas.append("### ⚖️ Fundamento Normativo y Legal")
                lineas.append(
                    "A continuación se presenta el marco regulatorio aplicable identificado en el corpus jurídico "
                    "de la contratación pública en Colombia:\n"
                )

            # Citas de fuentes con trazabilidad limpia
            lineas.append("\n**Disposiciones Legales Citadas:**")
            for f in fuentes:
                score = f.get("score_coseno", 0.0)
                doc = f.get("documento", "Normativa")
                art = f.get("articulo", "General")
                tipo_f = f.get("tipo_fuente", "Marco Legal")
                texto = f.get("texto", "").strip().replace("\n", " ")
                resumen_texto = texto[:320] + "..." if len(texto) > 320 else texto

                lineas.append(f"- **{doc}** | *{art}* ({tipo_f}) — Relevancia: `{score:.4f}`")
                lineas.append(f"  > \"{resumen_texto}\"")

        if not lineas:
            return (
                "No se encontraron registros ni disposiciones legales específicas para responder a tu consulta. "
                "Por favor intenta reformular tu pregunta o verificar los filtros aplicados."
            )

        return "\n".join(lineas)

    def _responder_local(
        self,
        pregunta: str,
        filtro_documento: str | None = None,
        top_k: int = 3,
        query_sql_manual: str | None = None,
    ) -> RespuestaAsistente:
        """Ejecuta la respuesta 100% de manera local y determinística."""
        t0 = time.time()
        tipo = self.clasificar_consulta(pregunta)

        fuentes: list[dict[str, Any]] = []
        df_sql: pd.DataFrame | None = None
        sql_ejecutado: str | None = None

        if tipo == "fuera_de_alcance":
            latencia = round(time.time() - t0, 3)
            return RespuestaAsistente(
                respuesta=self._sintetizar_respuesta_local(pregunta, tipo, [], None, None),
                tipo_consulta=tipo,
                latencia_segundos=latencia,
                modo_utilizado="local",
            )

        # Recuperar normas si es normativa o mixta
        if tipo in ("normativa", "mixta"):
            fuentes = self.buscar_normas(pregunta, top_k=top_k, filtro_documento=filtro_documento)
            # Validar si el puntaje más alto es extremadamente bajo (alucinación / no match)
            if fuentes and fuentes[0].get("score_coseno", 0.0) < self.umbral_fuera_de_alcance and tipo == "normativa":
                tipo = "fuera_de_alcance"
                fuentes = []

        # Ejecutar SQL si es cuantitativa o mixta
        if tipo in ("cuantitativa", "mixta"):
            sql_query = query_sql_manual or self.generar_sql_local(pregunta)
            try:
                df_sql, sql_ejecutado = self.ejecutar_sql_seguro(sql_query)
            except Exception as e:
                logger.error("Error ejecutando SQL local: %s", e)
                if not self.db_path.exists():
                    respuesta_sin_db = (
                        "⚠️ **Base de datos de contratos no disponible en este entorno.**\n\n"
                        "Los datos de SECOP II se generan ejecutando el notebook localmente. "
                        "En este despliegue solo está disponible la consulta normativa (RAG).\n\n"
                        "Puedes preguntar sobre leyes, decretos y guías de contratación pública."
                    )
                    fuentes = self.buscar_normas(pregunta, top_k=top_k, filtro_documento=filtro_documento)
                    latencia = round(time.time() - t0, 3)
                    return RespuestaAsistente(
                        respuesta=respuesta_sin_db,
                        tipo_consulta="normativa",
                        latencia_segundos=latencia,
                        fuentes_normativas=fuentes,
                        modo_utilizado="local",
                    )
                df_sql = pd.DataFrame([{"error": str(e)}])
                sql_ejecutado = sql_query

        respuesta_texto = self._sintetizar_respuesta_local(pregunta, tipo, fuentes, df_sql, sql_ejecutado)
        latencia = round(time.time() - t0, 3)

        return RespuestaAsistente(
            respuesta=respuesta_texto,
            tipo_consulta=tipo,
            sql_ejecutado=sql_ejecutado,
            datos_sql=df_sql.to_dict(orient="records") if df_sql is not None else None,
            fuentes_normativas=fuentes,
            latencia_segundos=latencia,
            modo_utilizado="local",
        )

    def _responder_con_gemini(
        self,
        pregunta: str,
        filtro_documento: str | None = None,
        top_k: int = 3,
        query_sql_manual: str | None = None,
    ) -> RespuestaAsistente:
        """Responde utilizando Gemini para enrutamiento y síntesis inteligente con fallback a local."""
        t0 = time.time()
        tipo = self.clasificar_consulta(pregunta)

        if self.gemini_client is None:
            return self._responder_local(pregunta, filtro_documento, top_k, query_sql_manual)

        try:
            from google.genai import types

            fuentes: list[dict[str, Any]] = []
            df_sql: pd.DataFrame | None = None
            sql_ejecutado: str | None = None

            # Recuperar RAG si corresponde
            if tipo in ("normativa", "mixta"):
                fuentes = self.buscar_normas(pregunta, top_k=top_k, filtro_documento=filtro_documento)
                if fuentes and fuentes[0].get("score_coseno", 0.0) < self.umbral_fuera_de_alcance and tipo == "normativa":
                    tipo = "fuera_de_alcance"
                    fuentes = []

            # Ejecutar SQL si corresponde
            if tipo in ("cuantitativa", "mixta"):
                sql_query = query_sql_manual or self.generar_sql_local(pregunta)
                df_sql, sql_ejecutado = self.ejecutar_sql_seguro(sql_query)

            # Preparar contexto para la síntesis de Gemini
            contexto_partes = []
            if fuentes:
                contexto_partes.append("### FRAGMENTOS NORMATIVOS RECUPERADOS (RAG):")
                for f in fuentes:
                    contexto_partes.append(
                        f"- Documento: {f.get('documento')} | Artículo: {f.get('articulo')} | Fuente: {f.get('tipo_fuente')}\n"
                        f"  Texto: {f.get('texto')}"
                    )

            if df_sql is not None and not df_sql.empty:
                contexto_partes.append("### RESULTADOS DE BASE DE DATOS (SECOP II SQL):")
                contexto_partes.append(f"SQL: {sql_ejecutado}")
                contexto_partes.append(df_sql.to_string(index=False))

            contexto_str = "\n\n".join(contexto_partes)

            prompt_sistema = (
                "Eres el Asistente Oficial del Observatorio Ciudadano de Contratación Pública (SECOP II Colombia).\n"
                "Tu misión es responder con máxima claridad, precisión y contexto analítico a ciudadanos y veedurías.\n"
                "REGLAS ESTRICTAS DE RESPUESTA:\n"
                "1. NUNCA muestres código SQL, sintaxis de consulta técnica ni frases como 'Consulta analítica ejecutada: SELECT...'. "
                "El ciudadano debe recibir exclusivamente explicaciones claras, contextualizadas y datos legibles.\n"
                "2. NO te limites a arrojar una tabla fría o copiar fragmentos crudos de la norma: EXPLICA detalladamente el significado "
                "de los datos, las implicaciones para la veeduría y el marco jurídico que los sustenta.\n"
                "3. Si la consulta pide un límite específico (ej: 'las 5 modalidades' o 'las 5 entidades'), enfoca tu explicación exactamente en ese número de elementos.\n"
                "4. Cita siempre con precisión la norma y el artículo correspondiente (ej: Ley 80 de 1993, Decreto 1082 de 2015, Guías CCE).\n"
                "5. Si la pregunta está fuera de alcance (no trata sobre contratación estatal, leyes colombianas o SECOP II), "
                "declina amablemente responder explicando el alcance del observatorio sin inventar información.\n"
                "6. Responde en español formal, estructurado con subtítulos claros y viñetas en Markdown."
            )

            prompt_usuario = (
                f"PREGUNTA DEL CIUDADANO: {pregunta}\n\n"
                f"TIPO DETECTADO: {tipo}\n\n"
                f"{contexto_str if contexto_str else 'No se dispone de datos adicionales.'}\n\n"
                "Por favor elabora la respuesta final integrando las fuentes anteriores."
            )

            config = types.GenerateContentConfig(
                system_instruction=prompt_sistema,
                temperature=0.2,
            )

            response = self.gemini_client.models.generate_content(
                model=self.modelo_nombre,
                contents=prompt_usuario,
                config=config,
            )

            respuesta_texto = response.text or ""
            latencia = round(time.time() - t0, 3)

            return RespuestaAsistente(
                respuesta=respuesta_texto,
                tipo_consulta=tipo,
                sql_ejecutado=sql_ejecutado,
                datos_sql=df_sql.to_dict(orient="records") if df_sql is not None else None,
                fuentes_normativas=fuentes,
                latencia_segundos=latencia,
                modo_utilizado="gemini",
            )

        except Exception as e:
            logger.warning(
                "Error en llamada a Gemini (%s). Activando fallback automático a síntesis local.", e
            )
            resp = self._responder_local(pregunta, filtro_documento, top_k, query_sql_manual)
            resp.modo_utilizado = "gemini_fallback_a_local"
            return resp

    def responder(
        self,
        pregunta: str,
        filtro_documento: str | None = None,
        top_k: int | None = None,
        query_sql_manual: str | None = None,
    ) -> RespuestaAsistente:
        """
        Punto de entrada principal para responder a una consulta ciudadana.

        Args:
            pregunta: Pregunta en lenguaje natural del usuario.
            filtro_documento: Filtro opcional por documento normativo (ej: 'Ley 80 de 1993').
            top_k: Cantidad de fragmentos a recuperar (por defecto self.top_k_default).
            query_sql_manual: Consulta SQL específica a ejecutar si se desea sobreescribir la automática.

        Returns:
            RespuestaAsistente con la respuesta formateada, fuentes, datos SQL y latencia.
        """
        k = top_k if top_k is not None else self.top_k_default

        if self.usar_local:
            return self._responder_local(
                pregunta=pregunta,
                filtro_documento=filtro_documento,
                top_k=k,
                query_sql_manual=query_sql_manual,
            )

        return self._responder_con_gemini(
            pregunta=pregunta,
            filtro_documento=filtro_documento,
            top_k=k,
            query_sql_manual=query_sql_manual,
        )
