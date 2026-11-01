---
**documento**: Diccionario de Datos SECOP II - Registros Administrativos
**tipo_fuente**: Diccionario Técnico de Datos
**tema**: Definición de variables, cobertura y estructura de registros administrativos de SECOP II
**fecha**: Agosto de 2025
---

| Diccionario |              |     |     |             | de  | Datos       |                 | y         | Ficha        |         |     |
| ----------- | ------------ | --- | --- | ----------- | --- | ----------- | --------------- | --------- | ------------ | ------- | --- |
| Técnica     |              |     |     | – Registros |     |             | Administrativos |           |              |         |     |
|             | Agencia      |     |     | Nacional    |     | de          | Contratación    |           |              | Pública | –   |
|             |              |     |     | Colombia    |     | Compra      |                 | Eficiente |              |         |     |
|             | Subdirección |     |     |             | de  | Información |                 |           | y Desarrollo |         |     |
Tecnológico
|     |     |     |     | Sistemas |     | de  | Información |     |     |               |      |
| --- | --- | --- | --- | -------- | --- | --- | ----------- | --- | --- | ------------- | ---- |
|     |     |     |     |          |     |     |             |     |     | Fecha: agosto | 2025 |
Versión:1.0
| Agencia |     | Nacional |     | de  | Contratación |     | Pública |     |     |     |     |
| ------- | --- | -------- | --- | --- | ------------ | --- | ------- | --- | --- | --- | --- |
Página1de23
| Colombia   |              | Compra        |       | Eficiente |              |          |     |     |     |     |     |
| ---------- | ------------ | ------------- | ----- | --------- | ------------ | -------- | --- | --- | --- | --- | --- |
| Dirección: |              | Carrera       | 7     | # 26 –    | 20 - Bogotá, | Colombia |     |     |     |     |     |
| Mesa       | de servicio: |               | (+57) | 601       | 7456788      |          |     |     |     |     |     |
| Atención   |              | al ciudadano: |       | (+57)     | 601 7956600  |          |     |     |     |     |     |

Tabla de Contenido
1. Introducción..................................................................................................................................................3
2. ObjetivodelDocumento..........................................................................................................................4
3. Marco Normativo...........................................................................................................................................4
4. Conjuntos deDatosIncluidos.................................................................................................................5
4.1 SECOP I: Procesos de Compra Pública....................................................................................5
Metadatos...........................................................................................................................................................6
La llave única asociada..........................................................................................................................12
Frecuencia........................................................................................................................................................12
Cobertura..........................................................................................................................................................12
Campos Relevantes...................................................................................................................................12
4.2 SECOP II: Contratos Electrónicos...............................................................................................13
Metadatos........................................................................................................................................................13
La llave única asociada..........................................................................................................................18
Frecuencia........................................................................................................................................................18
Cobertura..........................................................................................................................................................18
Campos Relevantes...................................................................................................................................18
4.3 TVEC: TIENDAVIRTUAL DEL ESTADO COLOMBIANO....................................................19
La llave única asociada..........................................................................................................................20
Frecuencia........................................................................................................................................................20
Cobertura..........................................................................................................................................................20
Metadatos........................................................................................................................................................20
Campos Relevantes...................................................................................................................................21
5. Usos Potenciales...........................................................................................................................................22
6. Limitaciones.....................................................................................................................................................22
7. Glosariode Términos.................................................................................................................................22
8. Contacto...........................................................................................................................................................23
9. Metodología para el acopio..........................................................................................................23
10. Unidad deMedida..............................................................................................................................23
Agencia Nacional de Contratación Pública Página2de23
Colombia Compra Eficiente
Dirección: Carrera 7 # 26 – 20 - Bogotá, Colombia
Mesa de servicio: (+57) 601 7456788
Atención al ciudadano: (+57) 601 7956600

1. Introducción
El Departamento Administrativo Nacional de Estadística (DANE) ha
implementadoelprocesoSICODE(SistemadeClasificacióndeDatosEstadísticos)
como parte de su estrategia para fortalecer la producción de estadísticas
| oficiales | en  | Colombia. |     |     |     |     |
| --------- | --- | --------- | --- | --- | --- | --- |
Dentro de este proceso, el DANE solicita registros administrativos a entidades
públicas, con el fin de integrarlos en sistemas estadísticos que permitan generar
indicadores confiables sobre contratación pública, gasto estatal, y eficiencia
administrativa.
Los registros administrativos son fundamentales para alimentar bases de datos
estructuradas que cumplen con estándares técnicos y metodológicos definidos
por el DANE. Esto permite que los datos abiertos no solo sean útiles para la
ciudadanía, sino también para la generación de estadísticas oficiales que
| apoyan | la toma |     | de decisiones |     | públicas. |     |
| ------ | ------- | --- | ------------- | --- | --------- | --- |
La articulación entre datos abiertos y registros administrativos fortalece la
transparencia, la interoperabilidad institucional y la calidad de la información
| pública | en Colombia. |     |     |     |     |     |
| ------- | ------------ | --- | --- | --- | --- | --- |
DesdeColombiaCompraEficiente,sehanregistradohasta lafecha tresregistros
administrativos, relacionados conlos procesos ycontratos de compra pública:
| SECOPI:  | Procesos      |     | deCompra     | Pública      |            |         |
| -------- | ------------- | --- | ------------ | ------------ | ---------- | ------- |
| SECOPII: | Contratos     |     | Electrónicos |              |            |         |
| TVEC:    | TIENDAVIRTUAL |     | DEL          | ESTADO       | COLOMBIANO |         |
| Agencia  | Nacional      |     | de           | Contratación |            | Pública |
Página3de23
| Colombia   | Compra        |       | Eficiente |              |          |     |
| ---------- | ------------- | ----- | --------- | ------------ | -------- | --- |
| Dirección: | Carrera       | 7     | # 26 –    | 20 - Bogotá, | Colombia |     |
| Mesa de    | servicio:     | (+57) | 601       | 7456788      |          |     |
| Atención   | al ciudadano: |       | (+57)     | 601 7956600  |          |     |

| 2. Objetivo |     | del | Documento |     |     |     |     |     |
| ----------- | --- | --- | --------- | --- | --- | --- | --- | --- |
Este documento tiene como propósito describir los tres conjuntos de datos
abiertos publicados por la Agencia Nacional de Contratación Pública –
Colombia Compra Eficiente, relacionados con los procesos y contratos de
| compra   | pública |           | en Colombia. |     |     |     |     |     |
| -------- | ------- | --------- | ------------ | --- | --- | --- | --- | --- |
| 3. Marco |         | Normativo |              |     |     |     |     |     |
Para fortalecer la validez técnica y jurídica de los registros administrativos
descritos en este documento, se presenta el marco normativo que respalda su
| elaboración, |       | usoypublicación: |              |     |          |     |     |     |
| ------------ | ----- | ---------------- | ------------ | --- | -------- | --- | --- | --- |
| Normativa    | sobre |                  | contratación |     | pública: |     |     |     |
• Ley 80 de 1993: Estatuto General de Contratación de la Administración
Pública.
• Ley 1150 de 2007: Por la cual se introducen medidas para la eficiencia y
|     | transparencia |     | en  | la  | contrataciónpública. |     |     |     |
| --- | ------------- | --- | --- | --- | -------------------- | --- | --- | --- |
• Decreto 1082 de 2015: Decreto Único Reglamentario del Sector
|           | Administrativo |     | de            | PlaneaciónNacional. |        |           |     |     |
| --------- | -------------- | --- | ------------- | ------------------- | ------ | --------- | --- | --- |
| Normativa | sobre          |     | transparencia |                     | ydatos | abiertos: |     |     |
• Ley 1712 de 2014: Ley de Transparencia y del Derecho de Acceso a la
|     | Información |     | Pública |     | Nacional. |     |     |     |
| --- | ----------- | --- | ------- | --- | --------- | --- | --- | --- |
• Decreto 103 de 2015: Reglamenta la Ley 1712 y establece lineamientos
|     | para | la gestiónde |     | la  | información | pública. |     |     |
| --- | ---- | ------------ | --- | --- | ----------- | -------- | --- | --- |
• CONPES 3920 de 2018: Política Nacional de Explotación de Datos (Big
|           | Data) | yDatos | Abiertos.   |     |           |           |                  |     |
| --------- | ----- | ------ | ----------- | --- | --------- | --------- | ---------------- | --- |
| Normativa | sobre |        | estadística |     | oficial y | registros | administrativos: |     |
• Ley79 de 1993: Por la cualse reorganiza elSistema EstadísticoNacional.
• Decreto 2106 de 2019:Simplificaciónde trámites, incluye disposiciones
|         | sobre          | interoperabilidad |                      |              | yusode | registros | administrativos. |         |
| ------- | -------------- | ----------------- | -------------------- | ------------ | ------ | --------- | ---------------- | ------- |
|         | • Lineamientos |                   | técnicosdelDANEsobre |              |        |           | elproceso        | SICODE. |
| Agencia | Nacional       |                   | de                   | Contratación |        | Pública   |                  |         |
Página4de23
| Colombia   | Compra        |       | Eficiente |         |                    |     |     |     |
| ---------- | ------------- | ----- | --------- | ------- | ------------------ | --- | --- | --- |
| Dirección: | Carrera       | 7     | # 26      | – 20    | - Bogotá, Colombia |     |     |     |
| Mesa       | de servicio:  | (+57) | 601       | 7456788 |                    |     |     |     |
| Atención   | al ciudadano: |       | (+57)     | 601     | 7956600            |     |     |     |

| Normas | específicasmencionadas |     |     |     | en  | eldocumento: |     |     |
| ------ | ---------------------- | --- | --- | --- | --- | ------------ | --- | --- |
• Decreto 248 de 2021: Impulsa la contratación conpequeños productores
agropecuarios.
• Sentencia T-302 de 2017: Protecciónde derechos fundamentales de
|              | comunidades |             |          | indígenas. |     |         |     |     |
| ------------ | ----------- | ----------- | -------- | ---------- | --- | ------- | --- | --- |
| 4. Conjuntos |             |             | de Datos | Incluidos  |     |         |     |     |
| 4.1          | SECOP       | I: Procesos |          | de Compra  |     | Pública |     |     |
El SECOP I (Sistema Electrónico para la Contratación Pública - versión I) es una
plataforma digital dispuesta por la Agencia Nacional de Contratación Pública –
Colombia Compra Eficiente, que permite a las entidades del Estado
colombianopublicar sus procesos de contratación. Básicamente en esta
plataforma solo se da publicidad a los procesos de compra pública, para
| aquellas |     | entidades | que | aún nousan |     | elSECOP | II. |     |
| -------- | --- | --------- | --- | ---------- | --- | ------- | --- | --- |
El SECOP I alimenta conjuntos de datos abiertos como el publicado en
datos.gov.co, (de MinTic) permitiendo que ciudadanos, periodistas,
investigadores y entidades públicas puedan analizar, reutilizar y visualizar la
informaciónpara fines de auditoría, investigación ymejora de políticaspúblicas.
| Funciones |     | del SECOP |     | I   |     |     |     |     |
| --------- | --- | --------- | --- | --- | --- | --- | --- | --- |
• Publicación de procesos de contratación: Las entidades estatales
registran informaciónsobre licitaciones, contratos, adjudicaciones,entre
otros.
• Transparencia: Toda la informaciónes pública, lo que permite elcontrol
|     | ciudadano |     | yelseguimiento |     | por | parte | de organismos | de control. |
| --- | --------- | --- | -------------- | --- | --- | ----- | ------------- | ----------- |
• Historialcontractual: Se puede consultar elhistorial de contratación de
|         | una | entidad  | ocontratista. |              |     |         |     |     |
| ------- | --- | -------- | ------------- | ------------ | --- | ------- | --- | --- |
| Agencia |     | Nacional | de            | Contratación |     | Pública |     |     |
Página5de23
| Colombia   |              | Compra     |           | Eficiente      |          |     |     |     |
| ---------- | ------------ | ---------- | --------- | -------------- | -------- | --- | --- | --- |
| Dirección: |              | Carrera    | 7 # 26    | – 20 - Bogotá, | Colombia |     |     |     |
| Mesa       | de servicio: |            | (+57) 601 | 7456788        |          |     |     |     |
| Atención   | al           | ciudadano: | (+57)     | 601 7956600    |          |     |     |     |

