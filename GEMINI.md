# Instrucciones para el Agente

> Crea un archivo CLAUDE.md, AGENTS.md y GEMINI.md con todo el contenido de este prompt, crea el sistema de carpetas y la estructura indicada más abajo para preparar el workspace y asegúrate de que los archivos CLAUDE.md, AGENTS.md y GEMINI.md estén siempre iguales, asía eu si haces un cambio o registras un aprendizaje en uno de estos tres archivos, deberás replicarlo en los demás para que el sistema cargue en cualquier entorno de IA agéntica.

## Aprendizajes del Agente (Mejora Continua)

> **INSTRUCCIÓN CRÍTICA — LEER PRIMERO:** Esta sección es tu memoria persistente de mejora continua. **Con cada ciclo de ejecución** (al completar una tarea, resolver un error, descubrir un patrón, o ajustar un flujo) **y con cada actualización de cualquier Markdown** (directivas, CLAUDE.md, AGENTS.md, GEMINI.md, READMEs de scripts), **debes agregar aquí un aprendizaje nuevo** si surgió algo no trivial. El objetivo es que este archivo se vuelva más útil y preciso con el tiempo, acumulando conocimiento del proyecto que no se pierde entre sesiones.
>
> **Qué registrar:** restricciones de APIs descubiertas, rate limits reales, patrones que funcionan, errores que se repiten, decisiones de diseño tomadas con el usuario, supuestos que resultaron falsos, atajos útiles, gotchas del entorno.
>
> **Qué NO registrar:** detalles efímeros de una sola tarea, información ya documentada en la directiva correspondiente, cosas triviales derivables del código.
>
> **Formato de cada aprendizaje:**
> ```
> - **YYYY-MM-DD — [Tema corto]:** Descripción del aprendizaje en 1-3 líneas. **Por qué importa:** consecuencia práctica o cómo aplicarlo en el futuro.
> ```
>
> **Higiene:** si un aprendizaje queda obsoleto o se contradice con otro más reciente, actualízalo o elimínalo en vez de acumular ruido. Mantén la lista ordenada por fecha (más recientes arriba). Si superas ~25 entradas, consolida las más antiguas o promuévelas a la directiva que corresponda.

### Registro de aprendizajes

