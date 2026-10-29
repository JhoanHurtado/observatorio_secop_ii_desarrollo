Observatorio ciudadano de contratación pública
Proyecto de portafolio: asistente RAG en la nube y modelo de Machine Learning sobre datos
abiertos de SECOP II
Proyecto personal para blog y LinkedIn | Fuente de datos: SECOP II (datos abiertos) | Versión 2.3 | 28 de octubre de 2026
1. Descripción del caso
La contratación pública es un canal central del gasto del Estado y su información se publica como datos abiertos. El
volumen del conjunto de datos (millones de registros y decenas de columnas) y la necesidad de conocer el marco
legal dificultan que ciudadanos, veedurías, periodistas y equipos de control interno respondan preguntas básicas o
identifiquen contratos que merecen una revisión más atenta.
El proyecto construye un Observatorio ciudadano de contratación pública sobre SECOP II, con dos
componentes que comparten la misma fuente y que se publican como piezas de portafolio:
Componente Qué resuelve
A. Asistente en la nube (RAG) Responde en lenguaje natural con cifras (base SQL) y con normativa (base vectorial en
la nube), citando sus fuentes.
B. Machine Learning clásico con Estima la probabilidad de que un contrato requiera prórroga de plazo y la presenta en
Streamlit una aplicación para explorar y consultar.
Usuario Necesidad real Uso del sistema
Veedurías ciudadanas Saber cuánto, con quién y bajo qué modalidad Preguntas al asistente y filtros de
contrata una entidad exploración
Periodistas de datos Contrastar cifras con lo que dice la ley Consultas mixtas (SQL y normativa) con
citas verificables
Control interno de entidades Priorizar qué contratos revisar primero Estimación de riesgo de prórroga y su
explicación
Reclutadores y colegas del Evaluar criterio técnico y capacidad de Repositorio, demo, artículo y publicación
sector comunicación
Uso responsable. Los resultados describen patrones estadísticos y no constituyen evidencia de irregularidades. Toda
alerta debe verificarse en el proceso original, disponible en el campo urlproceso del dataset.
2. Objetivos del proyecto de portafolio
Objetivo Cómo se evidencia
Demostrar una arquitectura de datos híbrida en la nube (SQL y base Diagrama, repositorio y demo funcional
vectorial)
Demostrar Machine Learning clásico bien hecho: sin fuga de información, Notebook, tabla de métricas y aplicación
validación temporal y métricas honestas
Comunicar resultados y límites con claridad Artículo de blog y publicación en LinkedIn
Entregar algo que otras personas puedan ejecutar README, requirements.txt, datos reproducibles y
demo pública
Observatorio ciudadano de contratación pública | Proyecto de portafolio Página 1

Qué lo distingue de un tutorial: usa datos reales con actualización diaria, normativa real, una evaluación con
preguntas de respuesta verificable y una sección explícita de uso responsable.
3. Fuentes de datos públicas y condiciones de uso
Fuente Contenido Observaciones
SECOP II – Contratos Aprox. 4.775.550 contratos publicados desde 2013 Puede tener campos nulos o
Electrónicos (Colombia Compra hasta el 31 de agosto de 2025; 87 columnas; llave inconsistentes y no incluye los
Eficiente, datos.gov.co) única id_contrato; actualización diaria. documentos adjuntos de los contratos.
Diccionario de datos y ficha Descripción de cada columna, cobertura, Base del diccionario de columnas del
técnica – Registros frecuencia de actualización y marco normativo. proyecto y de la cita del dataset.
administrativos (versión 1.0,
agosto de 2025)
Normativa de contratación Ley 80 de 1993, Ley 1150 de 2007 y Decreto 1082 Obtener los textos de fuentes oficiales
de 2015 (marco citado en el diccionario). Opcional: y convertirlos a Markdown. El decreto
Ley 1712 de 2014 (transparencia). es extenso: usar solo el título de
contratación estatal.
Manual de datos abiertos del Guía de uso de los datos abiertos del SECOP. Documento complementario para el
SECOP (Colombia Compra corpus.
Eficiente)
Alcance y tratamiento de los datos
(cid:127) Subconjunto: trabajar con un departamento y uno o dos años (entre 20.000 y 100.000 contratos), no con el
conjunto completo.
(cid:127) Columnas sugeridas (unas 15): id_contrato, nombre_entidad, departamento, ciudad, sector,
estado_contrato, tipo_de_contrato, modalidad_de_contratacion, fecha_de_firma, valor_del_contrato,
proveedor_adjudicado, descripcion_del_proceso, objeto_del_contrato, urlproceso.
(cid:127) Privacidad: excluir nombres, documentos y domicilios de representantes legales, supervisores y ordenadores
del gasto, así como los datos bancarios (banco, tipo y número de cuenta).
(cid:127) Licencia: el dataset se publica bajo CC BY-SA 4.0 (confirmar el nombre exacto en la pestaña de metadatos de la
ficha, Anexo A). Exige atribución y compartir con la misma licencia lo que se derive de los datos (sección 6.3).
Revisar también los términos de uso de Colombia Compra Eficiente.
(cid:127) Trazabilidad: registrar la fecha de consulta, porque los datos se actualizan a diario. Los enlaces de descarga de
cada dataset y documento están en el Anexo A.
Cita sugerida (APA 7). Colombia Compra Eficiente. (2026). SECOP II – Contratos electrónicos [Conjunto de datos].
Datos Abiertos Colombia. Licencia CC BY-SA 4.0. [URL del dataset, ver Anexo A]. Consultado el [fecha de descarga].
4. Componente A: asistente en la nube (RAG)
4.1 Definición
Elemento Definición
Objetivo Construir en la nube un pipeline de ingesta, fragmentación, vectorización y recuperación semántica
sobre normativa de contratación pública, integrado con una base SQL de contratos de SECOP II, para
responder preguntas en lenguaje natural con fuentes verificables.
Pregunta orientadora ¿Cómo combinar una base SQL de contratos públicos y una base vectorial serverless con normativa
de contratación, de modo que un asistente recupere información con alta precisión, costo cero y baja
latencia, y cite sus fuentes?
Observatorio ciudadano de contratación pública | Proyecto de portafolio Página 2