• Cumplimiento normativo: Facilita elcumplimiento de laLey de
|     | Transparencia |     | ydelEstatuto |     | General | de Contratación | Pública. |     |
| --- | ------------- | --- | ------------ | --- | ------- | --------------- | -------- | --- |
Metadatos
| Los | metadatos | asociados |     | a este | registroson: |     |     |     |
| --- | --------- | --------- | --- | ------ | ------------ | --- | --- | --- |
Tipo
Nu Nombredela
|     |     |     | Descripción |     |     | NombredelcampoAPI |     | de  |
| --- | --- | --- | ----------- | --- | --- | ----------------- | --- | --- |
m columna
Dato
Identificadorúnicodelarelación
entreprocesoyadjudicación,
| 1   | UID |     | campoconstituidoporelnúmerode |     |     | uid |     | Texto |
| --- | --- | --- | ----------------------------- | --- | --- | --- | --- | ----- |
constanciayeldeadjudicación,
separadosporunguión
ValorNuméricoparaidentificarel
|     | AñoCargue |     |                             |     |     |                   |     | Númer |
| --- | --------- | --- | --------------------------- | --- | --- | ----------------- | --- | ----- |
| 2   |           |     | añoenqueelprocesofuecargado |     |     | anno_cargue_secop |     |       |
|     | SECOP     |     |                             |     |     |                   |     | o     |
enlaplataformaorma
Valordetextoqueidentificala
fechadefirmadelcontrato,en
AñoFirma
| 3   |     |     | casodenoexistiraúnfirmadel |     |     | anno_firma_contrato |     | Texto |
| --- | --- | --- | -------------------------- | --- | --- | ------------------- | --- | ----- |
Contrato
contrato,elregistrosemarcacomo
nofirmado
Determinaelprimergradode
caracterizacióndelaentidadde
| 4   | NivelEntidad |     |     |     |     | nivel_entidad |     | Texto |
| --- | ------------ | --- | --- | --- | --- | ------------- | --- | ----- |
acuerdoasuorden:Nacionalo
Territorial
Segundoniveldecaracterización,
5 OrdenEntidad quedetallaelordendefinidopara orden_entidad Texto
laentidad
NombredelaEntidaddelEstado
6 NombreEntidad quepublicóelprocesodecompra, nombre_entidad Texto
Entidadcompradoraelproceso
Identificadortributariodelaentidad
7 NITdelaEntidad delEstadoquepublicóelproceso nit_de_la_entidad Texto
decompra,Entidadcompradora
CódigodelaEntidad,utilizado
|     | Códigodela |     |                            |     |     |                      |     | Númer |
| --- | ---------- | --- | -------------------------- | --- | --- | -------------------- | --- | ----- |
| 8   |            |     | comoidentificadorúnicoenla |     |     | c_digo_de_la_entidad |     |       |
|     | Entidad    |     |                            |     |     |                      |     | o     |
plataformaSECOPI
IdentificadordelaModalidadde
selecciónquesedeterminóparael
Númer
| 9   | IDModalidad |     | procesodecompraactual,Ej: |     |     | id_modalidad |     |     |
| --- | ----------- | --- | ------------------------- | --- | --- | ------------ | --- | --- |
o
LicitaciónPública,Contratación
Directa.compra
| Agencia | Nacional |     | de  | Contratación | Pública |     |     |     |
| ------- | -------- | --- | --- | ------------ | ------- | --- | --- | --- |
Página6de23
| Colombia   | Compra        |       | Eficiente |                |          |     |     |     |
| ---------- | ------------- | ----- | --------- | -------------- | -------- | --- | --- | --- |
| Dirección: | Carrera       | 7     | # 26      | – 20 - Bogotá, | Colombia |     |     |     |
| Mesa       | de servicio:  | (+57) | 601       | 7456788        |          |     |     |     |
| Atención   | al ciudadano: |       | (+57)     | 601 7956600    |          |     |     |     |

Tipo
Nu Nombredela
|     |     |     | Descripción |     |     | NombredelcampoAPI | de  |
| --- | --- | --- | ----------- | --- | --- | ----------------- | --- |
m columna
Dato
Modalidaddeselecciónquese
| Modalidadde  |     |     | determinóparaelprocesode   |     |     | modalidad_de_contrata |       |
| ------------ | --- | --- | -------------------------- | --- | --- | --------------------- | ----- |
| 10           |     |     |                            |     |     |                       | Texto |
| contratación |     |     | compraactual,Ej:Licitación |     |     | cion                  |       |
Pública,ContrataciónDirecta.
| Estadodel     |     |     | ElEstadodelprocesoalafechade     |     |     |                         |       |
| ------------- | --- | --- | -------------------------------- | --- | --- | ----------------------- | ----- |
| 11            |     |     |                                  |     |     | estado_del_proceso      | Texto |
| Proceso       |     |     | publicación                      |     |     |                         |       |
| CausaldeOtras |     |     | Encasodeunacontratación          |     |     |                         |       |
| formasde      |     |     | directa,elcampodeterminala       |     |     | causal_de_otras_formas_ |       |
| 12            |     |     |                                  |     |     |                         | Texto |
| contratación  |     |     | causaporlacualsellegaala         |     |     | de                      |       |
| Directa       |     |     | decisióndecontratardirectamente. |     |     |                         |       |
DeterminasiseutilizanlasLeyes80
de1993y1150de2007oensu
IDrégimende defectounrégimenespecialIDdel id_regimen_de_contrata Númer
13
| contratación |     |     | régimenbajoelcuallaentidad |     |     | cion | o   |
| ------------ | --- | --- | -------------------------- | --- | --- | ---- | --- |
desarrollaelprocesodecompra
pública
DeterminasiseutilizanlasLeyes80
| Nombrerégimen  |     |     |                        |     |     | nombre_regimen_de_co |       |
| -------------- | --- | --- | ---------------------- | --- | --- | -------------------- | ----- |
| 14             |     |     | de1993y1150de2007oensu |     |     |                      | Texto |
| decontratación |     |     |                        |     |     | ntratacion           |       |
defectounrégimenespecial
IDdelObjetodelacontratación,
basadoenelcatálogodebienesy
| IDObjetoa |     |     |                                  |     |     |                       | Númer |
| --------- | --- | --- | -------------------------------- | --- | --- | --------------------- | ----- |
| 15        |     |     | serviciosUNSPSC,consultabledesde |     |     | id_objeto_a_contratar |       |
| Contratar |     |     |                                  |     |     |                       | o     |
https://www.colombiacompra.gov.c
o/clasificador-de-bienes-y-servicios
Objetodelacontratación,basado
enelcatálogodebienesyservicios
Objetoa
| 16  |     |     | UNSPSC,consultabledesde |     |     | objeto_a_contratar | Texto |
| --- | --- | --- | ----------------------- | --- | --- | ------------------ | ----- |
Contratar
https://www.colombiacompra.gov.c
o/clasificador-de-bienes-y-servicios
Adicionalalcódigoquedefineel
| Detalledel |     |     | objetodelcontrato,seregistraun |     |     |     |     |
| ---------- | --- | --- | ------------------------------ | --- | --- | --- | --- |
detalle_del_objeto_a_co
| 17 Objetoa |     |     | detalledeladefinicióndelbieno |     |     |     | Texto |
| ---------- | --- | --- | ----------------------------- | --- | --- | --- | ----- |
ntratar
| Contratar |     |     | servicioqueseadquirirádentrodel |     |     |     |     |
| --------- | --- | --- | ------------------------------- | --- | --- | --- | --- |
proceso
TipodeContratoqueserealizará,
| 18 TipoDeContrato |     |     |     |     |     | tipo_de_contrato | Texto |
| ----------------- | --- | --- | --- | --- | --- | ---------------- | ----- |
ejemplos:Fiducia,Obra,entreotros.
| Municipiode |     |     | Municipioenelquesedesarrollael |     |     |                        |       |
| ----------- | --- | --- | ------------------------------ | --- | --- | ---------------------- | ----- |
| 19          |     |     |                                |     |     | municipio_de_obtencion | Texto |
| obtención   |     |     | procesodecomprapública         |     |     |                        |       |
| Municipiode |     |     | Municipioenelquesehacela       |     |     |                        |       |
| 20          |     |     |                                |     |     | municipio_de_entrega   | Texto |
| Entrega     |     |     | entregadelbienoservicio        |     |     |                        |       |
Municipiosenlosquesedesarrollará
Municipios
| 21  |     |     | elobjetodelprocesodecompra |     |     | municipios_ejecucion | Texto |
| --- | --- | --- | -------------------------- | --- | --- | -------------------- | ----- |
ejecución
pública
Marca
|     |     |     | Fechaenlaquesehizoelregistro |     |     |     | de  |
| --- | --- | --- | ---------------------------- | --- | --- | --- | --- |
FechadeCargue delprocesodecompraenla fecha_de_cargue_en_el tiemp
22
| enelSECOP |     |     | plataforma,entregadaenformato |     |     | _secop | o       |
| --------- | --- | --- | ----------------------------- | --- | --- | ------ | ------- |
|           |     |     | DDMMYYYY                      |     |     |        | variabl |
e
| Agencia | Nacional |     | de  | Contratación | Pública |     |     |
| ------- | -------- | --- | --- | ------------ | ------- | --- | --- |
Página7de23
| Colombia   | Compra        |       | Eficiente |                       |     |     |     |
| ---------- | ------------- | ----- | --------- | --------------------- | --- | --- | --- |
| Dirección: | Carrera       | 7     | # 26 –    | 20 - Bogotá, Colombia |     |     |     |
| Mesa de    | servicio:     | (+57) | 601       | 7456788               |     |     |     |
| Atención   | al ciudadano: |       | (+57)     | 601 7956600           |     |     |     |

Tipo
Nu Nombredela
|     |     | Descripción |     |     | NombredelcampoAPI | de  |
| --- | --- | ----------- | --- | --- | ----------------- | --- |
m columna
Dato
| Numerode   |     | Identificadordelprocesode |     |     |                      |       |
| ---------- | --- | ------------------------- | --- | --- | -------------------- | ----- |
| 23         |     |                           |     |     | numero_de_constancia | Texto |
| Constancia |     | compra,generadoporSECOPI  |     |     |                      |       |
Identificadordelproceso,de
Numerode
| 24  |     | acuerdoconlanomenclaturadela |     |     | numero_de_proceso | Texto |
| --- | --- | ---------------------------- | --- | --- | ----------------- | ----- |
Proceso
entidad
Identificadordelcontrato,de
Numerode
| 25  |     | acuerdoconlanomenclaturadela |     |     | numero_de_contrato | Texto |
| --- | --- | ---------------------------- | --- | --- | ------------------ | ----- |
Contrato
entidad
|                   |     | Valorporelcualselanzaelproceso |     |     |                 | Númer |
| ----------------- | --- | ------------------------------ | --- | --- | --------------- | ----- |
| 26 cuantíaProceso |     |                                |     |     | cuantia_proceso |       |
|                   |     | decompra                       |     |     |                 | o     |
IDdelaCategorizacióninicialdel
bienoserviciodefinidoenel
procesodecompra,deacuerdo
consuscaracterísticasprincipales,
| 27 IDGrupo |     | constituyeelprimernivelde |     |     | id_grupo | Texto |
| ---------- | --- | ------------------------- | --- | --- | -------- | ----- |
clasificaciónUNSPSC,consultable
desde
https://www.colombiacompra.gov.c
o/clasificador-de-bienes-y-servicios
Categorizacióninicialdelbieno
serviciodefinidoenelprocesode
compra,deacuerdoconsus
característicasprincipales,
| 28 NombreGrupo |     | constituyeelprimernivelde |     |     | nombre_grupo | Texto |
| -------------- | --- | ------------------------- | --- | --- | ------------ | ----- |
clasificaciónUNSPSC,consultable
desde
https://www.colombiacompra.gov.c
o/clasificador-de-bienes-y-servicios
IDdelsegundoniveldela
Categorizacióndelbienoservicio
definidoenelprocesodecompra,
deacuerdoconsuscaracterísticas
29 IDFamilia principales,constituyeelprimernivel id_familia Texto
declasificaciónUNSPSC,
consultabledesde
https://www.colombiacompra.gov.c
o/clasificador-de-bienes-y-servicios
SegundoniveldelaCategorización
delbienoserviciodefinidoenel
procesodecompra,deacuerdoa
suscaracterísticasprincipales,
30 NombreFamilia constituyeelprimernivelde nombre_familia Texto
clasificaciónUNSPSC,consultable
desde
https://www.colombiacompra.gov.c
o/clasificador-de-bienes-y-servicios
| Agencia | Nacional | de Contratación |     | Pública |     |     |
| ------- | -------- | --------------- | --- | ------- | --- | --- |
Página8de23
| Colombia   | Compra          | Eficiente   |                    |     |     |     |
| ---------- | --------------- | ----------- | ------------------ | --- | --- | --- |
| Dirección: | Carrera 7       | # 26 – 20   | - Bogotá, Colombia |     |     |     |
| Mesa de    | servicio: (+57) | 601 7456788 |                    |     |     |     |
| Atención   | al ciudadano:   | (+57) 601   | 7956600            |     |     |     |