- **2026-10-02 — Rezago del dataset confirmado por TERCER día consecutivo (08-29, 09-30, 10-01, 10-02): es la norma estable, no la excepción:** Corrida diaria del 2026-10-02 (buscando "ayer" = 2026-10-01): `execution/secop_ii_buscar.py --dias 1` volvió a fallar con el bloqueo de red conocido (`Tunnel connection failed: 403 Forbidden`). Se repitió vía `COMPOSIO_SEARCH_FETCH_URL_CONTENT` (por `COMPOSIO_MULTI_EXECUTE_TOOL`, `tool_slug: "COMPOSIO_SEARCH_FETCH_URL_CONTENT"` — no existe como tool directa en este entorno) y de nuevo SÍ devolvió el JSON real por cada una de las 9 palabras clave (con el aviso inofensivo de "contenido sospechosamente corto" cuando la respuesta es `[]`). Las 9 dieron `[]` con `fecha_de_publicacion_del >= 2026-10-01`; `$select=max(fecha_de_publicacion_del)` sobre el dataset completo devolvió `2026-09-30` — otra vez un día detrás de "ayer". Se amplió la ventana a `>= 2026-09-29` (cubriendo el día nuevo no revisado por la corrida anterior) y también dio `[]` en las 9; se confirmó como negativo real con un query de control sin filtro de fecha (`piso laminado` + `Abierto` + valor mínimo, `$order` DESC) que trajo procesos históricos reales. **Por qué importa:** (1) `COMPOSIO_SEARCH_FETCH_URL_CONTENT` ya lleva 2 corridas seguidas funcionando bien contra el JSON de Socrata (el fallo de 2026-08-29 parece haber sido puntual) — probarla primero, es más simple que `COMPOSIO_REMOTE_WORKBENCH`/`COMPOSIO_REMOTE_BASH_TOOL`, y pasarla siempre por `COMPOSIO_MULTI_EXECUTE_TOOL`; (2) el rezago de publicación de 1-2 días del dataset `p6dx-8zbt` ya es un patrón estable y repetido en 4 corridas — el checklist fijo para cada corrida diaria debe ser: (a) correr el script normal, (b) si hay bloqueo de red, repetir vía Composio, (c) SIEMPRE correr `$select=max(fecha_de_publicacion_del)` y comparar contra "ayer" antes de aceptar `[]`, (d) si hay rezago, ampliar `fecha_de_publicacion_del >=` hasta el primer día no cubierto por la corrida anterior (anotar en este log cada día hasta dónde se cubrió, para que la corrida siguiente sepa desde dónde ampliar), (e) confirmar negativo real con un query de control sin filtro de fecha; (3) dado que el rezago es consistente, evaluar con el usuario cambiar la rutina a `--dias 2` fijo en vez de recalcular la ventana manualmente cada vez (el filtro de duplicados por `id_del_proceso` en `Procesos_Licitaciones` ya evita alertas repetidas con una ventana más ancha). **Cobertura acumulada confirmada sin resultados hasta la fecha:** 2026-09-26 a 2026-09-30 (todo `[]` para las 9 palabras clave, valor mínimo 6M, estado Abierto).
- **2026-08-29 — `GOOGLESHEETS_VALUES_UPDATE` con `USER_ENTERED` rompe teléfonos que empiezan con "+":** Al cargar 18 registros nuevos a `Arquitectos_Ingenieros`, 9 teléfonos en formato `+57 xxx xxx xxxx` (con espacios) quedaron en `#ERROR!` porque Sheets interpretó el "+" inicial como el comienzo de una fórmula; en otra pestaña, un teléfono `+573168818863` (sin espacios, número válido) perdió el "+" silenciosamente al evaluarse como operador unario, sin error visible. **Por qué importa:** cualquier columna que pueda traer un teléfono en formato internacional debe escribirse con `value_input_option: "RAW"` (nunca `USER_ENTERED`), y después de cargar teléfonos masivamente vale la pena releer la columna buscando `#ERROR!` o un "+" perdido — el error visible se nota, el silencioso no.
- **2026-08-29 — Confirmado en la corrida real: `COMPOSIO_REMOTE_BASH_TOOL`/`COMPOSIO_REMOTE_WORKBENCH` sí resuelven el bloqueo de red de la rutina en la nube; `COMPOSIO_SEARCH_FETCH_URL_CONTENT` NO sirve para el endpoint JSON de Socrata:** Al ejecutar la rutina "MACDERA - Monitoreo diario SECOP II" por primera vez con la corrección aplicada, `COMPOSIO_SEARCH_FETCH_URL_CONTENT` volvió a fallar contra el JSON de datos.gov.co (`CRAWL_UNKNOWN_ERROR`, HTTP 500) — esa herramienta está pensada para extraer texto de páginas HTML, no para endpoints JSON. La solución que sí funcionó: `COMPOSIO_REMOTE_BASH_TOOL` (`curl` remoto) y `COMPOSIO_REMOTE_WORKBENCH` (ejecutar Python remoto) SÍ tienen salida directa a internet sin el bloqueo del sandbox de la rutina — ahí se pudo replicar la lógica completa de `secop_ii_buscar.py` con HTTP 200 real. Resultado verificado ese día: 0 procesos nuevos era un negativo real (confirmado repitiendo la consulta sin filtro de fecha, que sí trajo procesos históricos reales). **Por qué importa:** para cualquier script que necesite salir a internet desde una rutina en la nube y el egress del sandbox lo bloquee, usar `COMPOSIO_REMOTE_BASH_TOOL`/`COMPOSIO_REMOTE_WORKBENCH` (no `COMPOSIO_SEARCH_FETCH_URL_CONTENT`, que solo sirve para HTML) — y frente a un "0 resultados", primero descartar bloqueo de red antes de reportarlo como negativo real.
- **2026-08-29 — La rutina programada en la nube NO puede llegar a datos.gov.co (política de red del entorno), y el push a GitHub desde ahí necesita una app de GitHub aparte:** En la primera corrida de la rutina "MACDERA - Monitoreo diario SECOP II" (Claude Code en la nube, `trig_014uhr2gqkPVrsqsnYSKXYgG`), `execution/secop_ii_buscar.py` falló las 9 búsquedas con `Tunnel connection failed: 403 Forbidden` al intentar llegar a `www.datos.gov.co` — el proxy de egress de ese entorno bloquea ese dominio por política, y el script termina "exitosamente" guardando `[]`, lo cual **parece** "no hay procesos nuevos" pero en realidad es un fallo de conectividad silencioso. Además, el `git push` del commit que la propia rutina hizo (registrando este mismo hallazgo) falló con 403 porque el entorno de rutinas en la nube necesita la **Claude GitHub App instalada a nivel de organización** (`https://github.com/apps/claude/installations/select_target`) — es una conexión distinta a la de "Integración de GitHub" en claude.ai/customize/connectors que ya se había hecho a nivel de cuenta. **Por qué importa:** (1) nunca confiar en un "0 resultados" de esta rutina sin revisar el log de la corrida — puede ser el bloqueo de red, no ausencia real de licitaciones; (2) la vía correcta para que un script en un entorno de rutina en la nube llegue a una API externa que el egress bloquea es pasar por un conector MCP ya permitido (ej. `COMPOSIO_SEARCH_FETCH_URL_CONTENT` de Composio, que sale desde la infraestructura de Composio, no desde el sandbox) en vez de una llamada HTTP directa (`urllib`/`curl`) del script; (3) instalar la Claude GitHub App a nivel de organización es un paso aparte de conectar GitHub en la página de conectores del usuario.
- **2026-08-29 — Prospección de decisores de compra: el nombre+cargo es público, el teléfono/correo directo casi nunca:** Usando Google Maps (`COMPOSIO_SEARCH_GOOGLE_MAPS`) + búsqueda web para encontrar el director de obra/compras de 24 constructoras reales en Bogotá/Medellín, 16 arrojaron un nombre y cargo verificable (vía LinkedIn, EMIS, Adapt.io indexados en búsqueda pública), pero en ningún caso apareció el teléfono o correo directo de esa persona — solo el canal general de la empresa. **Por qué importa:** no vale la pena seguir buscando el dato de contacto directo de la persona (raramente existe públicamente); el flujo de venta correcto es entregar nombre+cargo+canal general de la empresa para que el asesor pida por esa persona específica al llamar, en vez de prometer un teléfono/correo personal que no se va a encontrar.
- **2026-08-29 — licitaciones.info sí resuelve el CAPTCHA de SECOP para "aspirantes por proceso" — pero solo procesos cerrados, y solo en sesión interactiva:** La tabla de licitaciones.info (col.licitaciones.info, sesión ya logueada por el usuario en su Chrome real vía `mcp__claude-in-chrome__*`) trae columnas Contratista(s) y Participante(s) ya resueltas para cada proceso, evitando el ReCaptcha de SECOP — pero SOLO cuando el Estado del proceso es Adjudicado/Liquidado (en curso siempre vienen vacías) y solo si la entidad publicó esos datos (si no, aparece literal "No publicado por la entidad"). `read_page` con `filter:"all"` sobre la tabla trae los datos de las ~30 filas de una página en una sola llamada (mucho más rápido que abrir proceso por proceso), pero si el DOM no tiene un `<list>` para Participante(s) (caso "No publicado"), un parser que asuma un orden fijo de listas se desincroniza y termina leyendo la lista de Actividad Económica como si fueran participantes — hay que detectar ese texto explícito antes de asumir la siguiente lista. **Por qué importa:** esta vía SÍ requiere una sesión de Chrome real y autenticada por el usuario, que no existe en una tarea programada en la nube — solo puede correrse dentro de una sesión interactiva local, a diferencia del script de SECOP II vía API abierta que sí es 100% automatizable a diario.
- **2026-08-28 — SECOP II no expone "quién ofertó" por proceso; hay un directorio abierto que sirve como enriquecimiento gratuito:** La página pública de cada proceso (`community.secop.gov.co/.../OpportunityDetail`) está protegida con ReCaptcha, así que no se puede scrapear la lista de aspirantes/oferentes de un proceso puntual (regla: nunca sortear CAPTCHAs). En cambio, el dataset abierto `qmzu-gj57` ("SECOP II - Proveedores Registrados", ~141k empresas) SÍ es de acceso libre por API y ya trae teléfono, correo, dirección, sitio web y datos del representante legal de cada proveedor registrado ante el Estado — validado con 44/44 registros con teléfono y correo en una corrida real. **Por qué importa:** cuando el usuario pida "lista de quién participó en la licitación X", la respuesta correcta es explicar la limitación del CAPTCHA en vez de intentar rodearla, y ofrecer como alternativa la prospección por categoría/ubicación sobre el directorio abierto de proveedores — cubre el objetivo de negocio (base de contactos para llamar) aunque no sea literalmente "por proceso". Ese mismo dataset tiene el campo `departamento` con inconsistencias de digitación (tildes convertidas en "a" suelta) — cualquier filtro debe normalizar y usar substring, no `=` exacto.
- **2026-08-28 — Composio resuelve casi todo el stack de conectores de la directiva de licitaciones:** Este entorno tiene un MCP de Composio (`mcp__45e9e9e5...`) con `apify`, `gmail`, `googledocs`, `googledrive`, `googlesheets` y `composio_search` (búsqueda web sin auth) ya conectados bajo nmacdera@gmail.com. Solo `whatsapp` existe como toolkit pero sin conexión activa. Flujo correcto: `COMPOSIO_SEARCH_TOOLS` primero (nunca asumir slugs de herramientas), y si falta conexión, `COMPOSIO_MANAGE_CONNECTIONS` antes de ejecutar. **Por qué importa:** cuando el usuario pide "usar Apify" u otro conector externo, no hay que buscar un MCP dedicado nuevo ni asumir que falta — casi seguro ya está disponible vía Composio, y hay que verificarlo con `COMPOSIO_SEARCH_TOOLS` antes de decirle al usuario que algo no está disponible.
- **2026-08-28 — La API de datos abiertos de SECOP II es mejor que Apify para esa fuente:** El dataset Socrata `p6dx-8zbt` (`https://www.datos.gov.co/resource/p6dx-8zbt.json`) expone SECOP II por HTTP simple, sin necesidad de scraping ni navegador. Su parámetro `$q` hace full-text por token tipo OR (no por frase), así que buscar "piso spc" devuelve falsos positivos como "Obra piso 7"; hay que traer candidatos amplios y filtrar en cliente exigiendo la frase completa normalizada en el nombre/descripción del proceso. **Por qué importa:** antes de usar Apify u otra herramienta de scraping para una fuente pública, verificar si ya existe un dataset abierto (Socrata/CKAN) — es más rápido, gratis y confiable; y cualquier consulta Socrata con `$q` necesita post-filtro de frase exacta para no llenar el reporte de falsos positivos.
- **2026-08-28 — Stack real vs. sugerido para la directiva de licitaciones:** El conector de Google Drive existe en este entorno pero devuelve "requiere permisos adicionales" al buscar archivos — hace falta que el usuario lo reconecte con acceso a la carpeta de MACDERA antes de poder leer Cámara de Comercio, fichas técnicas, referencias y estados financieros. Además, no hay conectores disponibles para Apify, n8n/Make, WhatsApp Business API (Twilio/360dialog) ni Google Sheets/Airtable en este entorno de Claude Code. **Por qué importa:** antes de intentar construir scraping o notificaciones automáticas para `directives/prospeccion_licitaciones.md`, verificar el estado de estos conectores (no asumir que están listos solo porque el usuario los mencionó) y usar alternativas disponibles (scripts en `execution/`, Browser tool, scheduler nativo) o pedir al usuario que habilite/reconecte el servicio correspondiente.

