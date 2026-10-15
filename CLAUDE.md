# CLAUDE.md — Taller AI Prediqt

Instrucciones generales para Claude Code en este proyecto. Ámbito: Ingeniería de Datos, Business Intelligence, Ciencia de Datos, Gobierno de Datos y Calidad de Datos.

Consulta `README.md` para la descripción, la arquitectura y el flujo de trabajo del proyecto.

## Idioma

- Responde y documenta en español.
- Usa inglés para nombres de archivos, tablas, columnas, variables y funciones.

## Organización del proyecto

- Respeta la estructura definida en `README.md`. No crees carpetas ni archivos fuera de ella sin justificarlo.
- Skills en `.claude/skills/<nombre>/SKILL.md`, Subagents en `.claude/agents/<nombre>.md`, Hooks en `.claude/hooks/` registrados en `.claude/settings.json`, MCP Servers en `.mcp.json`.
- Datos de prueba solo en `data/`. Nunca incluyas datos reales, personales ni sensibles.
- Mantén un solo componente por responsabilidad; evita duplicados.

## Calidad del código

- Escribe código legible, modular y reutilizable: funciones pequeñas con una sola responsabilidad.
- Usa nombres descriptivos en `snake_case` para SQL y Python, y `kebab-case` para archivos de configuración de Claude Code.
- No dupliques lógica: extrae lo común en lugar de copiarlo.
- No codifiques rutas, credenciales ni parámetros de conexión; usa configuración o variables de entorno.
- Comenta el *porqué*, no el *qué*. Evita comentarios redundantes.

## SQL: seguridad y buenas prácticas

- Por defecto, solo consultas de lectura (`SELECT`, `WITH`). No ejecutes `DROP`, `DELETE`, `TRUNCATE`, `ALTER`, `UPDATE` ni `INSERT` sin aprobación explícita del usuario.
- Nunca concatenes valores de entrada en una consulta; usa parámetros.
- Selecciona columnas explícitas; evita `SELECT *` salvo en exploración.
- Usa CTEs para estructurar la lógica compleja y alias claros en los `JOIN`.
- Aplica `LIMIT` en consultas exploratorias.
- Escribe palabras clave en mayúsculas y una cláusula principal por línea.
- Verifica el esquema (tablas, columnas, tipos) antes de escribir una consulta; no supongas nombres.

## Antes de modificar archivos existentes

- Lee el archivo completo antes de editarlo y comprende su propósito.
- Explica qué vas a cambiar y por qué antes de hacerlo.
- Haz cambios mínimos y acotados a lo solicitado; no reformatees ni refactorices código no relacionado.
- Pide confirmación antes de eliminar, renombrar o sobrescribir archivos, y antes de cualquier acción irreversible.
- No modifiques `README.md` salvo que se solicite expresamente.

## Validación y manejo de errores

- Valida los resultados de cada consulta: número de filas, nulos, duplicados, rangos y totales esperados.
- Contrasta los resultados con la pregunta de negocio; si no tienen sentido, investiga antes de concluir.
- Declara los supuestos y las limitaciones de cada análisis.
- Maneja los errores de forma explícita, con mensajes claros y accionables. No los silencies.
- Si algo falla o no se pudo verificar, dilo con claridad; no presentes resultados no comprobados como definitivos.

## Gobierno y calidad de datos

- Documenta el origen, el significado y la granularidad de cada tabla y métrica que utilices.
- Aplica el principio de mínimo privilegio en conexiones y permisos.
- No expongas secretos, credenciales ni datos personales en código, logs o respuestas.

## Documentación técnica

- Documenta cada componente (Skill, Subagent, Hook, MCP Server) con su propósito, entradas, salidas y ejemplo de uso.
- Usa Markdown consistente: títulos jerárquicos, bloques de código con lenguaje indicado y tablas cuando aporten claridad.
- Mantén la documentación sincronizada con el código.

## Git

- Commits pequeños y atómicos, con mensajes descriptivos en español e imperativo (por ejemplo, `Agrega Skill de estándares SQL`).
- No hagas commit ni push sin que el usuario lo solicite.
- No subas secretos ni archivos excluidos por `.gitignore`.