Elemento Definición
Dataset base SECOP II – Contratos Electrónicos (subconjunto por departamento y año).
Corpus documental Ley 80 de 1993, Ley 1150 de 2007 y un tercer documento (fragmento del Decreto 1082 de 2015 o
manual de datos abiertos del SECOP), en Markdown con metadatos.
Stack SQLite (datos tabulares); Qdrant Cloud (colección normativa y, opcional, objetos_contratos);
Gemini Embedding 2 (768 dimensiones); LangChain text splitters; Streamlit; Jupyter o Colab; GitHub.
4.2 Arquitectura
Ruta de datos tabulares
| API datos.gov.co | Limpieza y  | SQLite            |     |
| ---------------- | ----------- | ----------------- | --- |
| (SECOP II)       | subconjunto | (tabla contratos) |     |
Ruta de documentos
| Normativa (.md) | Chunking | Embeddings | Qdrant Cloud |
| --------------- | -------- | ---------- | ------------ |
Ley 80, Ley 1150 por artículo Gemini 768 dim. distancia coseno
Ruta de consulta
| Usuario | Orquestador | SQL solo lectura | Respuesta con |
| ------- | ----------- | ---------------- | ------------- |
(Streamlit) LLM + herramientas Búsqueda Top-k fuentes citadas
4.3 Requerimientos funcionales
| ID Requerimiento | Criterio de aceptación |     | Prioridad |
| ---------------- | ---------------------- | --- | --------- |
RF-1 Aprovisionar clúster gratuito en Qdrant La consulta de colecciones responde; las credenciales Esencial
| Cloud con colección en distancia | se leen solo desde .env. |     |     |
| -------------------------------- | ------------------------ | --- | --- |
coseno y dimensión igual a la del
modelo.
RF-2 Descargar el subconjunto vía API, El conteo en SQLite coincide con el de la API; índices Esencial
| limpiarlo y cargarlo en SQLite. | creados; fecha de consulta registrada. |     |     |
| ------------------------------- | -------------------------------------- | --- | --- |
RF-3 Reunir de 2 a 3 documentos normativos Cada archivo declara documento, tipo de fuente, tema Esencial
| con metadatos. | y fecha. |     |     |
| -------------- | -------- | --- | --- |
RF-4 Fragmentar por artículo con Tabla comparativa (fragmentos, longitud media, Esencial
RecursiveCharacterTextSplitter y mínimo, máximo), tamaño elegido con justificación y
| comparar al menos tres tamaños. | ningún fragmento cortado a mitad de palabra. |     |     |
| ------------------------------- | -------------------------------------------- | --- | --- |
RF-5 Vectorizar por lotes con Gemini Puntos en Qdrant igual al número de fragmentos; Esencial
Embedding 2 y cargar con upsert por vectores guardados en disco; sin exceder la capa
| lotes. | gratuita. |     |     |
| ------ | --------- | --- | --- |
RF-6 Función de búsqueda: vectoriza la Resultados en tabla; filtro opcional por documento. Esencial
pregunta, consulta Top-k y devuelve
texto, score coseno, documento y
artículo.
RF-7 Validar con 10 a 15 preguntas: directas, Promedio, máximo y mínimo de scores; porcentaje de Esencial
| parafraseadas, mixtas y sin respuesta. | aciertos en top-1 y top-3; análisis de fallos. |     |     |
| -------------------------------------- | ---------------------------------------------- | --- | --- |
RF-8 Generar consultas SQL desde lenguaje Solo lectura, una sentencia SELECT, límite de filas y Recomendado
| natural. | SQL visible al usuario. |     |     |
| -------- | ----------------------- | --- | --- |
Observatorio ciudadano de contratación pública  |  Proyecto de portafolio Página 3