Tipo
Nu Nombredela
|     |     |     | Descripción |     |     | NombredelcampoAPI | de  |
| --- | --- | --- | ----------- | --- | --- | ----------------- | --- |
m columna
Dato
IDdeltercerniveldela
Categorizacióndelbienoservicio
definidoenelprocesodecompra,
deacuerdoasuscaracterísticas
31 IDClase principales,constituyeelprimernivel id_clase Texto
declasificaciónUNSPSC,
consultabledesde
https://www.colombiacompra.gov.c
o/clasificador-de-bienes-y-servicios
TercerniveldelaCategorizacióndel
bienoserviciodefinidoenel
procesodecompra,deacuerdoa
suscaracterísticasprincipales,
| 32 NombreClase |     |     | constituyeelprimernivelde |     |     | nombre_clase | Texto |
| -------------- | --- | --- | ------------------------- | --- | --- | ------------ | ----- |
clasificaciónUNSPSC,consultable
desde
https://www.colombiacompra.gov.c
o/clasificador-de-bienes-y-servicios
Identificadordelaadjudicación
| 33 IDadjudicación |     |     |     |     |     | id_adjudicacion | Texto |
| ----------------- | --- | --- | --- | --- | --- | --------------- | ----- |
hechasenelprocesodecompra
Tipo
|                      |     |     | TipodeIdentificacióndelcontratista |     |     | tipo_identifi_del_contrati |       |
| -------------------- | --- | --- | ---------------------------------- | --- | --- | -------------------------- | ----- |
| 34 Identificacióndel |     |     |                                    |     |     |                            | Texto |
|                      |     |     | seleccionadoenlaadjudicación       |     |     | sta                        |       |
Contratista
identificacióndel Identificacióndelcontratista identificacion_del_contr
| 35          |     |     |                              |     |     |        | Texto |
| ----------- | --- | --- | ---------------------------- | --- | --- | ------ | ----- |
| Contratista |     |     | seleccionadoenlaadjudicación |     |     | atista |       |
NombreoRazónSocialdel
| NomrazónSocial |     |     |                             |     |     | nom_razon_social_contr |       |
| -------------- | --- | --- | --------------------------- | --- | --- | ---------------------- | ----- |
| 36             |     |     | contratistaseleccionadoenla |     |     |                        | Texto |
| Contratista    |     |     |                             |     |     | atista                 |       |
adjudicación
DepartamentoyMunicipioenel
DptoyMuni
| 37  |     |     | cualoperaelcontratista |     |     | dpto_y_muni_contratista | Texto |
| --- | --- | --- | ---------------------- | --- | --- | ----------------------- | ----- |
Contratista
seleccionadoenlaadjudicación
Encasodequeeladjudicadosea
| TipoDoc |     |     | unapersonajurídica,eltipode |     |     |     |     |
| ------- | --- | --- | --------------------------- | --- | --- | --- | --- |
tipo_doc_representante_
| 38 Representante |     |     | identificacióndelrepresentante |     |     |     | Texto |
| ---------------- | --- | --- | ------------------------------ | --- | --- | --- | ----- |
legal
| Legal |     |     | legaldelaempresaseleccionada |     |     |     |     |
| ----- | --- | --- | ---------------------------- | --- | --- | --- | --- |
enlaadjudicación
Encasodequeeladjudicadosea
| Identific. |     |     | unapersonajurídica,registrala |     |     |     |     |
| ---------- | --- | --- | ----------------------------- | --- | --- | --- | --- |
identific_representante_l
| 39 Representante |     |     | identificacióndelrepresentante |     |     |     | Texto |
| ---------------- | --- | --- | ------------------------------ | --- | --- | --- | ----- |
egal
| Legal |     |     | legaldelaempresaseleccionada |     |     |     |     |
| ----- | --- | --- | ---------------------------- | --- | --- | --- | --- |
enlaadjudicación
Encasodequeeladjudicadosea
unapersonajurídica,registrael
| Nombredel     |     |     |                               |     |     | nombre_del_represen_le |       |
| ------------- | --- | --- | ----------------------------- | --- | --- | ---------------------- | ----- |
| 40            |     |     | nombredelrepresentantelegalde |     |     |                        | Texto |
| RepresenLegal |     |     |                               |     |     | gal                    |       |
laempresaseleccionadaenla
adjudicación
Marca
FechadeFirma Fechaenquesehacelafirmadel fecha_de_firma_del_con
| 41          |     |     |                            |     |     |       | de  |
| ----------- | --- | --- | -------------------------- | --- | --- | ----- | --- |
| delContrato |     |     | contratocorrespondienteala |     |     | trato |     |
tiemp
| Agencia | Nacional |     | de  | Contratación | Pública |     |     |
| ------- | -------- | --- | --- | ------------ | ------- | --- | --- |
Página9de23
| Colombia   | Compra        |       | Eficiente |                       |     |     |     |
| ---------- | ------------- | ----- | --------- | --------------------- | --- | --- | --- |
| Dirección: | Carrera       | 7     | # 26 –    | 20 - Bogotá, Colombia |     |     |     |
| Mesa de    | servicio:     | (+57) | 601       | 7456788               |     |     |     |
| Atención   | al ciudadano: |       | (+57)     | 601 7956600           |     |     |     |

Tipo
Nu Nombredela
|     |     |     | Descripción |     |     | NombredelcampoAPI | de  |
| --- | --- | --- | ----------- | --- | --- | ----------------- | --- |
m columna
Dato
|     |     |     | adjudicacióndelregistro,entregada |     |     |     | o       |
| --- | --- | --- | --------------------------------- | --- | --- | --- | ------- |
|     |     |     | enformatoDDMMYYYY                 |     |     |     | variabl |
e
Marca
de
Fechaenqueinicialaejecucióndel
| FechaIniEjec |     |     |                             |     |     |                         | tiemp |
| ------------ | --- | --- | --------------------------- | --- | --- | ----------------------- | ----- |
| 42           |     |     | contrato,entregadaenformato |     |     | fecha_ini_ejec_contrato |       |
| Contrato     |     |     |                             |     |     |                         | o     |
DDMMYYYY
variabl
e
PlazodeEjecdel Valorsobreelcualsedeterminala plazo_de_ejec_del_contr Númer
43
| Contrato |     |     | duracióndelcontrato |     |     | ato | o   |
| -------- | --- | --- | ------------------- | --- | --- | --- | --- |
RangodeEjec Unidadenlaquesedefineelplazo, rango_de_ejec_del_cont
| 44          |     |     |                          |     |     |      | Texto |
| ----------- | --- | --- | ------------------------ | --- | --- | ---- | ----- |
| delContrato |     |     | puedenserdías,mesesoaños |     |     | rato |       |
TiempoAdiciones Tiempoadicionadoalcontrato,en tiempo_adiciones_en_di Númer
45
| enDias |     |     | días |     |     | as  | o   |
| ------ | --- | --- | ---- | --- | --- | --- | --- |
TiempoAdiciones Tiempoadicionadoalcontrato, tiempo_adiciones_en_m Númer
46
| enMeses |     |     | cuandoesmásdeunmes |     |     | eses | o   |
| ------- | --- | --- | ------------------ | --- | --- | ---- | --- |
Marca
de
Fechaenquefinalizalaejecución
| FechaFinEjec |     |     |                                |     |     |                         | tiemp |
| ------------ | --- | --- | ------------------------------ | --- | --- | ----------------------- | ----- |
| 47           |     |     | delcontrato,entregadaenformato |     |     | fecha_fin_ejec_contrato |       |
| Contrato     |     |     |                                |     |     |                         | o     |
DDMMYYYY
variabl
e
Encasodetenerregistro
| Compromiso   |     |     |                               |     |     | compromiso_presupuest |       |
| ------------ | --- | --- | ----------------------------- | --- | --- | --------------------- | ----- |
| 48           |     |     | presupuestal,elcampomuestrael |     |     |                       | Texto |
| Presupuestal |     |     |                               |     |     | al                    |       |
códigocorrespondiente
Númer
49 cuantíaContrato Valorporelcualsefirmaelcontrato cuantia_contrato
o
| ValorTotalde |     |     | Valordelasumadelasadiciones |     |     |                          | Númer |
| ------------ | --- | --- | --------------------------- | --- | --- | ------------------------ | ----- |
| 50           |     |     |                             |     |     | valor_total_de_adiciones |       |
| Adiciones    |     |     | hechasalcontrato            |     |     |                          | o     |
ValorContrato Valortotaldelcontrato,incluyendo valor_contrato_con_adic Númer
51
| conAdiciones |     |     | lasadiciones |     |     | iones | o   |
| ------------ | --- | --- | ------------ | --- | --- | ----- | --- |
Objetodel
|                |     |     | Objetodelcontratoalmomentode |     |     | objeto_del_contrato_a_l |       |
| -------------- | --- | --- | ---------------------------- | --- | --- | ----------------------- | ----- |
| 52 Contratoala |     |     |                              |     |     |                         | Texto |
|                |     |     | lafirma                      |     |     | a                       |       |
Firma
Listadodelosproponentes
| Proponentes   |     |     |                            |     |     | proponentes_selecciona |       |
| ------------- | --- | --- | -------------------------- | --- | --- | ---------------------- | ----- |
| 53            |     |     | seleccionadosenelprocesode |     |     |                        | Texto |
| Seleccionados |     |     |                            |     |     | dos                    |       |
compra
Calificacióndefinitivadelos
calificación
54 proponentesdentrodelprocesode calificacion_definitiva Texto
Definitiva
compra
IdentificadorynombredelaSub
| IDSubUnidad |     |     | Unidaddeejecucionde            |     |     | id_sub_unidad_ejecutor |       |
| ----------- | --- | --- | ------------------------------ | --- | --- | ---------------------- | ----- |
| 55          |     |     |                                |     |     |                        | Texto |
| Ejecutora   |     |     | presupuestoasignadaalprocesode |     |     | a                      |       |
compra
IdentificadorynombredelaSub
| NombreSub       |     |     | Unidaddeejecucionde            |     |     | nombre_sub_unidad_eje |       |
| --------------- | --- | --- | ------------------------------ | --- | --- | --------------------- | ----- |
| 56              |     |     |                                |     |     |                       | Texto |
| UnidadEjecutora |     |     | presupuestoasignadaalprocesode |     |     | cutora                |       |
compra
| Agencia | Nacional |     | de  | Contratación | Pública |     |     |
| ------- | -------- | --- | --- | ------------ | ------- | --- | --- |
Página10de23
| Colombia   | Compra        |       | Eficiente |                       |     |     |     |
| ---------- | ------------- | ----- | --------- | --------------------- | --- | --- | --- |
| Dirección: | Carrera       | 7     | # 26 –    | 20 - Bogotá, Colombia |     |     |     |
| Mesa de    | servicio:     | (+57) | 601       | 7456788               |     |     |     |
| Atención   | al ciudadano: |       | (+57)     | 601 7956600           |     |     |     |

