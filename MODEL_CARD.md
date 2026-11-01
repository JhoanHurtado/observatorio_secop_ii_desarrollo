# 📋 Model Card: Estimador de Riesgo de Prórroga en Contratación Pública (SECOP II)

Documento elaborado conforme al estándar de *Model Cards for Model Reporting* (Mitchell et al., 2019) para garantizar transparencia algorítmica, trazabilidad ética y rendición de cuentas en el sector público.

---

## 1. Detalles del Modelo

| Atributo | Detalle |
| :--- | :--- |
| **Nombre del Modelo** | Estimador de Riesgo de Prórroga de Plazo (`pipeline_prorrogas.joblib`) |
| **Versión** | 1.0.0 |
| **Tipo de Algoritmo** | Ensamble de Árboles de Decisión (`HistGradientBoostingClassifier`) en Pipeline de scikit-learn |
| **Fecha de Entrenamiento** | Octubre de 2026 |
| **Desarrollador** | Observatorio Ciudadano de Contratación Pública (SECOP II) |
| **Licencia de Código y Modelo** | MIT / Licencia de Datos Abiertos CC BY-SA 4.0 |
| **Artefacto Serializado** | `models/pipeline_prorrogas.joblib` (preprocesador + clasificador) |
| **Metadatos Auxiliares** | `models/model_metadata.json` |

---

## 2. Uso Previsto y Alcance (Intended Use)

### Casos de Uso Primarios
- **Triaje Preventivo para Veedurías Ciudadanas:** Priorizar la revisión de expedientes contractuales que, desde su concepción, presentan características asociadas a extensiones temporales no programadas.
- **Alertas Tempranas para Oficinas de Control Interno:** Identificar procesos con alta probabilidad de desviación temporal para intensificar la supervisión e interventoría desde el acta de inicio.
- **Monitoreo Periodístico y Académico:** Analizar patrones estructurales de contratación en el departamento (Valle del Cauca) y comparar dinámicas entre sectores.

### Usos No Previstos y Restricciones Éticas (Out-of-Scope Use)
- **NO es un detector de corrupción:** Una prórroga es una figura legal válida (Ley 80 de 1993) ante imprevistos técnicos, climáticos o geológicos. El modelo estima riesgo de prórroga, no ilegalidad.
- **NO debe utilizarse para vetar proponentes:** La probabilidad no juzga la reputación del contratista ni debe ser usada como criterio descalificador en pliegos de condiciones.
- **NO reemplaza la auditoría documental:** Es una herramienta de cribado inicial; cualquier conclusión debe fundamentarse en el expediente electrónico original en SECOP II.

---

## 3. Prevención Estricta de Fuga de Información (Data Leakage)

El modelo cumple la **Regla de Oro de Firma Contractual (RF-ML2)**: se alimenta exclusivamente de información conocida y perfeccionada al momento de suscribir el contrato.

### Variables Permitidas
- **Numéricas (4):** `valor_contrato_log` (transformación log1p del valor oficial), `mes_firma`, `anio_firma`, `duracion_planeada_dias` (días entre fecha de inicio pactada o firma y fecha fin estimada).
- **Categóricas (11):** `tipo_de_contrato`, `modalidad_de_contratacion`, `sector`, `rama`, `orden`, `departamento`, `es_pyme`, `es_grupo`, `habilita_pago_adelantado`, `origen_de_los_recursos`, `segmento_unspsc` (primeros 2 dígitos de codificación de bienes/servicios).

### Variables Excluidas Proactivamente (`verificar_ausencia_leakage`)
Quedan vetadas del entrenamiento e inferencia: `dias_adicionados` (base del target), `estado_contrato`, `valor_pagado`, `valor_facturado`, `valor_pendiente_de_pago`, `liquidaci_n`, `fecha_ini_ejecucion`, `fecha_fin_ejecucion`, `reversion`, `saldo_cdp`.

---

## 4. Datos de Entrenamiento y Validación

- **Fuente:** Portal de Datos Abiertos del Estado Colombiano (datos.gov.co), Dataset `SECOP II – Contratos Electrónicos` (`jbjy-vk9h`).
- **Población:** 50,000 contratos firmados en el departamento del Valle del Cauca (2023 - 2026).
- **Control de Censura a la Derecha:** Se filtraron contratos cuyo plazo de ejecución original aún no vencía al momento del corte, evitando etiquetar como negativos contratos que aún podían solicitar adición.
- **Partición Temporal Estricta:**
  - **Entrenamiento (80% histórico):** 30,592 contratos (enero 2023 a febrero 2023). Prevalencia de prórroga: 10.41%.
  - **Prueba Temporal (20% futuro):** 7,648 contratos (febrero 2023 a octubre 2026). Prevalencia de prórroga: 18.03%.

---

## 5. Métricas de Rendimiento y Comparativa

Dado el desbalance de clases (prevalencia ~12-18%), la métrica de optimización primaria es el **Área bajo la Curva Precisión-Recall (PR-AUC)**.

| Modelo | PR-AUC (CV Train) | PR-AUC (Test) | ROC-AUC (Test) | Precision (Test) | Recall (Test) | F1-Score (Test) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Línea Base (Prior / Azar)** | 0.128 | 0.180 | 0.500 | 0.000 | 0.000 | 0.000 |
| **Regresión Logística (Balanced)** | 0.215 | 0.224 | 0.661 | 0.240 | 0.962 | 0.384 |
| **Random Forest (Balanced)** | 0.382 | 0.569 | 0.842 | 0.451 | 0.788 | 0.574 |
| **Gradient Boosting (Ajustado)** | **0.389** | **0.542** | **0.821** | **0.384** | **0.765** | **0.512** |

*El modelo ensamble supera con creces la línea base ingenua (PR-AUC 0.54 vs 0.18) y mantiene una exhaustividad (Recall) del 76.5%, logrando capturar 3 de cada 4 contratos que efectivamente terminan requiriendo prórroga.*

---

## 6. Factores de Riesgo e Importancia de Variables

Según el análisis de importancia por permutación sobre el conjunto de prueba temporal:
1. **Duración planeada inicial (`duracion_planeada_dias`):** Contratos con plazos pactados muy ajustados o extremadamente largos presentan mayor propensión a desvíos.
2. **Sector administrativo (`sector`):** Sectores de infraestructura, servicios públicos y salud presentan mayor tasa de adiciones que contratos administrativos o de papelería.
3. **Monto del contrato (`valor_contrato_log`):** Los contratos de gran cuantía conllevan mayor complejidad operativa y logística.
4. **Rama y Orden (`rama`, `orden`):** Dinámicas diferenciadas entre el nivel territorial (alcaldías/gobernación) frente al nivel nacional.

---

## 7. Categorización del Riesgo para Inferencia

El servicio de predicción (`predecir_riesgo_prorroga`) traduce la probabilidad continua $P(\text{prórroga})$ a tres categorías orientativas:
- **Bajo ($P < 0.30$):** Contrato con parámetros estándar; seguimiento habitual.
- **Medio ($0.30 \le P < 0.60$):** Alerta orientativa; se sugiere verificar el cronograma de supervisión e hitos de entrega.
- **Alto ($P \ge 0.60$):** Contrato complejo; se recomienda priorizar revisión de los estudios previos, garantías y pólizas.

---

## 8. Latencia y Rendimiento en Producción

- **Tiempo de inferencia unitaria:** ~18.7 ms (ampliamente inferior al límite de 2,000 ms establecido en RF-ML6).
- **Carga de artefacto:** Sin reentrenamiento, lectura de memoria directa vía `joblib`.

