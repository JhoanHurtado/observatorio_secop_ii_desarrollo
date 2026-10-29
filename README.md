# 🏛️ Observatorio Ciudadano de Contratación Pública (SECOP II)

**Asistente Híbrido en la Nube (RAG + SQL) y Modelo de Machine Learning Clásico sobre Datos Abiertos de Contratación Estatal en Colombia**

---

## 🎯 Descripción del Proyecto

La contratación pública concentra una parte fundamental del presupuesto estatal, pero el volumen del dataset abierto de **SECOP II** (millones de registros y 87 columnas) junto con la complejidad del marco jurídico colombiano dificultan la consulta ciudadana.

Este proyecto construye un **Observatorio Ciudadano de Contratación Pública** dividido en dos componentes complementarios que comparten una misma fuente de datos curada:

| Componente | Qué resuelve | Stack Tecnológico |
| :--- | :--- | :--- |
| **A. Asistente en la Nube (RAG + SQL)** | Responde preguntas en lenguaje natural combinando cifras exactas (**SQLite**) y normativa vigente (**Qdrant Cloud**), citando artículos y fuentes verificables. | `SQLite`, `Qdrant Cloud`, `Gemini Embedding 2` (768 dim), `LangChain Splitters`, `Streamlit` |
| **B. Machine Learning Clásico** | Estima al momento de la firma la probabilidad de que un contrato requiera **prórroga de plazo** (`dias_adicionados > 0`), sin fuga de información y con validación temporal. | `scikit-learn`, `pandas`, `joblib`, `plotly`, `Streamlit` |

> ⚠️ **Aviso de Uso Responsable:** Los resultados de este sistema describen patrones estadísticos e informativos para priorizar la revisión humana. **No constituyen evidencia de irregularidades, incumplimientos ni corrupción.** Toda alerta debe verificarse en el expediente electrónico oficial mediante el enlace `urlproceso`.

---

## 📂 Estructura del Repositorio

```text
observatorio_secop_ii_desarrollo/
├── .env.example                          # Plantilla de variables de entorno (sin claves)
├── requirements.txt                      # Dependencias con versiones fijas
├── pyproject.toml                        # Configuración del paquete instalable `observatorio`
├── observatorio_secop_ii_desarrollo.ipynb # Notebook maestro de desarrollo y experimentación
│
├── data/
│   ├── corpus_normativo/                 # Ley 80/1993, Ley 1150/2007 y Decreto 1082/2015 en Markdown
│   ├── raw/                              # Descargas crudas vía API Socrata
│   ├── processed/                        # Base SQLite limpia (`secop_contratos.sqlite`) y embeddings
│   └── evaluation/                       # Banco de 10-15 preguntas de validación RAG
│
├── models/
│   ├── pipeline_prorrogas.joblib         # Pipeline scikit-learn serializado
│   ├── model_metadata.json               # Metadatos, umbrales y métricas en prueba temporal
│   └── MODEL_CARD.md                     # Ficha técnica del modelo (RF-ML8)
│
├── src/
│   └── observatorio/                     # Paquete modular compartido entre Notebook y Streamlit
│       ├── config.py                     # Variables de entorno, rutas y semillas de reproducibilidad
│       ├── data/                         # Ingesta API Socrata, limpieza PII y SQLite seguro
│       ├── rag/                          # Chunking por artículo, Qdrant Cloud y orquestador RAG+SQL
│       └── ml/                           # Selección de variables sin leakage, pipeline e inferencia
│
├── apps/
│   ├── Home.py                           # Punto de entrada principal de la aplicación Streamlit
│   ├── rag_app.py                        # Interfaz del Asistente RAG + SQL
│   ├── ml_app.py                         # Interfaz de Exploración y Predicción de Prórrogas (4 pestañas)
│   └── ui_utils.py                       # Componentes visuales, avisos legales y control de sesión
│
└── tests/                                # Pruebas unitarias de seguridad SQL y prevención de leakage
```

---

## 🚀 Instalación y Ejecución Local

1. **Clonar el repositorio y crear el entorno virtual:**
   ```bash
   python -m venv .venv
   # En Windows (PowerShell):
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   pip install -e .
   ```

2. **Configurar las variables de entorno:**
   ```bash
   cp .env.example .env
   # Edita .env con tus claves de GEMINI_API_KEY y QDRANT_API_KEY
   ```

3. **Ejecutar la aplicación Streamlit:**
   ```bash
   streamlit run apps/Home.py
   ```

4. **Ejecutar las pruebas de seguridad e integridad:**
   ```bash
   pytest
   ```

---

## 📜 Licencia y Atribución de Datos (CC BY-SA 4.0)

* **Código fuente:** Distribuido bajo licencia **MIT** (ver archivo `LICENSE`).
* **Datos derivados:**
  > Datos originarios de *«SECOP II – Contratos Electrónicos»*, Colombia Compra Eficiente (Agencia Nacional de Contratación Pública), Portal Nacional de Datos Abiertos (`https://www.datos.gov.co/Estad-sticas-Nacionales/SECOP-II-Contratos-Electr-nicos/jbjy-vk9h`). Licencia: **CC BY-SA 4.0** (`https://creativecommons.org/licenses/by-sa/4.0/`). Modificaciones: filtrado departamental y temporal, limpieza de datos personales y generación de variables derivadas. Este proyecto es ciudadano e independiente y **no está afiliado ni respaldado por Colombia Compra Eficiente**.

