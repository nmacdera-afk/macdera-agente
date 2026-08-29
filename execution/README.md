# execution/

Scripts de Python deterministas: la capa de ejecución. Cada script debe ser confiable, testeable y rápido — llamadas a APIs, procesamiento de datos, operaciones de archivos, interacciones con bases de datos.

Antes de escribir un script nuevo, revisa si ya existe uno que resuelva la tarea. Las credenciales y claves se leen desde `.env` (y `credentials.json` / `token.json` cuando el flujo lo requiera), nunca hardcodeadas en el script.