Tipo
Nu Nombredela
|     |     |     | Descripción |     |     | NombredelcampoAPI | de  |
| --- | --- | --- | ----------- | --- | --- | ----------------- | --- |
m columna
Dato
Rutadelprocesodecompraen
| RutaProcesoen |     |     |                             |     |     | ruta_proceso_en_secop_ |     |
| ------------- | --- | --- | --------------------------- | --- | --- | ---------------------- | --- |
| 57            |     |     | SECOP,parahacerconsultadela |     |     |                        | URL |
| SECOPI        |     |     |                             |     |     | i                      |     |
informacióndetallada
Monedaenlacualestanregistradas
| 58 Moneda |     |     |     |     |     | moneda | Texto |
| --------- | --- | --- | --- | --- | --- | ------ | ----- |
lascuantíasdelprocesodecompra
Marcadorqueindicasielproceso
decomprapúblicaestá
Númer
| 59 EsPostConflicto |     |     | enmarcadoenlasaccionesde |     |     | es_postconflicto |     |
| ------------------ | --- | --- | ------------------------ | --- | --- | ---------------- | --- |
o
postconflictodelacuerdodepaz
delaño2017
| marcación |     |     | Marcacióndesielprocesotiene |     |     |                     | Númer |
| --------- | --- | --- | --------------------------- | --- | --- | ------------------- | ----- |
| 60        |     |     |                             |     |     | marcacion_adiciones |       |
| Adiciones |     |     | adicionesregistradas        |     |     |                     | o     |
Posición(Identificador)delRubro
| 61 PosiciónRubro |     |     |     |     |     | posicion_rubro | Texto |
| ---------------- | --- | --- | --- | --- | --- | -------------- | ----- |
presupuestal
NombredelRubroPresupuestalal
| 62 NombreRubro |     |     |     |     |     | nombre_rubro | Texto |
| -------------- | --- | --- | --- | --- | --- | ------------ | ----- |
quecorrespondeelproceso
|               |     |     | ValordelRubropresupuestal |     |     |             | Númer |
| ------------- | --- | --- | ------------------------- | --- | --- | ----------- | ----- |
| 63 ValorRubro |     |     |                           |     |     | valor_rubro |       |
|               |     |     | asignadoalproceso         |     |     |             | o     |
SexodelRepresentantelegaldela
| 64 SexoRepLegal |     |     |     |     |     | sexo_replegal | Texto |
| --------------- | --- | --- | --- | --- | --- | ------------- | ----- |
entidadcompradora
Pilar,delacuerdodepazdelaño
65 PilarAcuerdoPaz 2016,sobreelcualsedesarrollael pilar_acuerdo_paz Texto
procesodecompra
Puntodelacuerdodepazdelaño
| PuntoAcuerdo |     |     | 2016,alqueserelacionaelobjeto |     |     |                   |       |
| ------------ | --- | --- | ----------------------------- | --- | --- | ----------------- | ----- |
| 66           |     |     |                               |     |     | punto_acuerdo_paz | Texto |
| Paz          |     |     | decontratacióndelprocesode    |     |     |                   |       |
compra
Municipioenelqueseencuentra
67 MunicipioEntidad registradalaentidadestatal municipio_entidad Texto
compradora
Departamentoenelquese
Departamento
| 68  |     |     | encuentraregistradalaentidad |     |     | departamento_entidad | Texto |
| --- | --- | --- | ---------------------------- | --- | --- | -------------------- | ----- |
Entidad
estatalcompradora
Marca
Parasuplirrequerimientosde
de
timestamp,seregistralaúltima
| Ultima        |     |     |                               |     |     |                      | tiemp |
| ------------- | --- | --- | ----------------------------- | --- | --- | -------------------- | ----- |
| 69            |     |     | fechademodificacióndelproceso |     |     | ultima_actualizacion |       |
| actualización |     |     |                               |     |     |                      | o     |
decompra,entregadosenformato
variabl
DDMMYYYY
e
Marca
de
|                     |     |     | Fechaenquefueliquidadoel |     |     |                   | tiemp |
| ------------------- | --- | --- | ------------------------ | --- | --- | ----------------- | ----- |
| 70 Fechaliquidación |     |     |                          |     |     | fecha_liquidacion |       |
|                     |     |     | contrato                 |     |     |                   | o     |
variabl
e
Indicasielrequerimientodelbieno
| CumpleDecreto |     |     | serviciotienecaracteristicasquelo |     |     |                  |       |
| ------------- | --- | --- | --------------------------------- | --- | --- | ---------------- | ----- |
| 71            |     |     |                                   |     |     | cumpledecreto248 | Texto |
| 248           |     |     | catalogancomocandidatoa           |     |     |                  |       |
recibireltratamientoestipuladoen
| Agencia | Nacional |     | de  | Contratación | Pública |     |     |
| ------- | -------- | --- | --- | ------------ | ------- | --- | --- |
Página11de23
| Colombia   | Compra        |       | Eficiente |                       |     |     |     |
| ---------- | ------------- | ----- | --------- | --------------------- | --- | --- | --- |
| Dirección: | Carrera       | 7     | # 26 –    | 20 - Bogotá, Colombia |     |     |     |
| Mesa de    | servicio:     | (+57) | 601       | 7456788               |     |     |     |
| Atención   | al ciudadano: |       | (+57)     | 601 7956600           |     |     |     |

Tipo
Nu Nombredela
|     |     | Descripción |     |     | NombredelcampoAPI | de  |
| --- | --- | ----------- | --- | --- | ----------------- | --- |
m columna
Dato
eldecreto248delaño2021,que
buscaimpulsareldesarrollodelos
pequeñosagricultores
Indicasielprocesoincluyearticulos
IncluyeBienesDec
72 directamenterelacionadosconel incluyebienesdecreto248 Texto
reto248
decreto248delaño2021
| Cumple        |     | Indicasicumpleonoconla |     |     |                       |       |
| ------------- | --- | ---------------------- | --- | --- | --------------------- | ----- |
| 73            |     |                        |     |     | cumple_sentencia_t302 | Texto |
| SentenciaT302 |     | sentenciaT302          |     |     |                       |       |
Indicasilaentidadcompradoraes
| 74 EsMiPyme |     |     |     |     | es_mipyme | Texto |
| ----------- | --- | --- | --- | --- | --------- | ----- |
Mipyme
Indicaeltamañodelaentidad
| 75 TamañoMipyme |     |     |     |     | tama_o_mipyme | Texto |
| --------------- | --- | --- | --- | --- | ------------- | ----- |
compradora
Núm
| 76 CódigoBPIN |     | CodigoBPINdelContrato |     |     | codigo_bpin |     |
| ------------- | --- | --------------------- | --- | --- | ----------- | --- |
ero
| La llave | única | asociada |     |     |     |     |
| -------- | ----- | -------- | --- | --- | --- | --- |
UID
Frecuencia
| Elste registro | se actualiza | Diariamente |     |     |     |     |
| -------------- | ------------ | ----------- | --- | --- | --- | --- |
Cobertura
Este registro administrativo contiene dos vistas: una histórica con procesos de
compra publicados desde su origen hasta el 31 de diciembre del 2017 y cuenta
con aproximadamente 6.122.471 y el otro desde el 1 de enero de 2018 hasta la
fecha(31deagostode2025)ycuentaconaproximadamente6.154.604registros.
URL: SECOP I- Procesos de Compra Pública| Datos Abiertos Colombia
SECOPI-ProcesosdeCompraPúblicaHistorico|DatosAbiertosColombia
| Campos | Relevantes |     |     |     |     |     |
| ------ | ---------- | --- | --- | --- | --- | --- |
• - UID
| • - Nombre    | Entidad              |                 |     |         |     |     |
| ------------- | -------------------- | --------------- | --- | ------- | --- | --- |
| • - Modalidad |                      | de Contratación |     |         |     |     |
| • - Objetoa   | Contratar            |                 |     |         |     |     |
| • - Valor     | ContratoconAdiciones |                 |     |         |     |     |
| • - Fecha     | Firma                | Contrato        |     |         |     |     |
| Agencia       | Nacional             | de Contratación |     | Pública |     |     |
Página12de23
| Colombia   | Compra          | Eficiente   |                    |     |     |     |
| ---------- | --------------- | ----------- | ------------------ | --- | --- | --- |
| Dirección: | Carrera 7       | # 26 – 20   | - Bogotá, Colombia |     |     |     |
| Mesa de    | servicio: (+57) | 601 7456788 |                    |     |     |     |
| Atención   | al ciudadano:   | (+57) 601   | 7956600            |     |     |     |

| 4.2 | SECOP |     | II: Contratos |     | Electrónicos |     |     |     |     |     |     |
| --- | ----- | --- | ------------- | --- | ------------ | --- | --- | --- | --- | --- | --- |
El SECOP II (Sistema Electrónico para la Contratación Pública - versión II) es una
plataforma digital dispuesta por Colombia Compra Eficiente que representa una
evolución del SECOP I. Mientras que el SECOP I se enfoca en la publicación de
informacióncontractual,elSECOPIIesuna plataformatransaccional quepermite
| realizar |     | todoelproceso |     |     | decontrataciónen |     |     | línea |     |     |     |
| -------- | --- | ------------- | --- | --- | ---------------- | --- | --- | ----- | --- | --- | --- |
Funciona como una plataforma transaccional con cuentas para las Entidades
Estatales y los Proveedores. Cada cuenta tiene unos usuarios asociados a ella.
Desde sus cuentas las Entidades Estatales crean, evalúan y adjudican Procesos
de Contratación. Los Proveedores pueden hacer comentarios a los Documentos
del Proceso, presentar ofertas yseguir elprocesode selecciónen línea.
| Características |     |     | principales |     | del | SECOP | II  |     |     |     |     |
| --------------- | --- | --- | ----------- | --- | --- | ----- | --- | --- | --- | --- | --- |
• Transaccionalidad: Las entidades estatales pueden crear, evaluar,
|     |     | adjudicar    |     | y hacer |                | seguimiento |     | a los | procesos | de  | contratación |
| --- | --- | ------------ | --- | ------- | -------------- | ----------- | --- | ----- | -------- | --- | ------------ |
|     |     | directamente |     | en      | la plataforma. |             |     |       |          |     |              |
• Interacción con proveedores: Los proveedores pueden consultar
oportunidades, presentar ofertas, hacer observaciones yseguir el proceso
|     |     | de selección |     | en  | tiempo | real. |     |     |     |     |     |
| --- | --- | ------------ | --- | --- | ------ | ----- | --- | --- | --- | --- | --- |
Cuentas personalizadas: Tanto entidades como proveedores tienen
•
cuentas con usuarios asociados, lo que permite una gestión segura y
trazable.
• Transparencia y trazabilidad: Toda la información queda registrada y
disponible para consulta pública, fortaleciendo el control ciudadano y la
rendicióndecuentas.
Metadatos
| Los | metadatos  |     | asociados |     | a   | este registroson: |     |     |                |     |        |
| --- | ---------- | --- | --------- | --- | --- | ----------------- | --- | --- | -------------- | --- | ------ |
| Nu  | Nombredela |     |           |     |     |                   |     |     | Nombredelcampo |     | Tipode |
Descripción
|     | m         | columna |     |                               |     |     |     |     |                | API | Dato  |
| --- | --------- | ------- | --- | ----------------------------- | --- | --- | --- | --- | -------------- | --- | ----- |
|     | Nombre    |         |     | Nombredelaentidaddelestadoque |     |     |     |     |                |     |       |
|     |           |         |     |                               |     |     |     |     | nombre_entidad |     | Texto |
|     | 1 Entidad |         |     | publicaelcontrato             |     |     |     |     |                |     |       |
NITdelaentidaddelestadoque
|         | NitEntidad |          |     |                   |              |     |     |         | nit_entidad |     | Número |
| ------- | ---------- | -------- | --- | ----------------- | ------------ | --- | --- | ------- | ----------- | --- | ------ |
|         | 2          |          |     | publicaelcontrato |              |     |     |         |             |     |        |
| Agencia |            | Nacional |     | de                | Contratación |     |     | Pública |             |     |        |
Página13de23
| Colombia   |     | Compra        |       | Eficiente |         |         |          |     |     |     |     |
| ---------- | --- | ------------- | ----- | --------- | ------- | ------- | -------- | --- | --- | --- | --- |
| Dirección: |     | Carrera       | 7     | # 26      | – 20 -  | Bogotá, | Colombia |     |     |     |     |
| Mesa       | de  | servicio:     | (+57) | 601       | 7456788 |         |          |     |     |     |     |
| Atención   |     | al ciudadano: |       | (+57)     | 601     | 7956600 |          |     |     |     |     |