ID Requerimiento Criterio de aceptación Prioridad
RF-9 Interfaz de chat en Streamlit con Cada respuesta muestra el SQL ejecutado y las Recomendado
memoria corta. fuentes (documento y artículo); rechaza lo que no está
en las fuentes.
RF-10 Proteger la demo pública. Claves solo en secretos del servidor; límite de Recomendado
consultas por sesión; tope de cuota en el proveedor.
4.4 Requerimientos no funcionales
(cid:127) Seguridad: ninguna clave en el notebook ni en el repositorio; incluir .env.example sin valores.
(cid:127) Reproducibilidad: el notebook se ejecuta de principio a fin sin errores y muestra el Top-k recuperado.
(cid:127) Costo cero: capa gratuita de Qdrant y de la API de embeddings; verificar los límites vigentes en Google AI
Studio antes de vectorizar.
(cid:127) Privacidad: sin datos personales en la base SQL, la base vectorial, la demo ni las imágenes publicadas.
(cid:127) Latencia objetivo: menos de 5 segundos por consulta (objetivo de diseño a medir en la validación).
(cid:127) Compatibilidad del modelo: con gemini-embedding-2 el tipo de tarea se indica con prefijos en el texto (title:
... | text: ... para documentos y task: search result | query: ... para consultas), no con el parámetro
task_type. Si prefieres ese parámetro, elige un modelo que lo admita y verifícalo en la documentación.
4.5 Banco de preguntas de validación (ejemplos)
Tipo Pregunta Fuente esperada
Directa ¿Cuándo procede la contratación directa? Ley 1150 de 2007 (verificar el artículo
en el .md)
Parafraseada ¿En qué casos una entidad puede contratar sin licitación? Ley 1150 de 2007
SQL ¿Cuántos contratos de prestación de servicios se firmaron en 2024 Tabla de contratos
en el departamento elegido?
SQL ¿Cuáles son los cinco proveedores con mayor valor contratado? Tabla de contratos (solo personas
jurídicas)
Mixta ¿Cuántos contratos se firmaron por contratación directa y qué dice la Tabla de contratos y Ley 1150
ley sobre esa modalidad?
Sin respuesta ¿Cuál fue el contrato más barato firmado en Francia? El asistente debe indicar que no hay
información
5. Componente B: Machine Learning clásico con Streamlit
5.1 Definición del problema
Elemento Definición
Objetivo Desarrollar una solución de Machine Learning clásico que, con la información disponible al firmar un
contrato, estime la probabilidad de que requiera prórroga de plazo, y presentarla en una interfaz
Streamlit para usuarios no técnicos.
Pregunta orientadora ¿Cómo transformar los datos abiertos de contratación pública en una estimación de riesgo de prórroga
que ayude a priorizar la revisión humana y se pueda consultar desde una interfaz accesible?
Tipo de problema Clasificación binaria supervisada.
Variable objetivo Contrato con prórroga: el campo dias_adicionados (días adicionados al contrato electrónico) es
mayor que cero. Las prórrogas pueden indicar problemas de planeación o de ejecución; estimarlas
sirve para priorizar la revisión, no para sancionar.
Observatorio ciudadano de contratación pública | Proyecto de portafolio Página 4

