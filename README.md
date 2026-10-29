# Observatorio Ciudadano de Contratación Pública (SECOP II)

**Inteligencia Artificial y Datos Abiertos para Consultar Contratos Estatales, Contrastar la Ley y Estimar el Riesgo de Prórrogas**

---

## ¿Por qué nace este proyecto?

En Colombia, la contratación pública representa uno de los principales canales de ejecución del presupuesto estatal. Aunque el portal **SECOP II** publica la información como datos abiertos de forma diaria, enfrentarse a millones de filas, decenas de variables técnicas y un marco jurídico extenso hace que responder preguntas sencillas o detectar contratos que requieren seguimiento sea una tarea compleja para ciudadanos, veedurías y periodistas de datos.

Este proyecto construye un **Observatorio Ciudadano de Contratación Pública** que transforma esos datos abiertos y la normativa vigente en dos herramientas accesibles desde una misma aplicación interactiva:

| Herramienta | ¿Qué permite hacer? | Tecnologías principales |
| :--- | :--- | :--- |
| **A. Asistente Híbrido (RAG + SQL)** | Responder preguntas en lenguaje cotidiano combinando cifras reales de contratos (**SQLite**) con artículos exactos de la ley y manuales oficiales (**Qdrant Cloud**), citando siempre la fuente. | `SQLite`, `Qdrant Cloud`, `Gemini Embedding 2`, `LangChain`, `Streamlit` |
| **B. Predictor de Riesgo de Prórrogas (ML)** | Estimar, con la información disponible el día en que se firma un contrato, la probabilidad de que requiera una prórroga de plazo (`dias_adicionados > 0`) para priorizar su revisión preventiva. | `scikit-learn`, `pandas`, `joblib`, `plotly`, `Streamlit` |

> ⚠️ **Uso responsable:** Los resultados de este observatorio muestran patrones estadísticos orientativos para apoyar la revisión humana. **No constituyen evidencia de irregularidades, incumplimientos ni corrupción.** Cualquier hallazgo debe contrastarse directamente en el expediente electrónico oficial a través del enlace `urlproceso`.

---

## Organización del Proyecto

```text
observatorio_secop_ii_desarrollo/
├── .env.example                          # Plantilla de configuración (variables de entorno)
├── FLUJO_DE_TRABAJO.md                   # Guía de cómo se conectan los módulos y etapas
├── requirements.txt                      # Librerías necesarias para ejecutar el proyecto
├── pyproject.toml                        # Configuración del paquete interno `observatorio`
│
├── data/
│   ├── corpus_rag_normativo/             # Leyes, decretos y guías de Colombia Compra Eficiente
│   │   ├── 01_leyes/                     # Ley 80/1993, Ley 1150/2007 y Ley 1712/2014
│   │   ├── 02_decretos_y_regulaciones/   # Decreto 1082/2015 y Circular Externa Única CCE
│   │   ├── 03_guias_y_manuales_cce/      # Diccionario de Datos, Manual de Datos Abiertos y Guías SECOP II
│   │   └── 04_markdown_procesado/        # Textos normativos estructurados para búsqueda semántica
│   ├── raw/                              # Datos originales descargados desde la API de datos.gov.co
│   ├── processed/                        # Datos limpios (CSV y base SQLite) sin información personal
│   └── evaluation/                       # Banco de preguntas para validar la precisión del asistente
│
├── models/
│   ├── pipeline_prorrogas.joblib         # Modelo entrenado listo para usar en la aplicación
│   ├── model_metadata.json               # Métricas de desempeño y parámetros de referencia
│   └── MODEL_CARD.md                     # Ficha de transparencia, alcances y límites del modelo
│
├── notebooks/
│   └── observatorio_secop_ii_desarrollo.ipynb # Desarrollo paso a paso: datos, RAG y Machine Learning
│
├── src/
│   └── observatorio/                     # Módulos de Python reutilizados por el Notebook y la App
│       ├── config.py                     # Rutas y configuración general
│       ├── data/                         # Descarga desde API Socrata, limpieza y base SQLite
│       ├── rag/                          # Fragmentación de leyes, vectores en Qdrant y asistente
│       └── ml/                           # Selección de variables, entrenamiento y predicción
│
├── apps/
│   ├── Home.py                           # Aplicación principal en Streamlit
│   ├── rag_app.py                        # Vista del Asistente de Consulta (Chat RAG + SQL)
│   ├── ml_app.py                         # Vista de Exploración y Simulador de Prórrogas
│   └── ui_utils.py                       # Elementos visuales y avisos de atribución
│
└── tests/                                # Pruebas automatizadas de seguridad y calidad de datos
```

---

## Cómo Ejecutarlo en tu Equipo

1. **Crear y activar el entorno virtual:**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   python -m pip install -e .
   ```

2. **Configurar tus credenciales:**
   Copia el archivo `.env.example` como `.env` y agrega tus claves gratuitas de **Google AI Studio (`GEMINI_API_KEY`)** y **Qdrant Cloud (`QDRANT_URL`, `QDRANT_API_KEY`)**.

3. **Lanzar la aplicación web:**
   ```powershell
   python -m streamlit run apps/Home.py
   ```

---

## Fuente de Datos y Licencia (CC BY-SA 4.0)

* **Código del proyecto:** Distribuido bajo licencia **MIT** (ver [LICENSE](LICENSE)).
* **Datos abiertos y derivados:**
  > Datos originarios de *«SECOP II – Contratos Electrónicos»*, publicados por Colombia Compra Eficiente (Agencia Nacional de Contratación Pública) en el Portal Nacional de Datos Abiertos (`https://www.datos.gov.co/Estad-sticas-Nacionales/SECOP-II-Contratos-Electr-nicos/jbjy-vk9h`). Licencia: **CC BY-SA 4.0** (`https://creativecommons.org/licenses/by-sa/4.0/`). Los datos fueron filtrados por departamento y periodo, depurados para proteger datos personales y estructurados para análisis estadístico. Este proyecto es una iniciativa ciudadana e independiente y **no está afiliado ni respaldado por Colombia Compra Eficiente**.