| Nu  | Nombredela |     |     |     |     |     | Nombredelcampo |     | Tipode |
| --- | ---------- | --- | --- | --- | --- | --- | -------------- | --- | ------ |
Descripción
|     | m   | columna |     |     |     |     |     | API | Dato |
| --- | --- | ------- | --- | --- | --- | --- | --- | --- | ---- |
Departamentoenelcualseregistróla
Departament
|     |     |     |     | entidaddelestadoquepublicael |     |     | departamento |     | Texto |
| --- | --- | --- | --- | ---------------------------- | --- | --- | ------------ | --- | ----- |
o
|     | 3   |     |     | contrato |     |     |     |     |     |
| --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- |
Ciudadenelcualseregistróla
|     | Ciudad |     |     | entidaddelestadoquepublicael |     |     | ciudad |     | Texto |
| --- | ------ | --- | --- | ---------------------------- | --- | --- | ------ | --- | ----- |
|     | 4      |     |     | contrato                     |     |     |        |     |       |
Ubicacióncompletadelaentidaddel
|     | Localización |     |     |                            |     |     | localizaci_n |     | Texto |
| --- | ------------ | --- | --- | -------------------------- | --- | --- | ------------ | --- | ----- |
|     | 5            |     |     | estadoquepublicaelcontrato |     |     |              |     |       |
Ordenentidaddelestadoquepublica
|     | Orden |     |     |            |     |     | orden |     | Texto |
| --- | ----- | --- | --- | ---------- | --- | --- | ----- | --- | ----- |
|     | 6     |     |     | elcontrato |     |     |       |     |       |
Sectorentidaddelestadoquepublica
|     | Sector |     |     |            |     |     | sector |     | Texto |
| --- | ------ | --- | --- | ---------- | --- | --- | ------ | --- | ----- |
|     | 7      |     |     | elcontrato |     |     |        |     |       |
Ramadelestadodelaentidadque
|     | Rama           |     |     |                                    |     |     | rama                 |     | Texto |
| --- | -------------- | --- | --- | ---------------------------------- | --- | --- | -------------------- | --- | ----- |
|     | 8              |     |     | publicaelcontrato                  |     |     |                      |     |       |
|     | Entidad        |     |     | Definesilaentidadesdescentralizada |     |     |                      |     |       |
|     |                |     |     |                                    |     |     | entidad_centralizada |     | Texto |
|     | 9 Centralizada |     |     | ocentralizada                      |     |     |                      |     |       |
|     | Procesode      |     |     | Identificadordelprocesodecompra    |     |     |                      |     |       |
|     |                |     |     |                                    |     |     | proceso_de_compra    |     | Texto |
| 10  | Compra         |     |     | publicado                          |     |     |                      |     |       |
Identificadordelcontratofirmado,
|     | IDContrato |     |     |                         |     |     | id_contrato |     | Texto |
| --- | ---------- | --- | --- | ----------------------- | --- | --- | ----------- | --- | ----- |
| 11  |            |     |     | generadoporlaplataforma |     |     |             |     |       |
Referencia Identificadordelcontratofirmado, referencia_del_contra
Texto
| 12  | delContrato |     |     | generadoporlaentidaddelestado |     |     | to              |     |       |
| --- | ----------- | --- | --- | ----------------------------- | --- | --- | --------------- | --- | ----- |
|     | Estado      |     |     | Estadodelcontrato,frenteasu   |     |     |                 |     |       |
|     |             |     |     |                               |     |     | estado_contrato |     | Texto |
| 13  | Contrato    |     |     | ejecución,firmaoliquidación   |     |     |                 |     |       |
Códigode
|     |           |     |     | CodigoUNSPSCdelacategoría |     |     | codigo_de_categoria |     |       |
| --- | --------- | --- | --- | ------------------------- | --- | --- | ------------------- | --- | ----- |
|     | categoría |     |     |                           |     |     |                     |     | Texto |
|     |           |     |     | principalparaelcontrato   |     |     | _principal          |     |       |
14 Principal
descripción Descripcióndelobjetodelprocesode descripcion_del_proc
Texto
| 15  | delProceso |     |     | compra                     |     |     | eso              |     |       |
| --- | ---------- | --- | --- | -------------------------- | --- | --- | ---------------- | --- | ----- |
|     | Tipode     |     |     | Tipodecontratodeacuerdoasu |     |     |                  |     |       |
|     |            |     |     |                            |     |     | tipo_de_contrato |     | Texto |
| 16  | Contrato   |     |     | marcojurídico              |     |     |                  |     |       |
Modalidad
|     |     |     |     | Modalidaddecontrataciónde  |     |     | modalidad_de_contra |     |       |
| --- | --- | --- | --- | -------------------------- | --- | --- | ------------------- | --- | ----- |
|     | de  |     |     |                            |     |     |                     |     | Texto |
|     |     |     |     | acuerdoalmodelodeselección |     |     | tacion              |     |       |
17 contratación
|     | justificación |     |     | Justificacióndelamodalidad,el |     |     |                        |     |     |
| --- | ------------- | --- | --- | ----------------------------- | --- | --- | ---------------------- | --- | --- |
|     | Modalidad     |     |     | escenariobajoelcualsetomala   |     |     | justificacion_modalida |     |     |
Texto
|     | de           |     |     | decisióndedefinirunauotra |     |     | d_de |     |     |
| --- | ------------ | --- | --- | ------------------------- | --- | --- | ---- | --- | --- |
| 18  | contratación |     |     | modalidaddecontratación   |     |     |      |     |     |
Marcade
|     | Fechade   |     |     | Fechadefirmadelcontrato        |     |     |                       |     |          |
| --- | --------- | --- | --- | ------------------------------ | --- | --- | --------------------- | --- | -------- |
|     |           |     |     |                                |     |     | fecha_de_firma        |     | tiempo   |
|     | Firma     |     |     | electronico                    |     |     |                       |     |          |
| 19  |           |     |     |                                |     |     |                       |     | variable |
|     | Fechade   |     |     |                                |     |     |                       |     | Marcade  |
|     |           |     |     | Fechadeiniciodelas             |     |     | fecha_de_inicio_del_c |     |          |
|     | Iniciodel |     |     |                                |     |     |                       |     | tiempo   |
|     |           |     |     | responsabilidadescontractuales |     |     | ontrato               |     |          |
| 20  | Contrato  |     |     |                                |     |     |                       |     | variable |
Marcade
FechadeFin Fechadefindelasresponsabilidades fecha_de_fin_del_con
tiempo
|     | delContrato |     |     | contractuales |     |     | trato |     |     |
| --- | ----------- | --- | --- | ------------- | --- | --- | ----- | --- | --- |
variable
21
| Agencia |     | Nacional |     | de  | Contratación | Pública |     |     |     |
| ------- | --- | -------- | --- | --- | ------------ | ------- | --- | --- | --- |
Página14de23
| Colombia   |     | Compra        |       | Eficiente |                       |     |     |     |     |
| ---------- | --- | ------------- | ----- | --------- | --------------------- | --- | --- | --- | --- |
| Dirección: |     | Carrera       | 7     | # 26 –    | 20 - Bogotá, Colombia |     |     |     |     |
| Mesa       | de  | servicio:     | (+57) | 601       | 7456788               |     |     |     |     |
| Atención   |     | al ciudadano: |       | (+57)     | 601 7956600           |     |     |     |     |

| Nu  | Nombredela |     |     |     |     |     | Nombredelcampo |     | Tipode |
| --- | ---------- | --- | --- | --- | --- | --- | -------------- | --- | ------ |
Descripción
|     | m         | columna |     |                                 |     |     |                       | API | Dato     |
| --- | --------- | ------- | --- | ------------------------------- | --- | --- | --------------------- | --- | -------- |
|     | Fechade   |         |     |                                 |     |     |                       |     | Marcade  |
|     |           |         |     | Fechadeiniciodelaejecucióndelas |     |     | fecha_de_inicio_de_ej |     |          |
|     | Iniciode  |         |     |                                 |     |     |                       |     | tiempo   |
|     |           |         |     | actividadesdelcontrato          |     |     | ecucion               |     |          |
| 22  | ejecución |         |     |                                 |     |     |                       |     | variable |
Marcade
|     | FechadeFin |     |     | Fechadefindelaejecucióndelas |     |     | fecha_de_fin_de_ejec |     |     |
| --- | ---------- | --- | --- | ---------------------------- | --- | --- | -------------------- | --- | --- |
tiempo
|     | deejecución |     |     | actividadesdelcontrato |     |     | ucion |     |     |
| --- | ----------- | --- | --- | ---------------------- | --- | --- | ----- | --- | --- |
variable
23
|     | Condiciones |     |     | Condicionesbajolascualesse |     |     | condiciones_de_entre |     |     |
| --- | ----------- | --- | --- | -------------------------- | --- | --- | -------------------- | --- | --- |
Texto
| 24  | deEntrega    |     |     | entregaelproductooservicio    |     |     | ga                |     |       |
| --- | ------------ | --- | --- | ----------------------------- | --- | --- | ----------------- | --- | ----- |
|     | TipoDocProve |     |     | Tipodedocumentodelproveedor   |     |     |                   |     |       |
|     |              |     |     |                               |     |     | tipodocproveedor  |     | Texto |
| 25  | edor         |     |     | adjudicado                    |     |     |                   |     |       |
|     | Documento    |     |     | Númerodedocumentodelproveedor |     |     | documento_proveed |     |       |
Texto
| 26  | Proveedor  |     |     | adjudicado                   |     |     | or                  |     |       |
| --- | ---------- | --- | --- | ---------------------------- | --- | --- | ------------------- | --- | ----- |
|     | Proveedor  |     |     |                              |     |     | proveedor_adjudicad |     |       |
|     |            |     |     | Nombredelproveedoradjudicado |     |     |                     |     | Texto |
| 27  | Adjudicado |     |     |                              |     |     | o                   |     |       |
Determinaelproveedoresungrupo
deentidades,existeunconjuntode
|     | EsGrupo |     |     |     |     |     | es_grupo |     | Texto |
| --- | ------- | --- | --- | --- | --- | --- | -------- | --- | ----- |
datosdeCCEquecontienela
| 28  |        |     |     | conformacióndelosgrupos       |     |     |         |     |       |
| --- | ------ | --- | --- | ----------------------------- | --- | --- | ------- | --- | ----- |
| 29  | EsPyme |     |     | DeterminasilaempresaesunaPyme |     |     | es_pyme |     | Texto |
Determinasielcontratotiene
|     | HabilitaPago |     |     |                            |     |     | habilita_pago_adelan |     |       |
| --- | ------------ | --- | --- | -------------------------- | --- | --- | -------------------- | --- | ----- |
|     |              |     |     | habilitadalaopcióndepagode |     |     |                      |     | Texto |
|     | Adelantado   |     |     |                            |     |     | tado                 |     |       |
| 30  |              |     |     | adelantos                  |     |     |                      |     |       |
Determinasielcontratohasido
|     | Liquidación |     |     |           |     |     | liquidaci_n |     | Texto |
| --- | ----------- | --- | --- | --------- | --- | --- | ----------- | --- | ----- |
| 31  |             |     |     | liquidado |     |     |             |     |       |
Determinasielcontratotiene
Obligación
|     |     |     |     | compromisosdecumplimientoa |     |     | obligaci_n_ambiental |     | Texto |
| --- | --- | --- | --- | -------------------------- | --- | --- | -------------------- | --- | ----- |
Ambiental
| 32  |     |     |     | obligacionesambientales |     |     |     |     |     |
| --- | --- | --- | --- | ----------------------- | --- | --- | --- | --- | --- |
Determinasielcontratotiene
|     | Obligaciones |     |     | compromisosdecumplimientoa |     |     | obligaciones_postcon |     |     |
| --- | ------------ | --- | --- | -------------------------- | --- | --- | -------------------- | --- | --- |
Texto
|     | Postconsumo |     |     | obligacionesposterioresalaentrega |     |     | sumo |     |     |
| --- | ----------- | --- | --- | --------------------------------- | --- | --- | ---- | --- | --- |
| 33  |             |     |     | delproductooprestacióndelservicio |     |     |      |     |     |
Determinasielcontratohasido
|     | reversión   |     |     |                            |     |     | reversion             |     | Texto |
| --- | ----------- | --- | --- | -------------------------- | --- | --- | --------------------- | --- | ----- |
| 34  |             |     |     | reversado                  |     |     |                       |     |       |
|     | Origendelos |     |     | OrigendelosRecursos,anivel |     |     | origen_de_los_recurso |     |       |
Texto
| 35  | Recursos |     |     | presupuestal |     |     | s   |     |     |
| --- | -------- | --- | --- | ------------ | --- | --- | --- | --- | --- |
36 DestinoGasto Destinodelgasto,anivelpresupuestal destino_gasto Texto
Valordel
|     |     |     |     | Valortotaldelcontrato |     |     | valor_del_contrato |     | Número |
| --- | --- | --- | --- | --------------------- | --- | --- | ------------------ | --- | ------ |
37 Contrato
Valorde
valor_de_pago_adela
|     | pago |     |     | Valordelpagoporadelantado |     |     |     |     | Número |
| --- | ---- | --- | --- | ------------------------- | --- | --- | --- | --- | ------ |
ntado
38 adelantado
Valor
|     |     |     |     | ValorFacturadoalafecha |     |     | valor_facturado |     | Número |
| --- | --- | --- | --- | ---------------------- | --- | --- | --------------- | --- | ------ |
39 Facturado
Valor
valor_pendiente_de_p
|     | Pendientede |     |     | ValorPendientedePagoalafecha |     |     |     |     | Número |
| --- | ----------- | --- | --- | ---------------------------- | --- | --- | --- | --- | ------ |
ago
40 Pago
| 41  | ValorPagado |     |     | ValorPagadoalafecha |     |     | valor_pagado |     | Número |
| --- | ----------- | --- | --- | ------------------- | --- | --- | ------------ | --- | ------ |
Valor
|     |     |     |     | ValorAmortizadoalafecha |     |     | valor_amortizado |     | Número |
| --- | --- | --- | --- | ----------------------- | --- | --- | ---------------- | --- | ------ |
42 Amortizado
| Agencia |     | Nacional |     | de  | Contratación | Pública |     |     |     |
| ------- | --- | -------- | --- | --- | ------------ | ------- | --- | --- | --- |
Página15de23
| Colombia   |     | Compra        |       | Eficiente |                       |     |     |     |     |
| ---------- | --- | ------------- | ----- | --------- | --------------------- | --- | --- | --- | --- |
| Dirección: |     | Carrera       | 7     | # 26 –    | 20 - Bogotá, Colombia |     |     |     |     |
| Mesa       | de  | servicio:     | (+57) | 601       | 7456788               |     |     |     |     |
| Atención   |     | al ciudadano: |       | (+57)     | 601 7956600           |     |     |     |     |