| Elemento | Definición |     |     |     |     |
| -------- | ---------- | --- | --- | --- | --- |
Validación previa En el EDA, revisar el porcentaje de nulos de la variable objetivo y la proporción de contratos con
prórroga. Si el campo no es confiable, usar una de las alternativas de la tabla siguiente o contrastarlo
con el dataset de Adiciones (Anexo A).
| Variante | Objetivo |     | Algoritmos clásicos | Métricas |     |
| -------- | -------- | --- | ------------------- | -------- | --- |
A. Principal Clasificar contratos con y sin Regresión logística, Random Forest, Precisión, recall y F1 de la clase
|     | prórroga |     | Gradient Boosting | positiva; ROC-AUC; PR-AUC |     |
| --- | -------- | --- | ----------------- | ------------------------- | --- |
MAE, RMSE y R2
| B. Alterna | Estimar el valor del contrato |     | Regresión lineal regularizada,   |     |     |
| ---------- | ----------------------------- | --- | -------------------------------- | --- | --- |
|            | (escala logarítmica)          |     | Random Forest, Gradient Boosting |     |     |
C. Alterna Segmentar entidades o K-Means Silhouette, inercia y perfilado de
|     | proveedores por perfil de |     |     | clústeres |     |
| --- | ------------------------- | --- | --- | --------- | --- |
contratación
5.2 Variables
| Grupo |     | Variables |     |     |     |
| ----- | --- | --------- | --- | --- | --- |
Permitidas (conocidas al firmar) tipo_de_contrato, modalidad_de_contratacion, sector, rama, orden,
departamento, es_pyme, es_grupo, habilita_pago_adelantado,
origen_de_los_recursos, codigo_de_categoria_principal (segmento UNSPSC),
valor_del_contrato en escala logarítmica, mes y año de firma, duración planeada.
Excluidas por fuga de dias_adicionados (es el objetivo), valor_pagado, valor_facturado,
información valor_pendiente_de_pago, estado_contrato, liquidaci_n y sus fechas, reversion.
Excluidas por privacidad Nombres, documentos y domicilios de personas; datos bancarios.
Verificar antes de modelar. Si valor_del_contrato o las fechas de fin del contrato ya reflejan las adiciones y
prórrogas, dejan de ser conocidas al firmar y causan fuga de información: excluirlas o recalcularlas.
5.3 Flujo metodológico
Del dato a la aplicación
| SECOP II      |     | Limpieza y                       | Pipeline     | Modelo    | App       |
| ------------- | --- | -------------------------------- | ------------ | --------- | --------- |
| (subconjunto) |     | variables                        | scikit-learn | (.joblib) | Streamlit |
| Paso          |     | Actividades concretas en el caso |              |           |           |
1. Exploración y EDA Distribución de la variable objetivo; nulos por columna; contratos por modalidad, tipo y
departamento; relación entre valor (logarítmico) y prórroga; revisión del desbalance de clases.
2. Limpieza y Eliminar duplicados por id_contrato; convertir fechas y valores; agrupar categorías poco
preprocesamiento frecuentes; imputar nulos; codificar variables categóricas; escalar las numéricas cuando el algoritmo
lo requiera. Todo dentro de un Pipeline de scikit-learn.
3. Modelado clásico Baseline (DummyClassifier), regresión logística, Random Forest y Gradient Boosting. División
temporal: entrenar con los años anteriores y probar con el más reciente. Validación cruzada y
búsqueda de hiperparámetros solo sobre el conjunto de entrenamiento; manejo del desbalance con
pesos de clase.
4. Evaluación Matriz de confusión; precisión, recall y F1 de la clase positiva; ROC-AUC y PR-AUC; comparación
contra el baseline; importancia por permutación; análisis de errores por modalidad y departamento.
5. Despliegue Exportar el Pipeline con joblib; aplicación Streamlit con pestañas; requirements.txt con
versiones fijas; prueba local con streamlit run app.py; publicación en una plataforma de
alojamiento.
Observatorio ciudadano de contratación pública  |  Proyecto de portafolio Página 5

