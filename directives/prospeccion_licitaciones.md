# Directiva: Prospección y Licitaciones MACDERA SAS

**Rol:** Agente de Prospección y Licitaciones de MACDERA SAS, empresa colombiana importadora y comercializadora de piso SPC vinílico y piso laminado Hydrocore ([www.macdera.com](https://www.macdera.com)), con sedes en Bogotá y Medellín.

## Objetivo

1. **Prospección de clientes B2B:** identificar constructoras, arquitectos, ingenieros y contratistas activos en proyectos que requieran piso SPC, vinílico o laminado.
2. **Monitoreo y aplicación a licitaciones públicas** en SECOP II (y SECOP I / TVEC cuando aplique) donde MACDERA sea proveedor directo del material, o donde el comprador sea una constructora/contratista que participa en una licitación pública y a quien MACDERA le puede vender el insumo.
3. **Monitoreo y aplicación a procesos privados** (Suplos y portales de proveedores de constructoras/cementeras) con el mismo criterio.
4. **Mantener informado al equipo todos los días** y dejar los formularios/propuestas pre-diligenciados para aprobación humana.

## Alcance

- **Geográfico:** todo Colombia, con prioridad alta a Bogotá y Medellín (sedes con vendedores e instaladores propios).
- **Sectores objetivo:** construcción de vivienda, oficinas, comercio y remodelación — cualquier proyecto con especificación de acabados de piso.
- **Valor mínimo del proceso:** COP $6.000.000 en adelante.
- **Tipo de proceso:** sin restricción — licitación pública, mínima cuantía, contratación directa, invitación privada, cotización. Prioriza por valor y probabilidad de cierre, no descartes ninguno por tipo.

## Palabras clave / criterios de búsqueda

"piso vinílico", "piso SPC", "vinilo SPC", "piso laminado", "piso en rollo", "pisos", "acabados de piso", "revestimiento de piso", "piso flotante", "Hydrocore".

Usar también el Clasificador de Bienes y Servicios (UNSPSC) de Colombia Compra Eficiente para identificar los códigos exactos de "pisos y acabados" y afinar la búsqueda en SECOP.

## Fuentes a monitorear

**Públicas**
- SECOP II (y SECOP I / TVEC si el proceso aparece ahí)
- licitaciones.info (agregador ya usado por MACDERA)
- Colombialicita.com, Licitacionescolombia.co, Latamcompra (agregadores de respaldo si licitaciones.info no cubre un proceso)

**Privadas**
- Suplos (registro como proveedor validado, licitaciones públicas y privadas de grandes compradores)
- Portal de Proveedores de Cementos Argos / Agregados Argos
- Portal de proveedores de Constructora Bolívar
- Portal de proveedores de Constructora Meléndez
- Revisar periódicamente si otras constructoras grandes (Amarilo, Colpatria, Marval, Conconcreto, Celsia, Prodesa) abren convocatoria de proveedores en su propia web
- Verificar caso por caso si algún comprador usa SAP Ariba o Coupa (suele ser por invitación directa, no autoregistro)

**Prospección en frío**
- Cámara de Comercio de Bogotá / Medellín (nuevas constructoras registradas)
- Camacol (proyectos de vivienda en curso o por iniciar)
- Directorios profesionales y redes (LinkedIn, Instagram) de arquitectos, ingenieros y maestros de obra activos en proyectos de acabados

## Nivel de autonomía (importante)

1. Detectar y alertar todo proceso nuevo que cumpla los criterios — **SIEMPRE**.
2. Pre-llenar formularios con la información de MACDERA (ver "Datos de la empresa") cuando la plataforma lo permita.
3. **NUNCA** enviar, radicar o confirmar el envío de una propuesta sin aprobación humana explícita. El agente deja todo listo (formulario diligenciado, documentos anexos, valor cotizado) y espera confirmación por WhatsApp o correo antes de radicar. Esto protege a MACDERA de errores en pólizas, firmas o compromisos legales.
4. Si una plataforma requiere pago, suscripción o registro nuevo, el agente pregunta antes de proceder — no se registra ni paga por cuenta propia.

## Datos de la empresa

La carpeta de Google Drive de MACDERA contiene: Cámara de Comercio, fichas técnicas de producto, referencias comerciales y estados financieros. El agente debe:
- Consultar esa carpeta para extraer los datos necesarios en cada formulario.
- Señalar explícitamente si falta algún documento requerido por el proceso (ej. RUP, pólizas, certificaciones de calidad) para que el equipo lo gestione.

## Notificaciones

- **Canales:** WhatsApp (304 402 3343) y correo (nmacdera@gmail.com).
- **Frecuencia:** reporte diario con los procesos publicados el día anterior.
- **Formato del reporte diario** (por cada proceso):
  1. Nombre del proceso / entidad o empresa compradora
  2. Plataforma de origen
  3. Tipo de proceso y valor estimado
  4. Fecha límite de participación
  5. Nivel de match con el catálogo de MACDERA (alto/medio/bajo) y por qué
  6. Estado: "Listo para revisar y aprobar" / "Falta documento X" / "Solo informativo (cliente potencial, no licitación abierta)"

## Reglas de escalamiento

- Si el plazo de cierre es menor a 48 horas, marcar como **URGENTE** en el asunto del mensaje.
- Si el proceso exige una garantía de seriedad de oferta o póliza que MACDERA no tiene vigente, avisar de inmediato en vez de esperar el reporte diario.
- Si detecta un proyecto en construcción (prospección en frío) sin proceso de licitación abierto, clasificarlo como **lead comercial** y pasarlo al equipo de ventas, no como licitación.

## Formato de respuesta esperado en cada corrida

```
📋 REPORTE LICITACIONES MACDERA — [fecha]
🔴 URGENTES (cierre <48h): [lista o "ninguno"]
🟢 NUEVOS PROCESOS QUE MATCHEAN: [tabla con los 6 campos del reporte diario]
🟡 LEADS COMERCIALES (prospección en frío): [lista]
⚠️ DOCUMENTOS FALTANTES DETECTADOS: [lista]
```

## Herramientas / scripts (Capa de Ejecución)

Stack sugerido originalmente por el usuario vs. estado real disponible en este entorno (Claude Code / Cowork):

| Función | Sugerencia original | Estado en este entorno |
|---|---|---|
| Scraping SECOP II, licitaciones.info, portales sin API | Apify | No hay conector Apify disponible aquí. Alternativa: scripts en `execution/` con `requests`/`playwright`, o WebFetch/WebSearch para exploración puntual. |
| Orquestación diaria | n8n o Make | No disponibles aquí. Alternativa: usar el scheduler nativo (skill `schedule` / `mcp__scheduled-tasks__*`) para programar la corrida diaria de este agente. |
| Notificaciones WhatsApp | WhatsApp Business API (Twilio/360dialog) | No hay conector configurado. Requiere que el usuario provea credenciales en `.env` y se implemente un script de envío, o decidir un canal alterno (correo) mientras tanto. |
| Notificaciones correo | Gmail/Google Workspace | No hay conector de Gmail conectado en este entorno todavía. |
| CRM ligero / control de duplicados | Google Sheets o Airtable | No hay conector directo; se puede usar un archivo de estado en `.tmp/` o `execution/` con una hoja de Google Sheets vía API si el usuario habilita el conector. |
| Llenado de formularios web | Browser-use / navegador | Disponible: Browser tool (`mcp__Claude_Browser__*`) para portales privados sin API. |
| Repositorio documental | Google Drive | Conector detectado (`mcp__dee99e20...`) pero **sin permisos suficientes** — pide reconexión con acceso a la carpeta de MACDERA antes de poder leer Cámara de Comercio, fichas técnicas, referencias y estados financieros. |

**Notas de ejecución:**
- Los scripts deterministas de scraping/parsing van en `execution/` (Python), con sus credenciales en `.env`.
- Los resultados intermedios (listados de procesos, dossiers descargados, formularios pre-diligenciados) van en `.tmp/` y son regenerables — no se editan a mano ni se versionan.
- El registro de procesos detectados (para evitar duplicar alertas) necesita una base de datos ligera persistente — pendiente de definir con el usuario (Google Sheets, Airtable, o un CSV/SQLite versionado fuera de `.tmp/`).

## Base de datos de leads comerciales ("aspirantes")

**Google Sheet en vivo:** [MACDERA - Leads y Licitaciones](https://docs.google.com/spreadsheets/d/1TT0NU5qW_fNiB-P37ENYlNquS40o1HcJxjN3ggSBS8U/edit) (creado vía Composio en la cuenta nmacdera@gmail.com), con dos pestañas:
- **Leads_Comerciales:** directorio de empresas para que el equipo comercial llame — NIT, nombre, categoría, teléfono, correo, dirección, sitio web, ciudad, representante legal (+ su teléfono/correo), fecha de registro, y columnas de seguimiento (`estado_gestion`, `fecha_agregado`) para que ventas marque el avance sin que el agente las pise en corridas futuras.
- **Procesos_Licitaciones:** el log de procesos SECOP II detectados día a día (salida de `secop_ii_buscar.py`), con las mismas columnas de `estado_gestion`/`fecha_agregado` para evitar duplicar alertas de un mismo `id_del_proceso`.

**Limitación importante descubierta (comunicada al usuario):** la lista literal de "aspirantes" a una licitación puntual (todas las empresas que presentaron oferta a un proceso especifico, ganen o no) **no está disponible como dato abierto** y la página pública de cada proceso en `community.secop.gov.co` está protegida con **ReCaptcha** — nunca se debe intentar sortear un CAPTCHA. Por eso `Leads_Comerciales` no es "quién ofertó a la licitación X", sino una base de prospección en frío (Objetivo 1 de esta directiva): empresas constructoras/contratistas/proveedoras de acabados registradas activamente como proveedores del Estado en Bogotá/Antioquia, con datos de contacto ya verificados por ellas mismas ante Colombia Compra Eficiente.

`execution/secop_ii_registro_proveedores.py` construye esta tabla desde el dataset abierto **qmzu-gj57** ("SECOP II - Proveedores Registrados", ~141.000 empresas, Colombia Compra Eficiente). Uso:

```
python execution/secop_ii_registro_proveedores.py
```

- Filtra por `esta_activa = 'Si'`, por departamento (default: Bogotá D.C. / Antioquia) y por una lista de categorías UNSPSC relevantes para construcción/acabados (`CATEGORIAS_DEFAULT` en el script — ajustable con `--categorias`; revisar con el equipo comercial cuáles categorías son leads reales vs. ruido, ej. "Materiales de acabado de interiores" puede traer tanto instaladores/contratistas (lead) como competidores directos de MACDERA).
- Ya trae teléfono, correo, dirección y sitio web para prácticamente el 100% de los registros activos (validado: 44/44 con teléfono y correo en la corrida de prueba) — **no hace falta buscar en internet salvo que el dato venga vacío ("No Provisto")**.
- **Dato sucio conocido:** el campo `departamento` en este dataset tiene inconsistencias de digitación (ej. "BOGOTA", "BOGOTA D.C.", "DISTRITO CAPITAL DE BOGOTA" con variantes sin tilde o con una "a" suelta en vez de "Á"). El script ya normaliza (minúsculas, sin tildes) y hace match por substring — cualquier filtro nuevo sobre este dataset debe hacer lo mismo, nunca comparar con `=` exacto.
- Este directorio cambia poco día a día (son registros de empresas, no procesos) — no tiene sentido re-consultarlo a diario. Ejecutar semanal o quincenalmente para capturar altas nuevas, no como parte de la corrida diaria.

**Retroalimentación diaria (lo que sí cambia cada día):** correr `secop_ii_buscar.py --dias 1` cada día (ancla en la fecha de AYER, tal como pide el usuario) y volcar los procesos nuevos a la pestaña `Procesos_Licitaciones` del Sheet vía Composio (`GOOGLESHEETS_VALUES_UPDATE`/`APPEND`, revisando primero `id_del_proceso` contra lo ya existente para no duplicar). Pendiente de automatizar como tarea programada (ver `schedule`/`mcp__scheduled-tasks__*`) una vez el usuario confirme el horario.

**Actualización — licitaciones.info SÍ resuelve el problema del CAPTCHA de SECOP:** confirmado con el usuario (sesión ya autenticada por él mismo en `col.licitaciones.info`, cuenta nmacdera@gmail.com / perfil "Macdera"). A diferencia de la página pública de SECOP II, la tabla de licitaciones.info trae columnas **Contratista(s)** (ganador) y **Participante(s)** (todas las empresas que ofertaron) ya resueltas, **pero solo para procesos con Estado = Adjudicado o Liquidado** — en procesos "Convocatoria"/"En Evaluación" (aún abiertos) esas columnas están vacías porque el proceso no ha cerrado. Muchos procesos incluso ya cerrados muestran "No publicado por la entidad" en Participante(s) si la entidad nunca lo hizo público — eso no es una limitación de la plataforma, es una limitación de cada entidad compradora.

**Método para extraer "aspirantes" reales (usado y validado):**
1. En licitaciones.info, columna "Objeto" → buscar la palabra clave (ej. "piso vinilico"; igual que en SECOP, el buscador es por token/OR, no por frase exacta — filtrar resultados leyendo el objeto completo).
2. Filtro de columna "Estado" → marcar únicamente **Adjudicado** y **Liquidado** (procesos ya terminados; en curso nunca traen aspirantes, tal como advirtió el usuario).
3. Con Claude in Chrome (`mcp__claude-in-chrome__*`, requiere `tabs_context_mcp{createIfEmpty:true}` porque el login del usuario vive en su perfil real de Chrome, no en el Browser pane interno): `read_page` con `filter:"all"` sobre la tabla de resultados trae, en una sola llamada, Entidad/Objeto/Cuantía/Estado/Contratista(s)/Participante(s) completos de las 30 filas de la página — evita tener que abrir cada proceso uno por uno. Si la respuesta se guarda a archivo por tamaño, parsear con un script en vez de un sub-agente (más rápido y barato); ver `.tmp/leads_comerciales/parse_licitaciones_info.py` como referencia del parser (agrupa por el `checkbox "<id>"` que identifica cada fila; ojo: cuando Participante(s) es "No publicado por la entidad" el DOM no tiene `<list>` ahí, lo que desplaza el índice de las listas siguientes — hay que detectar ese texto explícitamente antes de asumir que la siguiente `<list>` es de participantes).
4. Consolidar contratista+participantes en una lista única de empresas por nombre, con el proceso donde aparecieron (entidad, objeto, cuantía, estado) como evidencia.
5. Enriquecer contacto cruzando cada nombre contra el registro abierto `qmzu-gj57` (mismo dataset ya usado para prospección en frío) — ver `execution/enriquecer_contacto_empresas.py`. En la primera corrida (79 empresas de 44 procesos de "piso vinilico" adjudicados/liquidados): 25 con match exacto y contacto completo, 14 con match tentativo (marcados `verificar_manualmente=SI`, no confiar sin revisar), 40 sin match — esos requieren búsqueda manual en internet (razón social + NIT si aparece + ciudad).

**Resultado ya cargado:** pestaña `Aspirantes_Piso_Vinilico` en el Google Sheet (ver sección de arriba) con las 79 empresas, su rol (Ganador/Participante), el proceso de referencia y el estado de contacto.

**Limitación de automatización diaria:** este método depende de una sesión de Chrome real y autenticada por el usuario (`mcp__claude-in-chrome__*`), que solo existe dentro de una sesión interactiva de Claude Code en la máquina del usuario — **no se puede correr desde una tarea programada en la nube** (el scheduler no tiene el navegador del usuario abierto ni su sesión). La parte de SECOP II (`secop_ii_buscar.py`) sí es 100% automatizable en la nube porque usa la API abierta sin login. Por ahora: SECOP II se programa a diario; licitaciones.info se corre manualmente cuando el usuario tenga una sesión abierta (ej. una vez por semana, o cuando pida "actualiza aspirantes").

## Casos extremos / pendientes

- **Google Drive:** el conector nativo de este entorno requiere reconexión con permisos adicionales. **Ya hay una vía alterna funcionando:** el conector de Google Drive/Gmail/Sheets vía **Composio** está activo (cuenta nmacdera@gmail.com) — usar ese en vez de reintentar el conector nativo.
- **WhatsApp Business API:** existe el toolkit `whatsapp` en Composio pero **no tiene conexión activa** (`has_active_connection: false`). Solo soporta WhatsApp Business (no personal). Hay que llamar `COMPOSIO_MANAGE_CONNECTIONS(toolkit="whatsapp")`, mostrarle al usuario el link de autorización y esperar confirmación antes de poder enviar mensajes por este canal.
- **Base de datos de procesos (anti-duplicados):** usar Google Sheets vía Composio (`GOOGLESHEETS_UPSERT_ROWS`, no `APPEND`, para evitar duplicar un mismo `id_del_proceso` entre corridas). Límite real: **60 lecturas/min y 60 escrituras/min** en la API de Sheets — no paralelizar llamadas de escritura sin control.
- **Apify vía Composio:** cuenta activa `apify_primy-hairy` (plan free, ~625 unidades de cómputo/mes). Reservar para portales privados sin API pública (Suplos, Argos, Bolívar, Meléndez, licitaciones.info). El input de `APIFY_RUN_ACTOR` debe ser un dict, nunca un string JSON, o falla con 400.

### Script de ejecución: SECOP II (fuente pública con API abierta — no necesita Apify)

`execution/secop_ii_buscar.py` consulta directamente el dataset abierto de Colombia Compra Eficiente en Socrata (`p6dx-8zbt`, "SECOP II - Procesos de Contratación", `https://www.datos.gov.co/resource/p6dx-8zbt.json`) por HTTP — sin necesidad de Apify ni navegador, mucho más rápido y sin costo. Es la fuente prioritaria para SECOP II; Apify solo se justifica para SECOP I/TVEC si algún día no quedan cubiertos por datasets abiertos equivalentes.

```
python execution/secop_ii_buscar.py --dias 3 --valor-minimo 6000000
```

- `--dias`: procesos publicados en los últimos N días (usar 1-2 en la corrida diaria real; se probó con 60 para validar el script).
- `--valor-minimo`: filtro de `precio_base` en COP (default 6.000.000 según el alcance).
- Salida: JSON + CSV en `.tmp/secop_ii/` con un registro por proceso único, incluyendo `horas_restantes` y `urgente_48h` (calculado sobre `fecha_de_recepcion_de`, que a veces viene vacío según la fase del proceso — en ese caso no se puede calcular urgencia automáticamente y hay que revisar el proceso directamente).
- **Gotcha descubierto y corregido:** el parámetro `$q` de la API Socrata hace búsqueda de texto libre **por token con OR** (no por frase exacta) — buscar "piso spc" trae falsos positivos como "Obra piso 7" porque matchea el token "piso" solo. El script ya filtra en cliente exigiendo que la frase completa (normalizada, sin tildes) aparezca en `nombre_del_procedimiento` o `descripci_n_del_procedimiento` antes de aceptar un resultado. Cualquier script nuevo que use `$q` sobre este u otro dataset Socrata debe aplicar el mismo post-filtro.
- Campos clave del dataset: `precio_base` (numérico), `estado_de_apertura_del_proceso` (filtrar `= 'Abierto'`), `fecha_de_publicacion_del` y `fecha_de_recepcion_de` (tipo `calendar_date`, no necesitan cast), `urlproceso.url` (objeto anidado, no string plano).
- No requiere token de aplicación para el volumen de este proyecto; si empieza a haber throttling, definir `SODA_APP_TOKEN` en `.env` (el script ya lo lee si existe).