| Nu  | Nombredela |     |     |     |     |     | Nombredelcampo |     | Tipode |
| --- | ---------- | --- | --- | --- | --- | --- | -------------- | --- | ------ |
Descripción
|     | m   | columna |     |     |     |     |     | API | Dato |
| --- | --- | ------- | --- | --- | --- | --- | --- | --- | ---- |
Valor
ValorPendientedeAmortizacionala
|     | Pendientede |     |     |     |     |     | valor_pendiente_de |     | Número |
| --- | ----------- | --- | --- | --- | --- | --- | ------------------ | --- | ------ |
fecha
43 Amortizacion
Valor
|     |             |     |     | ValorPendientedeEjecucionala |     |     | valor_pendiente_de_e |     |        |
| --- | ----------- | --- | --- | ---------------------------- | --- | --- | -------------------- | --- | ------ |
|     | Pendientede |     |     |                              |     |     |                      |     | Número |
|     |             |     |     | fecha                        |     |     | jecucion             |     |        |
44 ejecución
Estadodeasignacióndelcódigodel
|     | EstadoBPIN |     |     |                             |     |     | estado_bpin |     | Texto |
| --- | ---------- | --- | --- | --------------------------- | --- | --- | ----------- | --- | ----- |
| 45  |            |     |     | BancodeProyectosdeInversión |     |     |             |     |       |
CódigoasociadoalBancode
|     | CódigoBPIN |     |     |                      |     |     | c_digo_bpin |     | Texto |
| --- | ---------- | --- | --- | -------------------- | --- | --- | ----------- | --- | ----- |
| 46  |            |     |     | ProyectosdeInversión |     |     |             |     |       |
Añodeasignacióndelcódigodel
|     | AñoBPIN |     |     |                             |     |     | anno_bpin |     | Texto |
| --- | ------- | --- | --- | --------------------------- | --- | --- | --------- | --- | ----- |
| 47  |         |     |     | BancodeProyectosdeInversión |     |     |           |     |       |
SaldodelCDPasignadoalprocesoy
|     | SaldoCDP       |     |     |                                  |     |     | saldo_cdp          |     | Número |
| --- | -------------- | --- | --- | -------------------------------- | --- | --- | ------------------ | --- | ------ |
| 48  |                |     |     | alcontrato                       |     |     |                    |     |        |
|     | Saldo          |     |     | SaldoactualparalavigenciadelCDP  |     |     |                    |     |        |
|     |                |     |     |                                  |     |     | saldo_vigencia     |     | Número |
| 49  | Vigencia       |     |     | asignadoalprocesoyalcontrato     |     |     |                    |     |        |
|     | EsPostConflict |     |     | Determinasielprocesoestáasociado |     |     |                    |     |        |
|     |                |     |     |                                  |     |     | espostconflicto    |     | Texto  |
| 50  | o              |     |     | aalgúneventodeacuerdodepaz       |     |     |                    |     |        |
|     | días           |     |     | Díasadicionadosalcontrato        |     |     |                    |     |        |
|     |                |     |     |                                  |     |     | dias_adicionados   |     | Número |
| 51  | adicionados    |     |     | electrónico                      |     |     |                    |     |        |
|     | Puntosdel      |     |     | Pilaresdelacuerdodepaz,siel      |     |     |                    |     |        |
|     |                |     |     |                                  |     |     | puntos_del_acuerdo |     | Texto  |
| 52  | Acuerdo        |     |     | contratoespostconflicto          |     |     |                    |     |        |
Pilaresdel
|     |     |     |     | Pilaresdelacuerdodepaz |     |     | pilares_del_acuerdo |     | Texto |
| --- | --- | --- | --- | ---------------------- | --- | --- | ------------------- | --- | ----- |
53 Acuerdo
URLdelprocesodecompraenla
|     | URLProceso |     |     |                   |     |     | urlproceso |     | URL |
| --- | ---------- | --- | --- | ----------------- | --- | --- | ---------- | --- | --- |
| 54  |            |     |     | plataformaSECOPII |     |     |            |     |     |
Nombre
|     |              |     |     | Nombredelrepresentantelegaldela |     |     | nombre_representant |     |       |
| --- | ------------ | --- | --- | ------------------------------- | --- | --- | ------------------- | --- | ----- |
|     | Representant |     |     |                                 |     |     |                     |     | Texto |
|     |              |     |     | entidad                         |     |     | e_legal             |     |       |
55 eLegal
Nacionalidad
|     |              |     |     | Nacionalidaddelrepresentantelegal |     |     | nacionalidad_represe |     |       |
| --- | ------------ | --- | --- | --------------------------------- | --- | --- | -------------------- | --- | ----- |
|     | Representant |     |     |                                   |     |     |                      |     | Texto |
|     |              |     |     | delaentidad                       |     |     | ntante_legal         |     |       |
56 eLegal
Domicilio
|     |              |     |     | Direccióndedomiciliodel       |     |     | domicilio_representan |     |       |
| --- | ------------ | --- | --- | ----------------------------- | --- | --- | --------------------- | --- | ----- |
|     | Representant |     |     |                               |     |     |                       |     | Texto |
|     |              |     |     | representantelegaldelaentidad |     |     | te_legal              |     |       |
57 eLegal
Tipode
Identificación Tipodeidentificacióndel tipo_de_identificaci_n
Texto
Representant representantelegaldelaentidad _representante_legal
58 eLegal
Identificación
|     |              |     |     | Numerodeidentificacióndel     |     |     | identificaci_n_represe |     |       |
| --- | ------------ | --- | --- | ----------------------------- | --- | --- | ---------------------- | --- | ----- |
|     | Representant |     |     |                               |     |     |                        |     | Texto |
|     |              |     |     | representantelegaldelaentidad |     |     | ntante_legal           |     |       |
59 eLegal
Género
|     |              |     |     | Génerosexualdelrepresentantelegal |     |     | g_nero_representante |     |       |
| --- | ------------ | --- | --- | --------------------------------- | --- | --- | -------------------- | --- | ----- |
|     | Representant |     |     |                                   |     |     |                      |     | Texto |
|     |              |     |     | delaentidad                       |     |     | _legal               |     |       |
60 eLegal
|     | Presupuesto |     |     | Valordeorigendelosrecursosque |     |     |     |     |     |
| --- | ----------- | --- | --- | ----------------------------- | --- | --- | --- | --- | --- |
presupuesto_general_
|     | Generaldela |     |     | correspondealPresupuestoGeneral |     |     |     |     | Número |
| --- | ----------- | --- | --- | ------------------------------- | --- | --- | --- | --- | ------ |
de_la_nacion_pgn
| 61      | Nacion–PGN |          |     | delaNacion–PGN |              |         |     |     |     |
| ------- | ---------- | -------- | --- | -------------- | ------------ | ------- | --- | --- | --- |
| Agencia |            | Nacional |     | de             | Contratación | Pública |     |     |     |
Página16de23
| Colombia   |     | Compra        |       | Eficiente |                       |     |     |     |     |
| ---------- | --- | ------------- | ----- | --------- | --------------------- | --- | --- | --- | --- |
| Dirección: |     | Carrera       | 7     | # 26 –    | 20 - Bogotá, Colombia |     |     |     |     |
| Mesa       | de  | servicio:     | (+57) | 601       | 7456788               |     |     |     |     |
| Atención   |     | al ciudadano: |       | (+57)     | 601 7956600           |     |     |     |     |