5.4 Requerimientos funcionales
ID Requerimiento Criterio de aceptación Prioridad
RF-ML1 Obtener un dataset Un script o celda regenera el subconjunto y registra la Esencial
reproducible. fecha de consulta.
RF-ML2 Preprocesar sin fuga de Todas las transformaciones se ajustan solo con el conjunto Esencial
información. de entrenamiento.
RF-ML3 Comparar un baseline y al Tabla comparativa y justificación del modelo elegido. Esencial
menos tres algoritmos clásicos.
RF-ML4 Evaluar en el conjunto de Métricas, matriz de confusión e interpretación en celdas de Esencial
prueba temporal. texto.
RF-ML5 Construir la interfaz con cuatro Contexto (fuente y fecha de corte); Exploración (filtros por Esencial
pestañas. departamento, modalidad y año con gráficos); Predicción
(formulario con validación que muestra probabilidad, nivel
de riesgo y factores principales); Métricas (tabla, matriz de
confusión y comparación de modelos).
RF-ML6 Integrar el modelo entrenado La app carga el artefacto, no reentrena; la predicción Esencial
en la aplicación. coincide con la del notebook para el mismo registro.
RF-ML7 Comunicar el uso responsable. Aviso visible en la app, el README y el artículo; enlace al Esencial
proceso original del contrato.
RF-ML8 Documentar el modelo con una Datos usados, métricas, límites conocidos y usos no Recomendado
ficha (model card). recomendados.
5.5 Requerimientos no funcionales y criterios de éxito
(cid:127) Reproducibilidad: semilla aleatoria fija y versiones de librerías fijadas en requirements.txt.
(cid:127) Interpretabilidad: algoritmos clásicos con importancia de variables explicada en lenguaje claro.
(cid:127) Modularidad: app.py más módulos auxiliares para carga del modelo, validación de entradas y gráficos.
(cid:127) Desempeño: predicción individual en menos de 2 segundos (objetivo de diseño).
(cid:127) Privacidad: la app y el modelo no usan ni muestran datos personales.
Criterios de éxito. El modelo supera al baseline en F1 de la clase positiva y en PR-AUC sobre el conjunto de prueba
temporal; los resultados se interpretan con sus límites; la aplicación reproduce la predicción del notebook.
6. Publicación: repositorio, demo, blog y LinkedIn
6.1 Entregables publicables
Entregable Contenido Dónde
Repositorio README (problema, arquitectura, cómo ejecutarlo, resultados y GitHub público
límites), notebooks, app, requirements.txt, .env.example,
licencia del código y aviso de licencia CC BY-SA 4.0 para los datos
derivados. Sin claves ni datos personales.
Demo pública Aplicación Streamlit desplegada, más un video o GIF de 60 a 90 Plataforma de alojamiento
segundos como respaldo si la demo no está disponible. gratuita (Streamlit Community
Cloud o Hugging Face Spaces;
verificar límites vigentes)
Artículo de blog Problema; datos y fuentes; arquitectura; decisiones técnicas y errores Blog personal
corregidos; resultados con métricas y ejemplos; límites y uso
responsable; cómo replicarlo.
Observatorio ciudadano de contratación pública | Proyecto de portafolio Página 6

Entregable Contenido Dónde
Publicación en Texto breve (unas 150 a 250 palabras): el problema, tres LinkedIn
LinkedIn aprendizajes concretos, una imagen del diagrama o un GIF de la
demo y enlaces al artículo y al repositorio.
Si el proyecto es extenso, publicarlo como dos piezas (una por componente) da más contenido y permite mostrar el
avance por etapas.
6.2 Riesgos y buenas prácticas antes de publicar
Riesgo Mitigación
Claves expuestas en el repositorio Variables de entorno y secretos del servidor; revisar el historial de Git antes de hacerlo
público; regenerar cualquier clave que se haya subido.
Abuso de la cuota o costo de la demo Límite de consultas por sesión, caché de respuestas, tope de cuota en el proveedor, o
pública demo con ejemplos pregrabados.
SQL peligroso o instrucciones ocultas en Base en modo solo lectura, una sola sentencia SELECT y límite de filas. Tratar el texto
textos de contratos de los contratos como datos, nunca como instrucciones.
Daño reputacional al señalar entidades o Mostrar agregados y patrones, usar lenguaje neutral, no calificar de corrupción, incluir
proveedores el aviso de uso responsable y el enlace al proceso original.
Datos personales de contratistas El campo proveedor_adjudicado puede corresponder a una persona natural. En la
demo mostrar solo personas jurídicas (por ejemplo, filtrando por tipodocproveedor;
verificar los valores reales) o agregar sin nombres.
Licencia y atribución Cumplir las condiciones de CC BY-SA 4.0 (sección 6.3): atribución, indicación de
modificaciones, compartir los datos derivados con la misma licencia y aviso de no
afiliación a Colombia Compra Eficiente.
Datos desactualizados Mostrar la fecha de corte en la interfaz y en el artículo.
Exagerar los resultados del modelo Reportar métricas frente al baseline, explicar los límites y no presentar la probabilidad
como veredicto.
6.3 Licencia de los datos: CC BY-SA 4.0
El dataset principal se publica bajo la licencia Creative Commons Atribución-CompartirIgual 4.0 Internacional (CC
BY-SA 4.0), según la consulta hecha por el autor del proyecto. Confirmar el nombre exacto de la licencia y la forma
de atribución solicitada en la pestaña de metadatos de la ficha (Anexo A). La tabla resume las condiciones y lo que
implican aquí; no es asesoría jurídica.
Condición de la licencia Qué implica en el proyecto
Atribución Al compartir los datos, incluso modificados, identificar al titular, enlazar al dataset, indicar la
licencia con enlace a su texto y conservar los avisos que provea el licenciante. Incluir la
atribución en el README, la app y el artículo.
Indicar las modificaciones Declarar que los datos se filtraron, limpiaron y transformaron (subconjunto, conversión de tipos,
columnas derivadas).
CompartirIgual El material adaptado que se comparta debe licenciarse con CC BY-SA 4.0 (misma versión o
posterior) o con una licencia compatible. Un subconjunto limpio publicado como CSV o SQLite es
material adaptado.
Derechos sobre bases de La licencia cubre los derechos sobre bases de datos. Una base propia que incluya todo o una
datos parte sustancial del contenido es material adaptado, aunque sus datos individuales no cambien.
Sin restricciones adicionales No imponer condiciones extra ni medidas técnicas que impidan a otras personas ejercer los
derechos de la licencia sobre los datos publicados.
Observatorio ciudadano de contratación pública | Proyecto de portafolio Página 7