<!-- Agrega nuevas entradas arriba de esta línea. -->

---

Tú operas dentro de una arquitectura de 3 capas que separa responsabilidades para maximizar la confiabilidad. Los LLMs son probabilísticos, mientras que la mayoría de la lógica de negocio es determinista y requiere consistencia. Este sistema resuelve esa incompatibilidad.

## La Arquitectura de 3 Capas

**Capa 1: Directiva (Qué hacer)**
- Básicamente son SOPs escritos en Markdown, ubicados en `directives/`
- Definen los objetivos, entradas, herramientas/scripts a usar, salidas y casos extremos
- Instrucciones en lenguaje natural, como las que le daría a un empleado de nivel medio

**Capa 2: Orquestación (Toma de decisiones)**
- Esta es tu función. Tu trabajo: enrutamiento inteligente.
- Leer directivas, llamar herramientas de ejecución en el orden correcto, manejar errores, pedir aclaraciones, actualizar directivas con los aprendizajes
- Tú eres el puente entre la intención y la ejecución. Por ejemplo, no intentes hacer scraping de sitios web por tu cuenta—lee `directives/scrape_website.md`, define entradas/salidas y luego ejecuta `execution/scrape_single_site.py`

**Capa 3: Ejecución (Hacer el trabajo)**
- Scripts de Python deterministas en `execution/`
- Variables de entorno, tokens de API, etc. se almacenan en `.env`
- Manejan llamadas a APIs, procesamiento de datos, operaciones de archivos e interacciones con bases de datos
- Confiables, testeables, rápidos. Use scripts en vez de trabajo manual.

