# Notebooks del Observatorio SECOP II

El proyecto ofrece dos modalidades de ejecución en notebooks interactivos:

---

### 1. Cuaderno Principal Integrado
- **[`observatorio_secop_ii_desarrollo.ipynb`](observatorio_secop_ii_desarrollo.ipynb):**
  Cuaderno maestro unificado con la narrativa completa de extremo a extremo:
  - **Parte 1:** Ingesta de datos, anonimización y base de datos relacional SQLite.
  - **Parte 2:** Corpus normativo, chunking, indexación vectorial (Qdrant/Local) y asistente híbrido con evaluación.
  - **Parte 3 y 4:** Modelo predictivo de riesgo de prórroga (ML clásico), comparación, explicabilidad y empaquetado.

---

### 2. Cuadernos Modulares por Etapa
Para experimentación modular o ejecución por componentes:

1. **[`01_ingesta_y_sqlite.ipynb`](01_ingesta_y_sqlite.ipynb):**
   - Descarga vía API Socrata (`datos.gov.co`).
   - Anonimización estricta de documentos de personas naturales (CC/TI/CE).
   - Generación de `data/processed/secop_contratos.sqlite` con índices en columnas clave.

2. **[`02_rag_normativo.ipynb`](02_rag_normativo.ipynb):**
   - Conversión de 16 documentos jurídicos de PDF a Markdown estructurado con metadatos.
   - Evaluación comparativa de estrategias de fragmentación (chunking).
   - Indexación semántica en Qdrant Cloud / Parquet local con prefijos oficiales y fallback.
   - Conexión de consultas SQL seguras (solo lectura) con recuperación semántica.
   - Banco de 12 preguntas de validación y cálculo de métricas de precisión y latencia.

3. **[`03_ml_prorrogas.ipynb`](03_ml_prorrogas.ipynb):**
   - Auditoría de la variable objetivo (`dias_adicionados > 0`) y análisis exploratorio.
   - Regla de oro de firma: exclusión algorítmica de variables post-firma (cero data leakage).
   - Partición temporal estricta (80% entrenamiento histórico, 20% prueba reciente).
   - Entrenamiento y comparación de modelos (Baseline, Regresión Logística, Random Forest y HistGradientBoosting).
   - Evaluación con curvas Precision-Recall, matrices de confusión e importancia por permutación.
   - Exportación de `models/pipeline_prorrogas.joblib` y metadatos JSON auditables.
