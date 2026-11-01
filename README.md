# Observatorio Ciudadano de Contratación Pública (SECOP II)

**Inteligencia Artificial y Datos Abiertos para Consultar Contratos Estatales, Contrastar la Ley y Estimar el Riesgo de Prórrogas**

---

## ¿Por qué nace este proyecto?

En Colombia, la contratación pública representa uno de los principales canales de ejecución del presupuesto estatal. Aunque el portal **SECOP II** publica la información como datos abiertos de forma diaria, enfrentarse a millones de filas, decenas de variables técnicas y un marco jurídico extenso hace que responder preguntas sencillas o detectar contratos que requieren seguimiento sea una tarea compleja para ciudadanos, veedurías y periodistas de datos.

Este proyecto construye un **Observatorio Ciudadano de Contratación Pública** que transforma esos datos abiertos y la normativa vigente en dos herramientas accesibles desde una misma aplicación interactiva:

| Herramienta | ¿Qué permite hacer? | Tecnologías principales |
| :--- | :--- | :--- |
| **A. Asistente Híbrido (RAG + SQL)** | Responder preguntas en lenguaje cotidiano combinando cifras reales de contratos (**SQLite**) con artículos exactos de la ley y manuales oficiales (**Qdrant Cloud / Parquet Local**), citando siempre la fuente y operando en modo local o en la nube con Gemini. | `SQLite`, `Qdrant Cloud`, `Gemini Flash`, `sentence-transformers`, `Streamlit` |
| **B. Predictor de Riesgo de Prórrogas (ML)** | Estimar, con la información disponible exclusivamente el día en que se firma un contrato, la probabilidad de que requiera una prórroga de plazo (`dias_adicionados > 0`) para priorizar la revisión preventiva sin incurrir en fuga de datos. | `scikit-learn`, `HistGradientBoosting`, `pandas`, `joblib`, `Streamlit` |

> **Protocolo de Uso Responsable:** Los resultados de este observatorio describen patrones estadísticos agregados para orientar la labor de veeduría y control social. **No constituyen imputación de irregularidad, juicio de responsabilidad fiscal ni indicio penal.** Todo análisis debe ser contrastado en el expediente electrónico oficial a través del enlace `urlproceso` de SECOP II.

---

## Organización del Proyecto

Siguiendo el principio de arquitectura limpia, **la lógica de negocio, procesamiento, modelado y validación reside en módulos `.py`**, mientras que los notebooks y la interfaz actúan como desencadenadores orquestados:

```text
observatorio_secop_ii_desarrollo/
├── .env.example                          # Variables de entorno de referencia
├── requirements.txt                      # Dependencias del proyecto
├── pyproject.toml                        # Metadatos del paquete instalable `observatorio`
├── MODEL_CARD.md                         # Ficha técnica formal del modelo (Mitchell et al.)
│
├── data/
│   ├── corpus_rag_normativo/             # Leyes, decretos y guías de Colombia Compra Eficiente
│   │   ├── 01_leyes/                     # Ley 80/1993, Ley 1150/2007 y Ley 1712/2014
│   │   ├── 02_decretos_y_regulaciones/   # Decreto 1082/2015 y regulaciones CCE
│   │   ├── 03_guias_y_manuales_cce/      # Manuales de Mínima Cuantía, Supervisión, etc.
│   │   └── 04_markdown_procesado/        # Textos normativos procesados y etiquetados
│   ├── raw/                              # Dataset crudo descargado vía Socrata
│   ├── processed/                        # Base SQLite indexada y respaldo de embeddings Parquet
│   └── evaluation/                       # Evaluaciones y resultados
│
├── models/
│   ├── pipeline_prorrogas.joblib         # Pipeline scikit-learn entrenado para producción
│   └── model_metadata.json               # Métricas de prueba, períodos y parámetros
│
├── notebooks/
│   └── observatorio_secop_ii_desarrollo.ipynb # Notebook ejecutor y narrativa metodológica
│
├── src/
│   └── observatorio/                     # Código fuente modular
│       ├── config.py                     # Configuración central y rutas
│       ├── data/                         # Descarga, limpieza anonimizada y SQLite
│       │   ├── ingestion.py
│       │   ├── cleaning.py
│       │   └── database.py
│       ├── rag/                          # Chunking, vectorstore Qdrant/local, orquestador y evaluación
│       │   ├── chunking.py
│       │   ├── vectorstore.py
│       │   ├── assistant.py
│       │   └── evaluation.py
│       └── ml/                           # Preprocesamiento, pipelines, evaluación e inferencia
│           ├── features.py
│           ├── pipeline.py
│           ├── evaluation.py
│           └── inference.py
│
├── apps/                                 # Aplicación web Streamlit (diseño editorial sobrio)
│   ├── Home.py                           # Navegación principal
│   ├── rag_app.py                        # Componente A: Chat RAG + SQL
│   ├── ml_app.py                         # Componente B: Contexto, Explorador y Simulador ML
│   └── ui_utils.py                       # Estilos CSS minimalistas y avisos
│
└── tests/                                # Suite de pruebas automatizadas con pytest
    ├── test_no_leakage.py                # Auditoría de ausencia de fuga post-firma
    ├── test_sql_safety.py                # Verificación de modo solo lectura y bloqueo de inyecciones
    ├── test_assistant.py                 # Pruebas del orquestador y banco de preguntas
    └── test_ml_pipeline.py               # Pruebas del preprocesador e inferencia unitaria
```