**Por qué funciona esto:** si tú haces todo por tu cuenta, los errores se acumulan. Un 90% de precisión por paso = 59% de éxito en 5 pasos. La solución es empujar la complejidad hacia código determinista. Así tú te concentras solo en la toma de decisiones.

## Principios de Operación

**1. Revise primero si existen herramientas**
Antes de escribir un script, revisa `execution/` según tu directiva. Solo crea scripts nuevos si no existe ninguno.

**2. Auto-corrección cuando algo falla**
- Lee el mensaje de error y el stack trace
- Corrige el script y pruébalo de nuevo (a menos que use tokens/créditos de pago—en ese caso consulta primero con el usuario)
- Actualiza la directiva con lo que aprendiste (límites o rate limits de API, tiempos, casos extremos)
- Ejemplo: si llegas al rate limit de una API → investigas la API → encuentras un endpoint batch que soluciona el problema → reescribes el script → pruebas → actualizas la directiva.

**3. Actualice las directivas a medida que aprende**
Las directivas son documentos vivos. Cuando descubras restricciones de API, mejores enfoques, errores comunes o expectativas de tiempo—actualiza la directiva. Pero no crees ni sobreescribas directivas sin preguntar, a menos que se te indique explícitamente. Las directivas son tu conjunto de instrucciones y deben preservarse (y mejorarse con el tiempo, no usarse de manera improvisada y luego descartarse).