| Nu  | Nombredela |     |     |     |     |     | Nombredelcampo |     | Tipode |
| --- | ---------- | --- | --- | --- | --- | --- | -------------- | --- | ------ |
Descripción
|     | m   | columna |     |     |     |     |     | API | Dato |
| --- | --- | ------- | --- | --- | --- | --- | --- | --- | ---- |
Sistema
Valordeorigendelosrecursosque
|     | Generalde     |     |     |                               |     |     | sistema_general_de_p |     |        |
| --- | ------------- | --- | --- | ----------------------------- | --- | --- | -------------------- | --- | ------ |
|     |               |     |     | correspondealSistemaGeneralde |     |     |                      |     | Número |
|     | Participacion |     |     |                               |     |     | articipaciones       |     |        |
Participaciones
62 es
|     | Sistema |     |     | Valordeorigendelosrecursosque |     |     |     |     |     |
| --- | ------- | --- | --- | ----------------------------- | --- | --- | --- | --- | --- |
sistema_general_de_r
|     | Generalde |     |     | correspondealSistemaGeneralde |     |     |     |     | Número |
| --- | --------- | --- | --- | ----------------------------- | --- | --- | --- | --- | ------ |
egal_as
| 63  | Regalías |     |     | Regalías |     |     |     |     |     |
| --- | -------- | --- | --- | -------- | --- | --- | --- | --- | --- |
Recursos
Propios
recursos_propios_alcal
(Alcaldías,
|     |             |     |     | Indicaelvalorderecursosdela    |     |     | d_as_gobernaciones_  |     |        |
| --- | ----------- | --- | --- | ------------------------------ | --- | --- | -------------------- | --- | ------ |
|     | Gobernacion |     |     |                                |     |     |                      |     | Número |
|     |             |     |     | entidadenelcontratoelectronico |     |     | y_resguardos_ind_gen |     |        |
esy
as_
Resguardos
64 Indígenas)
|     | Recursosde |     |     | Valordeorigendelosrecursosque |     |     |                     |     |        |
| --- | ---------- | --- | --- | ----------------------------- | --- | --- | ------------------- | --- | ------ |
|     |            |     |     |                               |     |     | recursos_de_credito |     | Número |
| 65  | crédito    |     |     | correspondeaRecursosdeCredito |     |     |                     |     |        |
|     | Recursos   |     |     | Valordeorigendelosrecursosque |     |     |                     |     |        |
|     |            |     |     |                               |     |     | recursos_propios    |     | Número |
| 66  | Propios    |     |     | correspondeaRecursosPropios   |     |     |                     |     |        |
Marcade
|     | Ultima        |     |     | Fechadeúltimaactualizacióndel |     |     |                      |     |        |
| --- | ------------- | --- | --- | ----------------------------- | --- | --- | -------------------- | --- | ------ |
|     |               |     |     |                               |     |     | ultima_actualizacion |     | tiempo |
|     | actualización |     |     | contratoelectronico           |     |     |                      |     |        |
variable
67
|     | Código    |     |     | Codigodelaentidadenla   |     |     |                  |     |        |
| --- | --------- | --- | --- | ----------------------- | --- | --- | ---------------- | --- | ------ |
|     |           |     |     |                         |     |     | codigo_entidad   |     | Número |
| 68  | Entidad   |     |     | plataformaSECOPII       |     |     |                  |     |        |
|     | Código    |     |     | Codigodelproveedorednla |     |     |                  |     |        |
|     |           |     |     |                         |     |     | codigo_proveedor |     | Texto  |
| 69  | Proveedor |     |     | plataformaSECOPII       |     |     |                  |     |        |
Marcade
FechaInicio Fechadeiniciodeliquidacióndel fecha_inicio_liquidaci
tiempo
|     | liquidación |     |     | contratoelectrónico |     |     | on  |     |          |
| --- | ----------- | --- | --- | ------------------- | --- | --- | --- | --- | -------- |
| 70  |             |     |     |                     |     |     |     |     | variable |
Marcade
|     | FechaFin    |     |     | Fechadefindeliquidacióndel |     |     |                       |     |          |
| --- | ----------- | --- | --- | -------------------------- | --- | --- | --------------------- | --- | -------- |
|     |             |     |     |                            |     |     | fecha_fin_liquidacion |     | tiempo   |
|     | liquidación |     |     | contratoelectrónico        |     |     |                       |     |          |
| 71  |             |     |     |                            |     |     |                       |     | variable |
Objetodel
|     |     |     |     | Objetodelcontratoelectrónico |     |     | objeto_del_contrato |     | Texto |
| --- | --- | --- | --- | ---------------------------- | --- | --- | ------------------- | --- | ----- |
72 Contrato
|     | Duracióndel |     |     | Describeladuracióndelcontratoen  |     |     |                       |     |       |
| --- | ----------- | --- | --- | -------------------------------- | --- | --- | --------------------- | --- | ----- |
|     |             |     |     |                                  |     |     | duraci_n_del_contrato |     | Texto |
| 73  | contrato    |     |     | eltiempo                         |     |     |                       |     |       |
|     | Nombredel   |     |     | Indicaelnombredelbancoendonde    |     |     |                       |     |       |
|     |             |     |     |                                  |     |     | nombre_del_banco      |     | Texto |
| 74  | banco       |     |     | seconsignaranlospagosdelcontrato |     |     |                       |     |       |
|     | Tipode      |     |     | Tipodecuentaenlaquesese          |     |     |                       |     |       |
|     |             |     |     |                                  |     |     | tipo_de_cuenta        |     | Texto |
| 75  | cuenta      |     |     | consignaranlospagodelcontrato    |     |     |                       |     |       |
|     | Númerode    |     |     | Numerodecuentaendondeseharan     |     |     |                       |     |       |
|     |             |     |     |                                  |     |     | n_mero_de_cuenta      |     | Texto |
| 76  | cuenta      |     |     | lospagosdelcontrato              |     |     |                       |     |       |
Elcontrato
|     |          |     |     | Indicasielcontratopuedeserono |     |     | el_contrato_puede_se |     |       |
| --- | -------- | --- | --- | ----------------------------- | --- | --- | -------------------- | --- | ----- |
|     | puedeser |     |     |                               |     |     |                      |     | Texto |
|     |          |     |     | prorrogado                    |     |     | r_prorrogado         |     |       |
77 prorrogado
Fechade
Marcade
notificación Inficalafechadenotificacióndela fecha_de_notificaci_n
tiempo
|     | de  |     |     | prorrogacióndelcontrato |     |     | _de_prorrogaci_n |     |     |
| --- | --- | --- | --- | ----------------------- | --- | --- | ---------------- | --- | --- |
variable
78 prorrogación
| Agencia |     | Nacional |     | de  | Contratación | Pública |     |     |     |
| ------- | --- | -------- | --- | --- | ------------ | ------- | --- | --- | --- |
Página17de23
| Colombia   |     | Compra        |       | Eficiente |                       |     |     |     |     |
| ---------- | --- | ------------- | ----- | --------- | --------------------- | --- | --- | --- | --- |
| Dirección: |     | Carrera       | 7     | # 26 –    | 20 - Bogotá, Colombia |     |     |     |     |
| Mesa       | de  | servicio:     | (+57) | 601       | 7456788               |     |     |     |     |
| Atención   |     | al ciudadano: |       | (+57)     | 601 7956600           |     |     |     |     |

| Nu Nombredela |     |     |     |     | Nombredelcampo |     | Tipode |
| ------------- | --- | --- | --- | --- | -------------- | --- | ------ |
Descripción
| m   | columna |     |     |     |     | API | Dato |
| --- | ------- | --- | --- | --- | --- | --- | ---- |
Nombre
|           |     | Describeelnombredelordenadordel |     |     | nombre_ordenador_d |     |       |
| --------- | --- | ------------------------------- | --- | --- | ------------------ | --- | ----- |
| ordenador |     |                                 |     |     |                    |     | Texto |
|           |     | gastodelaentidadcompradora      |     |     | el_gasto           |     |       |
79 delgasto
Tipode
Indicaeltipodedocumentodel
| documento |     |                              |     |     | tipo_de_documento_  |     |       |
| --------- | --- | ---------------------------- | --- | --- | ------------------- | --- | ----- |
|           |     | ordenadordelgastodelaentidad |     |     |                     |     | Texto |
| Ordenador |     |                              |     |     | ordenador_del_gasto |     |       |
compradora
80 delgasto
Númerode
n_mero_de_documen
| documento |     | Indicaelnúmerodedocumentodel |     |     |                      |     |       |
| --------- | --- | ---------------------------- | --- | --- | -------------------- | --- | ----- |
|           |     |                              |     |     | to_ordenador_del_gas |     | Texto |
| Ordenador |     | ordenadordelgasto            |     |     |                      |     |       |
to
81 delgasto
| Nombre        |     | Describeelnombredelsupervisorde |     |     |                   |     |       |
| ------------- | --- | ------------------------------- | --- | --- | ----------------- | --- | ----- |
|               |     |                                 |     |     | nombre_supervisor |     | Texto |
| 82 supervisor |     | laentidadcompradora             |     |     |                   |     |       |
Tipode
|           |     | Indicaeltipodedocumentodel      |     |     | tipo_de_documento_s |     |       |
| --------- | --- | ------------------------------- | --- | --- | ------------------- | --- | ----- |
| documento |     |                                 |     |     |                     |     | Texto |
|           |     | supervisordelaentidadcompradora |     |     | upervisor           |     |       |
83 supervisor
Númerode
|           |     | Indicaelnúmerodedocumentodel |     |     | n_mero_de_documen |     |       |
| --------- | --- | ---------------------------- | --- | --- | ----------------- | --- | ----- |
| documento |     |                              |     |     |                   |     | Texto |
|           |     | supervisor                   |     |     | to_supervisor     |     |       |
84 supervisor
Nombre
|           |     | DescribeelnombredelOrdenadorde |     |     | nombre_ordenador_d |     |       |
| --------- | --- | ------------------------------ | --- | --- | ------------------ | --- | ----- |
| Ordenador |     |                                |     |     |                    |     | Texto |
|           |     | Pagodelaentidadcompradora      |     |     | e_pago             |     |       |
85 dePago
Tipode
Indicaeltipodedocumentodel
| documento |     |                            |     |     | tipo_de_documento_ |     |       |
| --------- | --- | -------------------------- | --- | --- | ------------------ | --- | ----- |
|           |     | OrdenadordePagodelaentidad |     |     |                    |     | Texto |
| Ordenador |     |                            |     |     | ordenador_de_pago  |     |       |
compradora
86 dePago
Númerode
n_mero_de_documen
| documento |     | Indicaelnúmerodedocumentodel |     |     |                    |     |       |
| --------- | --- | ---------------------------- | --- | --- | ------------------ | --- | ----- |
|           |     |                              |     |     | to_ordenador_de_pa |     | Texto |
| Ordenador |     | OrdenadordePago              |     |     |                    |     |       |
go
87 dePago
| La llave | única | asociada |     |     |     |     |     |
| -------- | ----- | -------- | --- | --- | --- | --- | --- |
ID Contrato
Frecuencia
| Este registrose |     | actualiza | Diariamente |     |     |     |     |
| --------------- | --- | --------- | ----------- | --- | --- | --- | --- |
Cobertura
Este registro administrativo contiene una vista: con aproximadamente 4.775.550
| contratos | publicados |     | desde 2013 | a la fecha(31 | de agosto2025) |     |     |
| --------- | ---------- | --- | ---------- | ------------- | -------------- | --- | --- |
URL: SECOP II - Contratos Electrónicos | Datos Abiertos Colombia
| Campos | Relevantes |     |     |     |     |     |     |
| ------ | ---------- | --- | --- | --- | --- | --- | --- |
• - ID Contrato
| Agencia | Nacional | de  | Contratación | Pública |     |     |     |
| ------- | -------- | --- | ------------ | ------- | --- | --- | --- |
Página18de23
| Colombia   | Compra        |           | Eficiente      |          |     |     |     |
| ---------- | ------------- | --------- | -------------- | -------- | --- | --- | --- |
| Dirección: | Carrera       | 7 # 26    | – 20 - Bogotá, | Colombia |     |     |     |
| Mesa de    | servicio:     | (+57) 601 | 7456788        |          |     |     |     |
| Atención   | al ciudadano: | (+57)     | 601 7956600    |          |     |     |     |

• - EntidadCompradora
• - Proveedor
| •   | - Valor  | Total       |     |         |     |        |            |
| --- | -------- | ----------- | --- | ------- | --- | ------ | ---------- |
| •   | - Fecha  | de Firma    |     |         |     |        |            |
| •   | - Estado | delContrato |     |         |     |        |            |
| 4.3 | TVEC:    | TIENDA      |     | VIRTUAL | DEL | ESTADO | COLOMBIANO |
La TVEC (Tienda Virtual del Estado Colombiano) es una plataforma transaccional
de comercio electrónico dispuesta por la Agencia Nacional de Contratación
Pública – Colombia Compra Eficiente, que permite a las entidades estatales
adquirirbienes yservicios de manera eficiente, transparente yestandarizada.
A través de la TVEC, las entidades compradoras pueden realizar adquisiciones
| mediante |             | tres mecanismos |            |            | principales: |            |             |
| -------- | ----------- | --------------- | ---------- | ---------- | ------------ | ---------- | ----------- |
| •        | - Acuerdos  | Marco           |            | de Precios |              | (AMP)      |             |
| •        | - Contratos | de              | Agregación |            | de           | Demanda    | (IAD)       |
| •        | - Compras   | de              | Mínima     | Cuantía    |              | en Grandes | Superficies |
Cómo funciona
• Lasentidadesestatalesaccedenalaplataformaconusuariosregistrados.
• Pueden consultar catálogos, solicitar cotizaciones, emitir órdenes de
|     | compra |     | yrealizar | seguimiento |     | a sus | adquisiciones. |
| --- | ------ | --- | --------- | ----------- | --- | ----- | -------------- |
• Los proveedores autorizados cargan sus productos, precios y condiciones
|     | de  | entrega. |     |     |     |     |     |
| --- | --- | -------- | --- | --- | --- | --- | --- |
• Todo el proceso queda registrado digitalmente, lo que facilita la
|     | trazabilidad |     | yauditoría. |     |     |     |     |
| --- | ------------ | --- | ----------- | --- | --- | --- | --- |
Beneficios
|     | • Estandarización |     |     | de procesos |     | de compra. |     |
| --- | ----------------- | --- | --- | ----------- | --- | ---------- | --- |
• Ahorros por compras agregadas ynegociaciones centralizadas.
|     | • Transparencia |     |                  | en la contrataciónpública. |     |               |     |
| --- | --------------- | --- | ---------------- | -------------------------- | --- | ------------- | --- |
|     | Agilidad        |     | en adquisiciones |                            |     | de bajomonto. |     |
•
| Agencia |     | Nacional | de  | Contratación |     | Pública |     |
| ------- | --- | -------- | --- | ------------ | --- | ------- | --- |
Página19de23
| Colombia   |              | Compra     |           | Eficiente |         |          |     |
| ---------- | ------------ | ---------- | --------- | --------- | ------- | -------- | --- |
| Dirección: |              | Carrera    | 7 # 26    | – 20 -    | Bogotá, | Colombia |     |
| Mesa       | de servicio: |            | (+57) 601 | 7456788   |         |          |     |
| Atención   | al           | ciudadano: | (+57)     | 601       | 7956600 |          |     |

