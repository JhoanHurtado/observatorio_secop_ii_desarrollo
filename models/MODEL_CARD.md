# 📋 Ficha Técnica del Modelo (Model Card) — Estimación de Riesgo de Prórroga

## 1. Detalles del Modelo
- **Nombre:** Clasificador de Riesgo de Prórroga en Contratos Públicos (SECOP II)
- **Tipo de problema:** Clasificación binaria supervisada (`prorroga = 1` si `dias_adicionados > 0`, `0` en caso contrario).
- **Algoritmos evaluados:** `DummyClassifier` (Baseline), `LogisticRegression`, `RandomForestClassifier`, `HistGradientBoostingClassifier`.
- **Artefacto exportado:** `models/pipeline_prorrogas.joblib`

## 2. Uso Previsto (Intended Use)
- **Propósito:** Ayudar a veedurías ciudadanas, periodistas de datos y equipos de control interno a priorizar qué contratos revisar preventivamente a partir de las características conocidas al momento de la firma.
- **Usuarios objetivo:** Ciudadanos, analistas y auditores no técnicos a través de la interfaz Streamlit.

## 3. Usos NO Recomendados (Out-of-Scope Uses)
- ⚠️ **No constituye evidencia de corrupción, incumplimiento ni ilegalidad.** Una prórroga puede responder a causas técnicas o administrativas justificadas.
- **No debe usarse para tomar decisiones sancionatorias automatizadas** ni para descalificar proveedores o entidades públicas.

## 4. Datos de Entrenamiento y Evaluación
- **Fuente:** SECOP II – Contratos Electrónicos (`datos.gov.co`, ID: `jbjy-vk9h`), Colombia Compra Eficiente.
- **Licencia de los datos:** CC BY-SA 4.0.
- **Estrategia de validación:** Partición temporal estricta (entrenamiento en periodo histórico y prueba en el periodo más reciente) para evitar fuga de información temporal.
- **Prevención de Data Leakage:** Se excluyen estrictamente variables post-firma (`valor_pagado`, `estado_contrato`, `liquidaci_n`, `reversion`, etc.) y datos personales/bancarios.

## 5. Métricas de Desempeño (Conjunto de Prueba Temporal)
*(Se completa automáticamente al exportar los resultados desde la Etapa 3/4 del Notebook)*
- **F1-Score (Clase Positiva):** Pendiente de ejecución
- **PR-AUC (Average Precision):** Pendiente de ejecución
- **ROC-AUC:** Pendiente de ejecución

## 6. Límites Conocidos y Consideraciones Éticas
- El dataset tabular no incluye los pliegos de condiciones ni las actas físicas adjuntas al expediente electrónico.
- Pueden existir rezagos entre la firma real del contrato y su registro o actualización en la plataforma SECOP II.
- Toda revisión debe contrastarse en el enlace oficial del proceso (`urlproceso`).