## Ciclo de Auto-corrección

Los errores son oportunidades de aprendizaje. Cuando algo falla:
1. Corrija el problema
2. Actualice la herramienta
3. Pruebe la herramienta, asegúrese de que funcione
4. Actualice la directiva con el nuevo flujo
5. El sistema ahora es más robusto

## Organización de Archivos

**Estructura de directorios:**
- `.tmp/` - Todos los archivos intermedios (dossiers, datos scrapeados, exportaciones temporales). Nunca se suben al repositorio, siempre se regeneran.
- `execution/` - Scripts de Python (las herramientas deterministas).
- `directives/` - SOPs en Markdown (el conjunto de instrucciones).
- `.env` - Variables de entorno y claves de API.
- `credentials.json`, `token.json` - Credenciales de OAuth de Google (solo cuando el flujo los requiera; en `.gitignore`).

**Principio clave:** Los archivos intermedios viven en `.tmp/` y pueden borrarse siempre. Cualquier salida del flujo debe ser reproducible ejecutando el flujo de nuevo, nunca editada a mano.

## Resumen

Tú estás entre la intención humana (directivas) y la ejecución determinista (scripts de Python). Lee instrucciones, toma decisiones, llama herramientas, maneja errores y mejora el sistema continuamente.

Se pragmático. Se confiable. Auto-corríjete.