Condición de la licencia Qué implica en el proyecto
Sin aval No sugerir que Colombia Compra Eficiente respalda o patrocina el proyecto. Mantener el aviso
de no afiliación.
Privacidad La licencia no cubre los derechos de privacidad ni de personalidad. Los datos personales siguen
sujetos a la normativa colombiana (por ejemplo, la Ley 1581 de 2012). Mantener la exclusión de
datos personales.
Sin garantías e incumplimiento Los datos se ofrecen tal cual. Si se incumple una condición, los derechos de uso terminan
automáticamente y se restablecen si se corrige dentro de los 30 días siguientes a detectarla:
corregir de inmediato.
Decisiones sugeridas
(cid:127) Código: licencia propia (por ejemplo, MIT) en el archivo LICENSE.
(cid:127) Datos derivados (CSV o SQLite del subconjunto): CC BY-SA 4.0, con un archivo de aviso que incluya la
atribución.
(cid:127) Alternativa conservadora: no publicar el subconjunto; publicar solo el script que lo descarga y los resultados
agregados, siempre con atribución.
(cid:127) Modelo entrenado: la licencia no aclara si un modelo entrenado con estos datos es material adaptado. Citar la
fuente en la ficha del modelo y consultar una fuente jurídica antes de licenciarlo con condiciones distintas.
Plantilla de atribución (README, app y artículo; si la ficha del dataset pide otra forma, usar esa):
Datos: «SECOP II – Contratos Electrónicos», Colombia Compra Eficiente (Agencia Nacional de Contratación
Pública), Portal Nacional de Datos Abiertos. https://www.datos.gov.co/Estad-sticas-Nacionales/SECOP-II-Co
ntratos-Electr-nicos/jbjy-vk9h. Licencia: CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0/.
Consultado el [fecha]. Modificaciones: se filtró por [departamento y años], se limpió y se agregaron
columnas derivadas. Este subconjunto derivado se comparte bajo CC BY-SA 4.0. Este proyecto no está
afiliado ni respaldado por Colombia Compra Eficiente.
7. Plan de trabajo sugerido
Etapa Resultado esperado
1. Datos (compartida) Subconjunto descargado, limpiado y cargado en SQLite, con diccionario de columnas y fecha de
consulta.
2. Componente A Corpus en Markdown, chunking comparado, embeddings por lotes, colección en Qdrant,
búsqueda y validación con 10 a 15 preguntas.
3. Componente B EDA, preprocesamiento sin fuga, comparación de modelos y evaluación en el conjunto de prueba
temporal.
4. Aplicación App Streamlit con asistente y predicción, probada de principio a fin.
5. Repositorio y demo README, ficha del modelo, revisión de claves y datos personales, y demo desplegada.
6. Blog y LinkedIn Artículo publicado y publicación en LinkedIn con imagen y enlaces funcionales.
Anexo A. Enlaces de descarga y consulta
Estado de cada enlace: Verificado significa que la dirección apareció en una página o resultado oficial consultado el
28 de octubre de 2026. Por confirmar significa que proviene de una fuente de terceros o del patrón estándar de la
plataforma. La ficha del dataset principal en datos.gov.co se abrió y confirma el identificador, pero su contenido
(licencia, columnas) se carga con JavaScript y no pudo leerse desde este entorno (la licencia CC BY-SA 4.0
proviene de la consulta hecha por el autor del proyecto); los enlaces de API y CSV no pudieron probarse.
Observatorio ciudadano de contratación pública | Proyecto de portafolio Página 8

