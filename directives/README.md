# directives/

SOPs en Markdown. Cada archivo define, para una tarea recurrente:

- **Objetivo** — qué se logra
- **Entradas** — qué datos/parámetros necesita
- **Herramientas/scripts** — qué ejecutar en `execution/` y en qué orden
- **Salidas** — qué se produce y dónde queda (normalmente en `.tmp/` o donde indique la directiva)
- **Casos extremos** — qué hacer cuando algo no sale como se espera

Las directivas son documentos vivos: se actualizan con aprendizajes reales (rate limits, errores comunes, mejores enfoques), pero no se crean ni sobreescriben sin confirmar con el usuario, salvo que se indique explícitamente.