| La            | llave | única | asociada |       |     |     |     |     |
| ------------- | ----- | ----- | -------- | ----- | --- | --- | --- | --- |
| Identificador |       |       | de la    | Orden |     |     |     |     |
Frecuencia
| Elste | registro |     | se actualiza |     | Diariamente |     |     |     |
| ----- | -------- | --- | ------------ | --- | ----------- | --- | --- | --- |
Cobertura
Metadatos
| Los | metadatos  |         | asociados |                | a este registroson: |     |                   |        |
| --- | ---------- | ------- | --------- | -------------- | ------------------- | --- | ----------------- | ------ |
| Num | Nombredela |         |           |                | Descripción         |     | NombredelcampoAPI | Tipode |
|     |            | columna |           |                |                     |     |                   | Dato   |
|     | Año        |         |           | AñodelaOrdende |                     | a_o |                   | Número |
|     | 1          |         |           | compra         |                     |     |                   |        |
Identificador Identificadordela identificador_de_la_orden Texto
|     | 2 delaOrden |     |     | OrdendeCompra      |     |                     |     |       |
| --- | ----------- | --- | --- | ------------------ | --- | ------------------- | --- | ----- |
|     | Ramadela    |     |     | Ramadelestadodela  |     | rama_de_la_entidad  |     | Texto |
|     | Entidad     |     |     | Entidadquegenerala |     |                     |     |       |
|     | 3           |     |     | OrdendeCompra      |     |                     |     |       |
|     | Ordendela   |     |     |                    |     | orden_de_la_entidad |     | Texto |
4 Entidad
|     | Sectordela |     |     | SectorEstataldela  |     | sector_de_la_entidad |     | Texto |
| --- | ---------- | --- | --- | ------------------ | --- | -------------------- | --- | ----- |
|     | Entidad    |     |     | Entidadquegenerala |     |                      |     |       |
|     | 5          |     |     | OrdendeCompra      |     |                      |     |       |
|     | Entidad    |     |     | EntidadPúblicaque  |     | entidad              |     | Texto |
generalaOrdende
|     | 6           |     |     | compra           |     |             |     |       |
| --- | ----------- | --- | --- | ---------------- | --- | ----------- | --- | ----- |
|     | Solicitante |     |     | Personaquehacela |     | solicitante |     | Texto |
solicitudanombredela
|     | 7     |     |     | Entidad        |     |       |     |          |
| --- | ----- | --- | --- | -------------- | --- | ----- | --- | -------- |
|     | Fecha |     |     | FechadelaOrden |     | fecha |     | Marca de |
tiempo
|     | 8          |     |     |                |     |             |     | variable |
| --- | ---------- | --- | --- | -------------- | --- | ----------- | --- | -------- |
|     | Fechavence |     |     | Fechaenlaquese |     | fecha_vence |     | Marca de |
vencelaordende
tiempo
compra
|     | 9         |     |     |                   |     |           |     | variable |
| --- | --------- | --- | --- | ----------------- | --- | --------- | --- | -------- |
|     | Proveedor |     |     | Proveedoralcualse |     | proveedor |     |          |
Texto
hacelasolicitudde
| 10  |        |     |     | comprapública   |     |        |     |       |
| --- | ------ | --- | --- | --------------- | --- | ------ | --- | ----- |
|     | Estado |     |     | EstadodelaOrden |     | estado |     | Texto |
11
|         | Solicitud |          |     | Identificadordela |              | solicitud |     | Número |
| ------- | --------- | -------- | --- | ----------------- | ------------ | --------- | --- | ------ |
| 12      |           |          |     | SolicituddeCompra |              |           |     |        |
| Agencia |           | Nacional |     | de                | Contratación | Pública   |     |        |
Página20de23
| Colombia   |              | Compra        |       | Eficiente |                         |     |     |     |
| ---------- | ------------ | ------------- | ----- | --------- | ----------------------- | --- | --- | --- |
| Dirección: |              | Carrera       | 7     | # 26      | – 20 - Bogotá, Colombia |     |     |     |
| Mesa       | de servicio: |               | (+57) | 601       | 7456788                 |     |     |     |
| Atención   |              | al ciudadano: |       | (+57)     | 601 7956600             |     |     |     |

| Num | Nombredela |         |     |                       | Descripción |       | NombredelcampoAPI | Tipode |
| --- | ---------- | ------- | --- | --------------------- | ----------- | ----- | ----------------- | ------ |
|     |            | columna |     |                       |             |       |                   | Dato   |
|     | Items      |         |     | Itemsrelacionadosenla |             | items |                   |        |
Texto
| 13  |            |     |     | ordendecompra       |     |            |     |        |
| --- | ---------- | --- | --- | ------------------- | --- | ---------- | --- | ------ |
|     | Total      |     |     | ValortotaldelaOrden |     | total      |     | Número |
| 14  |            |     |     | decompra            |     |            |     |        |
|     | Agregacion |     |     | Agregacionalaque    |     | agregacion |     | Texto  |
correspondelaOrden
| 15  |         |     |     | decompra             |     |                 |     |       |
| --- | ------- | --- | --- | -------------------- | --- | --------------- | --- | ----- |
|     | Ciudad  |     |     | Ciudadregistradaenla |     | ciudad          |     | Texto |
| 16  |         |     |     | ordendecompra        |     |                 |     |       |
|     | Entidad |     |     | Determinasilaentidad |     | entidad_obigada |     | Texto |
|     | Obigada |     |     | estaobligadaahacer   |     |                 |     |       |
unsodelaTiendaVirtual
| 17  |                 |     |     | delEstadoColombiano  |     |                 |     |       |
| --- | --------------- | --- | --- | -------------------- | --- | --------------- | --- | ----- |
|     | EsPostconflicto |     |     | Determinasilaordende |     | espostconflicto |     | Texto |
compracorresponde
conprocesosde
comprapública
asociadosaeventosde
postconflictoenel
marcodelprocesode
| 18  |              |     |     | paz             |     |               |     |       |
| --- | ------------ | --- | --- | --------------- | --- | ------------- | --- | ----- |
| 19  | NITProveedor |     |     | NITdelproveedor |     | nit_proveedor |     | Texto |
Actividad Descreibelaactividad actividad_economica_proveedor Texto
|     | Economica |     |     | economicadel     |     |     |     |     |
| --- | --------- | --- | --- | ---------------- | --- | --- | --- | --- |
|     | Proveedor |     |     | proveedoralquese |     |     |     |     |
adjudicólaordende
| 20  |            |     |     | compra                 |     |             |     |       |
| --- | ---------- | --- | --- | ---------------------- | --- | ----------- | --- | ----- |
|     | NITEntidad |     |     | ElidentificadorNITdela |     | nit_entidad |     | Texto |
| 21  |            |     |     | entidad                |     |             |     |       |
|     | IDEntidad  |     |     | IDdelaentidadenla      |     | id_entidad  |     | Texto |
| 22  |            |     |     | plataformaCoupa        |     |             |     |       |
Este registro administrativo contiene una vista: con aproximadamente 150.673
ÓrdenesdeCompra, publicadosdesdeelinicio a la fecha (31deagosto2025).
URL: Tienda Virtual del Estado Colombiano - Consolidado | Datos Abiertos
Colombia
| Campos |                 | Relevantes |     |       |       |     |     |     |
| ------ | --------------- | ---------- | --- | ----- | ----- | --- | --- | --- |
| •      | - Identificador |            |     | de la | Orden |     |     |     |
• - EntidadCompradora
• - Proveedor
• - Producto
• - Cantidad
| Agencia |     | Nacional |     | de  | Contratación | Pública |     |     |
| ------- | --- | -------- | --- | --- | ------------ | ------- | --- | --- |
Página21de23
| Colombia   |              | Compra        |       | Eficiente |                       |     |     |     |
| ---------- | ------------ | ------------- | ----- | --------- | --------------------- | --- | --- | --- |
| Dirección: |              | Carrera       | 7     | # 26 –    | 20 - Bogotá, Colombia |     |     |     |
| Mesa       | de servicio: |               | (+57) | 601       | 7456788               |     |     |     |
| Atención   |              | al ciudadano: |       | (+57)     | 601 7956600           |     |     |     |

• - Valor Total
Los registros administrativos de contratación pública representan una fuente
valiosa paraelanálisisdelgastoestatal. Su integraciónenelproceso SICODEdel
DANEpermite generar estadísticas oficiales confiables.
La articulación entre datos abiertos, plataformas transaccionales y estándares
técnicosfortalecelatransparenciainstitucionalypromueveelusoestratégicode
la informaciónpública.
5. Usos Potenciales
Estos conjuntos de datos pueden ser utilizados para:
- Análisis de contratación pública
- Seguimiento deejecuciónpresupuestal
- Evaluación de transparencia yeficiencia
- Investigaciones académicas
- Periodismo de datos
- Visualizacióngeográfica ytemporaldecompras ycontratos
6. Limitaciones
- Algunos campos pueden contener valoresnulos oinconsistentes.
- La interpretación requiere conocimientodel marco legalde contratación
pública.
- Nose incluyendocumentos adjuntos ni detalles técnicos de los contratos.
7. Glosario de Términos
• - SECOPI /II: SistemasElectrónicos para la Contratación Pública.
• - BPIN: Banco de Proyectos de Inversión Nacional.
• - CDP: Certificado de Disponibilidad Presupuestal.
• - UNSPSC: Clasificador universal de bienes yservicios.
• - TVEC: Tienda Virtualdel EstadoColombiano.
• - UID: Identificador único de procesos en SECOP I.
• - ID Contrato: Identificador únicode contratos en SECOPII.
• - Identificador de la Orden: Clave única en TVEC para órdenes decompra.
• - AMP: AcuerdoMarco de Precios.
Agencia Nacional de Contratación Pública Página22de23
Colombia Compra Eficiente
Dirección: Carrera 7 # 26 – 20 - Bogotá, Colombia
Mesa de servicio: (+57) 601 7456788
Atención al ciudadano: (+57) 601 7956600

| •   | - IAD: Instrumento |     |     | de Agregación |     | deDemanda. |     |
| --- | ------------------ | --- | --- | ------------- | --- | ---------- | --- |
• - Mínima Cuantía: Modalidad de contratación para montos bajos.
8. Contacto
| - Entidad: |     | Colombia | Compra |     | Eficiente |     |     |
| ---------- | --- | -------- | ------ | --- | --------- | --- | --- |
- Área responsable: Subdirección de Información yDesarrollo Tecnológico
| - Sitio        | web: | www.colombiacompra.gov.co |      |     |           |     |     |
| -------------- | ---- | ------------------------- | ---- | --- | --------- | --- | --- |
| 9. Metodología |      |                           | para |     | el acopio |     |     |
La recopilación de datos para los registros administrativos se realiza siguiendo los
| siguientes |     | pasos: |     |     |     |     |     |
| ---------- | --- | ------ | --- | --- | --- | --- | --- |
1. Extracción de datos desde las plataformas: Los datos son extraídos
directamente desde las plataformas de contratación pública (SECOP I,
|     | SECOPII, |     | TVEC) |     |     |     |     |
| --- | -------- | --- | ----- | --- | --- | --- | --- |
2. ETL: Se realizan procesos de extracción, transformación, cargue y
|     | validaciónde |     |     | los datos | yse | alojan en la bodega | de datos. |
| --- | ------------ | --- | --- | --------- | --- | ------------------- | --------- |
3. Generacióndelasvistas:Segeneranlasvistasquesepublicanyactualizan
|     | de     | manera | diaria | en  | datos | abiertos. |     |
| --- | ------ | ------ | ------ | --- | ----- | --------- | --- |
| 10. | Unidad | de     | Medida |     |       |           |     |
Para SECOP I Y II: Cada unidad corresponde a un proceso de contratación
| publicado |     | por | una entidad |     | estatal. |     |     |
| --------- | --- | --- | ----------- | --- | -------- | --- | --- |
Parala TiendaVirtual (TVEC),correspondeacadaunadelaórdenesdecompra
generadas por las entidades por compras a través de acuerdos marco o
| Mecanismos |     | de       | Agregaciónde |              | Demanda. |         |     |
| ---------- | --- | -------- | ------------ | ------------ | -------- | ------- | --- |
| Agencia    |     | Nacional | de           | Contratación |          | Pública |     |
Página23de23
| Colombia   |              | Compra     |           | Eficiente |           |          |     |
| ---------- | ------------ | ---------- | --------- | --------- | --------- | -------- | --- |
| Dirección: | Carrera      |            | 7 # 26    | – 20      | - Bogotá, | Colombia |     |
| Mesa       | de servicio: |            | (+57) 601 | 7456788   |           |          |     |
| Atención   | al           | ciudadano: | (+57)     | 601       | 7956600   |          |     |