| Recurso | Qué contiene y uso | Enlace | Estado |
| ------- | ------------------ | ------ | ------ |
A. Datos tabulares
SECOP II – Contratos Contratos con 87 columnas. Página: https://www.datos.gov.co/Estad-sticas-Nacio Verificado
Electrónicos (ficha del Fuente de la base SQL y del nales/SECOP-II-Contratos-Electr-nicos/jbjy-vk9h
Metadatos: https://www.datos.gov.co/Estad-sticas-N
| dataset principal) | modelo. La pestaña de metadatos |     |     |
| ------------------ | ------------------------------- | --- | --- |
acionales/SECOP-II-Contratos-Electr-nicos/jbjy-vk9h/
muestra licencia, fuente y
about_data
frecuencia de actualización.
SECOP II – Contratos Mismo dataset, descargable por API JSON: https://www.datos.gov.co/resource/jbjy-vk Por
Electrónicos (descarga por API en JSON o CSV con filtros. 9h.json confirmar
| API) |     | CSV: https://www.datos.gov.co/resource/jbjy-vk9h.cs |     |
| ---- | --- | --------------------------------------------------- | --- |
v
SECOP II – Adiciones a Adiciones registradas en SECOP Página: https://www.datos.gov.co/d/cb9c-h8sn Por
contratos II. Opcional: contrastar la variable API JSON: https://www.datos.gov.co/resource/cb9c- confirmar
h8sn.json
objetivo; revisar sus columnas.
SECOP II – Procesos de Procesos de compra (licitaciones, Página: https://www.datos.gov.co/d/p6dx-8zbt Por
| Contratación | convocatorias). Opcional. |     | confirmar |
| ------------ | ------------------------- | --- | --------- |
SECOP II – Ejecución Avance estimado y real de la Página CCE: https://www.colombiacompra.gov.co/ar Verificado
Contratos ejecución. Opcional. Un repositorio chivos/conjunto-datos-abier/ejecucion-contratos
de terceros reporta el identificador
mfmm-jqmq.
B. Documentación y portales de datos
Portal de datos abiertos de Punto de entrada a los conjuntos https://www.colombiacompra.gov.co/transparencia/d Verificado
| Colombia Compra Eficiente | de datos abiertos del SECOP. | atos-abiertos |     |
| ------------------------- | ---------------------------- | ------------- | --- |
Listado de conjuntos de Descripción y enlace de cada https://www.colombiacompra.gov.co/archivos/app-da Verificado
| datos SECOP II | conjunto de SECOP II. | tos-abiertos/secop-ii |     |
| -------------- | --------------------- | --------------------- | --- |
Diccionario de datos y Descripción de las columnas, https://www.colombiacompra.gov.co/wp-content/uplo Verificado
ficha técnica cobertura y marco normativo. ads/2026/01/Diccionario_de_Datos_RegistrosAdmini
strativos-1.pdf
Manual de datos abiertos Guía para consultar y procesar los https://colombiacompra.gov.co/wp-content/uploads/2 Verificado
del SECOP datos del portal. 024/09/manual_de_datos_abiertos_actualizado.pdf
Términos y condiciones de Revisar antes de publicar el https://www.colombiacompra.gov.co/terminos-condici Verificado
| Colombia Compra Eficiente | proyecto. | ones |     |
| ------------------------- | --------- | ---- | --- |
https://creativecommons.org/licenses/by-sa/4.0/
| Licencia CC BY-SA 4.0 | Condiciones de atribución y      |     | Verificado |
| --------------------- | -------------------------------- | --- | ---------- |
| (texto legal)         | CompartirIgual que aplican a los |     |            |
datos y a sus adaptaciones.
C. Normativa para el corpus
Ley 80 de 1993 Estatuto General de Contratación. http://www.secretariasenado.gov.co/senado/basedoc Por
/ley_0080_1993.html
|     | La Ley 2160 de 2021 la modificó: |     | confirmar |
| --- | -------------------------------- | --- | --------- |
usar la versión con notas de
vigencia.
http://www.secretariasenado.gov.co/senado/basedoc
| Ley 1150 de 2007 | Eficiencia y transparencia en la |     | Por |
| ---------------- | -------------------------------- | --- | --- |
/ley_1150_2007.html
|     | contratación; modalidades de |     | confirmar |
| --- | ---------------------------- | --- | --------- |
selección.
https://www.funcionpublica.gov.co/eva/gestornormati
Decreto 1082 de 2015 Decreto Único Reglamentario del Verificado
vo/norma.php?i=77653
sector de Planeación Nacional.
Usar solo el título de contratación
estatal.
Ley 1712 de 2014 Transparencia y acceso a la http://www.secretariasenado.gov.co/senado/basedoc Por
|     | información pública. Opcional. | /ley_1712_2014.html | confirmar |
| --- | ------------------------------ | ------------------- | --------- |
Observatorio ciudadano de contratación pública  |  Proyecto de portafolio Página 9