---

## Cómo Ejecutar el Proyecto

### 1. Entorno virtual e instalación

```bash
# Crear y activar entorno virtual
python3 -m venv .venv
source .venv/bin/activate       # En Windows: .\.venv\Scripts\Activate.ps1

# Actualizar pip e instalar dependencias y el paquete en modo editable
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

### 2. Variables de entorno

Copia la plantilla y edita tus credenciales:
```bash
cp .env.example .env
```
> **Nota de Autonomía:** Si no configuras llaves de API o se agota la cuota gratuita, el proyecto cuenta con **modo 100% local**: realiza búsqueda vectorial sobre el respaldo en Parquet con `sentence-transformers` y ejecuta consultas analíticas en SQLite sin costo ni conexión externa.

### 3. Ejecutar pruebas automatizadas

```bash
pytest tests/
```

### 4. Lanzar la aplicación web interactiva

```bash
streamlit run apps/Home.py
```

---

## Procedencia de Datos y Análisis de Riesgos de Publicación

### Procedencia y Marco Legal
* **Fuente de Datos:** Catálogo oficial *«SECOP II – Contratos Electrónicos»*, publicado por la Agencia Nacional de Contratación Pública (Colombia Compra Eficiente) en el portal del Estado colombiano [datos.gov.co](https://www.datos.gov.co/Estad-sticas-Nacionales/SECOP-II-Contratos-Electr-nicos/jbjy-vk9h) bajo el identificador API `jbjy-vk9h`.
* **Licencia de Uso:** Licencia internacional pública [Creative Commons Atribución-CompartirIgual 4.0 (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).
* **Marco de Transparencia:** Los contratos estatales y sus documentos anexos son de naturaleza y acceso público en virtud de la **Ley 1712 de 2014 (Ley de Transparencia y Acceso a la Información Pública Nacional)**.

### Evaluación y Mitigación de Riesgos al Publicar
1. **Protección de Datos Personales (Ley 1581 de 2012):** Aunque los contratistas del Estado son sujetos de escrutinio público, el proceso de limpieza anonimiza de forma determinística los documentos de identidad de personas naturales (cédulas de ciudadanía, extranjería o tarjetas de identidad) sustituyéndolos por identificadores ofuscados (`CC-ANONIMIZADO-XXXX`). Se descartan desde el origen números de cuenta bancaria, correos personales o datos sensibles.
2. **Prevención de Prejuzgamiento o Difamación:** El modelo predictivo de prórrogas calcula una propensión estadística multifactorial al momento de la firma. **No constituye imputación de irregularidad, juicio de responsabilidad fiscal ni indicio penal.** La aplicación incluye permanentemente advertencias de uso responsable y enlaces directos al expediente electrónico oficial (`urlproceso`) para contrastar cualquier hallazgo.
3. **Seguridad e Inmutabilidad de Datos:** El motor analítico ejecuta consultas sobre SQLite configurado estrictamente en modo de solo lectura (`?mode=ro`). Las sentencias generadas pasan por un filtro que bloquea comandos de mutación (`DROP`, `DELETE`, `UPDATE`, `ALTER`) e impone límites máximos de filas.

---

## Documentación y Publicaciones Complementarias

| Documento | Descripción |
| :--- | :--- |
| **[`MODEL_CARD.md`](MODEL_CARD.md)** | Ficha técnica formal del modelo predictivo según el estándar de Mitchell et al. (arquitectura, métricas, sesgos y consideraciones éticas). |
| **[`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md)** | Guía paso a paso para desplegar la aplicación de forma gratuita en **Streamlit Community Cloud** o **Hugging Face Spaces** para exhibir en portafolio. |
| **[`BLOG_POST.md`](BLOG_POST.md)** | Artículo técnico y metodológico en profundidad en español, listo para publicar en blog personal, Medium o Dev.to. |
| **[`BLOG_POST_EN.md`](BLOG_POST_EN.md)** | Versión completa en inglés del artículo técnico y metodológico (Technical Blog Post / Paper). |
| **[`LINKEDIN_POST.md`](LINKEDIN_POST.md)** | Publicación optimizada para LinkedIn con gancho profesional, síntesis técnica, métricas verificables y hashtags estratégicos. |

---

## Fuente de Datos y Licencia

* **Datos Abiertos:** Datos originarios de *«SECOP II – Contratos Electrónicos»*, Colombia Compra Eficiente ([datos.gov.co](https://www.datos.gov.co/Estad-sticas-Nacionales/SECOP-II-Contratos-Electr-nicos/jbjy-vk9h)), bajo licencia CC BY-SA 4.0.
* **Código Fuente:** Distribuido bajo licencia **MIT** (ver [LICENSE](LICENSE)).
