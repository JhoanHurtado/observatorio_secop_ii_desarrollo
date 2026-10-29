# 📋 Ficha de Transparencia del Modelo (Model Card)

## 1. Resumen General
- **Propósito:** Estimar, a partir de las condiciones conocidas el día en que se firma un contrato en SECOP II, la probabilidad de que requiera una prórroga de plazo (`dias_adicionados > 0`).
- **Enfoque:** Clasificación binaria supervisada comparando una línea base frente a modelos clásicos interpretables (`LogisticRegression`, `RandomForestClassifier`, `HistGradientBoostingClassifier`).
- **Archivo del modelo:** `models/pipeline_prorrogas.joblib`

## 2. ¿Para qué sirve esta herramienta?
- Ayudar a **veedurías ciudadanas, periodistas de datos y equipos de control interno** a priorizar qué contratos revisar preventivamente dentro de un volumen de decenas de miles de registros.
- Ofrecer una interfaz clara donde cualquier persona pueda explorar qué factores contractuales se asocian históricamente con mayores tiempos de ejecución.

## 3. ¿Para qué NO debe utilizarse?
- ⚠️ **No es un detector de irregularidades ni de corrupción:** Que un contrato tenga una alta probabilidad de prórroga (o que efectivamente se prorrogue) puede obedecer a causas técnicas, climáticas o administrativas plenamente justificadas.
- **No reemplaza la revisión documental:** Nunca debe usarse para emitir juicios o sanciones automáticas sobre entidades públicas o contratistas.

## 4. Datos y Criterios de Entrenamiento
- **Fuente oficial:** *SECOP II – Contratos Electrónicos* (`datos.gov.co`, ID: `jbjy-vk9h`), Colombia Compra Eficiente. Licencia **CC BY-SA 4.0**.
- **Validación en el tiempo:** El modelo se entrena con contratos históricos y se evalúa sobre los contratos más recientes, simulando un escenario real de predicción hacia adelante.
- **Cero información futura:** Se excluyen todas las columnas que reflejan eventos posteriores a la firma (como pagos realizados, saldos o fechas de liquidación), así como cualquier dato personal o bancario.

## 5. Desempeño en el Periodo de Prueba
*(Se actualiza al exportar los resultados desde el Notebook)*
- **F1-Score (Contratos con prórroga):** Pendiente de actualización
- **PR-AUC (Precisión vs. Exhaustividad):** Pendiente de actualización
- **ROC-AUC:** Pendiente de actualización

## 6. Limitaciones a Tener en Cuenta
- El conjunto de datos tabular resume las condiciones del contrato, pero no incluye los documentos PDF adjuntos (estudios previos, pliegos o actas de supervisión).
- Toda consulta o alerta debe verificarse directamente en el proceso oficial mediante el enlace `urlproceso`.