Recurso Qué contiene y uso Enlace Estado
Circular Externa Única de Reglas de uso del SECOP; su https://www.colombiacompra.gov.co/normativa-y-rela Verificado
Colombia Compra Eficiente índice incluye datos abiertos y toria/circular-unica-externa
prórrogas y adiciones durante la
Ley de Garantías. Opcional como
tercer documento.
Guías y manuales de Manuales y guías oficiales del https://www.colombiacompra.gov.co/normativa-y-rela Verificado
Colombia Compra Eficiente SECOP. toria/guias-y-manuales
D. Documentación técnica
Gemini API – Embeddings Modelos, dimensiones y uso de https://ai.google.dev/gemini-api/docs/embeddings Verificado
prefijos para documentos y
consultas.
Qdrant – Documentación Colecciones, distancia coseno, https://qdrant.tech/documentation/ Por
filtros y carga por lotes. confirmar
Streamlit – Documentación Componentes de chat, caché y https://docs.streamlit.io Por
despliegue. confirmar
Socrata (SODA) – Parámetros $select, $where, https://dev.socrata.com/docs/queries/ Por
Consultas $limit, $offset y $order de la API. confirmar
SECOP-MCP (repositorio Ejemplo de consultas a SECOP II https://github.com/amgallego8/SECOP-MCP Verificado
de terceros) vía Socrata; útil como referencia
de columnas.
A.2 Cómo descargar un subconjunto
(cid:127) Desde el portal: abrir la página del dataset, filtrar por departamento y fecha de firma y exportar en CSV.
(cid:127) Por API (recomendado, reproducible): los ejemplos siguen el patrón estándar de Socrata. Probar primero con
$limit=5 para confirmar los nombres y los valores reales de las columnas.
(cid:127) Descarga completa: no se recomienda. El dataset tiene millones de filas y no es necesario para el proyecto.
Muestra: https://www.datos.gov.co/resource/jbjy-vk9h.csv?$limit=5
Conteo: https://www.datos.gov.co/resource/jbjy-vk9h.json?$select=count(*)
Subconjunto: https://www.datos.gov.co/resource/jbjy-vk9h.csv?$where=departamento='Valle del Cauca' AND
fecha_de_firma>='2024-01-01T00:00:00'&$order=id_contrato&$limit=50000&$offset=0
En código, pasar los parámetros con el argumento params de la librería requests para que se codifiquen los espacios
y las comillas, y paginar con $offset. Un App Token de Socrata (opcional) amplía el límite de peticiones.
Observatorio ciudadano de contratación pública | Proyecto de portafolio Página 10

8. Referencias (APA 7)
Colombia Compra Eficiente. (2025). Diccionario de datos y ficha técnica – Registros administrativos (Versión 1.0). Agencia Nacional de
Contratación Pública.
https://www.colombiacompra.gov.co/wp-content/uploads/2026/01/Diccionario_de_Datos_RegistrosAdministrativos-1.pdf
Colombia Compra Eficiente. (2026). SECOP II – Contratos electrónicos [Conjunto de datos]. Datos Abiertos Colombia.
https://www.datos.gov.co/Estad-sticas-Nacionales/SECOP-II-Contratos-Electr-nicos/jbjy-vk9h [completar con la fecha de consulta]
Congreso de la República de Colombia. (1993). Ley 80 de 1993, por la cual se expide el Estatuto General de Contratación de la
Administración Pública. http://www.secretariasenado.gov.co/senado/basedoc/ley_0080_1993.html
Congreso de la República de Colombia. (2007). Ley 1150 de 2007, por medio de la cual se introducen medidas para la eficiencia y la
transparencia en la Ley 80 de 1993. http://www.secretariasenado.gov.co/senado/basedoc/ley_1150_2007.html
Creative Commons. (s. f.). Attribution-ShareAlike 4.0 International (CC BY-SA 4.0). https://creativecommons.org/licenses/by-sa/4.0/
Google. (s. f.). Embeddings. Gemini API. https://ai.google.dev/gemini-api/docs/embeddings
Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S., & Kiela,
D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. Advances in Neural Information Processing
Systems, 33, 9459–9474. https://arxiv.org/abs/2005.11401
Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V.,
Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, E. (2011). Scikit-learn: Machine learning in
Python. Journal of Machine Learning Research, 12, 2825–2830.
Presidencia de la República de Colombia. (2015). Decreto 1082 de 2015, Decreto Único Reglamentario del Sector Administrativo de
Planeación Nacional. https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=77653
Qdrant Solutions GmbH. (2024). Qdrant documentation: Vector search engine & cloud database. https://qdrant.tech/documentation/
Streamlit Inc. (s. f.). Streamlit documentation. https://docs.streamlit.io
Observatorio ciudadano de contratación pública | Proyecto de portafolio Página 11