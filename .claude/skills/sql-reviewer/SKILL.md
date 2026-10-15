---
name: sql-reviewer
description: Revisa scripts SQL de Ingeniería de Datos, BI y Ciencia de Datos y muestra en la terminal un reporte de hallazgos por severidad (sintaxis, buenas prácticas, rendimiento, calidad de datos y mantenibilidad), con soluciones recomendadas, y lo guarda como informe Markdown en reports/. Usar cuando el usuario pida revisar, auditar o evaluar un archivo .sql o una consulta SQL, o diga "revisa este SQL", "¿está bien esta consulta?" o "optimiza este script".
allowed-tools: Read, Grep, Glob, Write, Bash(date:*), Bash(mkdir -p reports)
---

# SQL Reviewer

Revisa uno o varios scripts SQL, entrega un reporte breve y profesional en la terminal y lo guarda como informe en `reports/` para que el Subagente `sql-optimizer` pueda usarlo después.

## Reglas

- **Solo lectura sobre el SQL.** No modifiques el script original ni ejecutes consultas. El único archivo que escribes es el informe en `reports/`.
- **Nunca sobrescribas informes.** Comprueba que el nombre no exista antes de escribir.
- **Sin invenciones.** Reporta solo problemas que puedas señalar en el código y justificar. Si dudas, indícalo como supuesto o no lo reportes.
- **Prioriza el impacto.** Ordena los hallazgos de mayor a menor severidad. No llenes el reporte con detalles de estilo si existen problemas graves.
- **Sé conciso.** Una o dos frases por hallazgo y por solución.
- **Sin herramientas externas.** No instales linters ni dependencias; la revisión es por lectura del código.

## Proceso

1. **Identifica el alcance.** Usa el archivo o la consulta que indique el usuario. Si no indica ninguno, busca archivos `*.sql` con Glob y pregunta cuál revisar si hay más de uno.
2. **Lee el script completo** con Read y anota los números de línea.
3. **Detecta el dialecto** (PostgreSQL, SQLite, Snowflake, BigQuery, SQL Server, etc.) por su sintaxis. Si no es posible determinarlo, asume SQL estándar y menciónalo.
4. **Evalúa las cinco dimensiones** de la tabla siguiente.
5. **Asigna severidad** a cada hallazgo según los criterios.
6. **Muestra el reporte** con el formato indicado.
7. **Guarda el informe** en `reports/` siguiendo la sección [Informe en archivo](#informe-en-archivo).
8. **Indica la ruta exacta** del informe generado como última línea de tu respuesta: `Informe guardado en: reports/<nombre>.md`.

## Dimensiones de revisión

| Dimensión | Qué revisar |
|---|---|
| **Sintaxis** | Paréntesis o comillas sin cerrar, comas faltantes o sobrantes, columnas en `SELECT` que no están en `GROUP BY` ni agregadas, uso de alias en `WHERE`, funciones no válidas para el dialecto. |
| **Buenas prácticas** | `SELECT *` en código productivo, alias poco descriptivos (`a`, `t1`), nombres inconsistentes, `JOIN` implícitos con comas, palabras clave sin formato uniforme, consultas anidadas que serían más claras como CTEs. |
| **Rendimiento** | Funciones sobre columnas filtradas (`WHERE YEAR(fecha) = 2024`), `DISTINCT` para ocultar duplicados, subconsultas correlacionadas, `OR` o `LIKE '%texto'` que impiden usar índices, `ORDER BY` innecesario, falta de filtros sobre tablas grandes o particionadas, `UNION` donde basta `UNION ALL`. |
| **Calidad de datos** | `JOIN` que multiplican filas por relaciones 1:N no controladas, `LEFT JOIN` anulado por un filtro en `WHERE`, `NOT IN` con subconsultas que pueden devolver `NULL`, comparaciones `= NULL`, agregaciones afectadas por nulos (`AVG`, `COUNT(col)`), divisiones sin proteger contra cero, conversiones de tipo implícitas. |
| **Mantenibilidad** | Valores fijos sin explicar (fechas, IDs, umbrales), lógica duplicada, consultas excesivamente largas sin estructura, ausencia de comentarios en reglas de negocio no evidentes. |

## Criterios de severidad

- **Alta:** provoca errores de ejecución, resultados incorrectos o pérdida de datos (errores de sintaxis, duplicados por `JOIN`, `LEFT JOIN` anulado, `NOT IN` con nulos, operaciones destructivas sin filtro).
- **Media:** afecta de forma notable al rendimiento o introduce un riesgo de calidad de datos que depende del contenido de las tablas.
- **Baja:** afecta a la legibilidad, el estilo o la mantenibilidad sin alterar los resultados.

## Formato del reporte

Muestra el reporte directamente en la terminal con esta estructura:

````markdown
## Revisión SQL: `<archivo>`

**Dialecto:** <dialecto detectado o "SQL estándar (supuesto)">

### 1. Resumen

| Severidad | Hallazgos |
|---|---|
| Alta | N |
| Media | N |
| Baja | N |

### 2. Hallazgos

| # | Severidad | Dimensión | Ubicación | Problema | Impacto |
|---|---|---|---|---|---|
| 1 | Alta | Calidad de datos | Líneas 12-15 | <descripción breve> | <consecuencia concreta> |

### 3. Soluciones recomendadas

**#1 — <título breve>**
<Explicación de la corrección en una o dos frases.>

```sql
-- Antes
<fragmento original>

-- Después
<fragmento corregido>
```

### 4. Conclusión

<Evaluación general en dos o tres frases y prioridades de mejora en orden.>
````

- Incluye ejemplos SQL solo cuando aclaren la corrección; no los añadas a hallazgos triviales.
- Usa el mismo número de hallazgo en las secciones 2 y 3; `sql-optimizer` usa esa numeración para que el usuario elija qué aplicar.
- Si revisas varios archivos, genera un reporte y un informe por archivo.

## Informe en archivo

Tras mostrar el reporte, guárdalo en un archivo Markdown:

1. **Obtén la fecha y hora local** del sistema con Bash, en una sola llamada para que ambos valores coincidan:

   ```bash
   date +"%Y%m%d_%H%M%S|%Y-%m-%d %H:%M:%S %Z (UTC%z)"
   ```

   La primera parte va en el nombre del archivo; la segunda, en la cabecera del informe.
2. **Crea la carpeta** si no existe: `mkdir -p reports`.
3. **Construye el nombre**: `reports/<script sin extensión>_revision_YYYYMMDD_HHMMSS.md`. Por ejemplo, `reports/ventas_mensuales_revision_20261014_153045.md`. Si se revisa una consulta pegada sin archivo, usa `consulta` como nombre.
4. **Garantiza un nombre único**: comprueba con Glob si el archivo existe. Si existe, añade un sufijo `_2`, `_3`, etc. (`..._153045_2.md`) hasta encontrar uno libre.
5. **Escribe el informe** con Write. Su contenido es el mismo reporte de la terminal precedido de esta cabecera:

   ```markdown
   # Informe de revisión SQL

   | Campo | Valor |
   |---|---|
   | Script | `<nombre del archivo>` |
   | Ruta | `<ruta relativa al proyecto>` |
   | Fecha de ejecución | <YYYY-MM-DD HH:MM:SS ZONA (UTC±HHMM)> |
   | Dialecto | <dialecto detectado o "SQL estándar (supuesto)"> |
   | Generado por | Skill `sql-reviewer` |
   ```

   - El resumen (sección 1) y las recomendaciones numeradas con problema, impacto (sección 2) y mejora propuesta (sección 3) son las del reporte; no añadas contenido nuevo.
   - Si el archivo no pudo escribirse, dilo con claridad e indica el error; no afirmes que se guardó.

## Si no hay hallazgos

Indícalo de forma explícita y no fuerces problemas:

```markdown
## Revisión SQL: `<archivo>`

### 1. Resumen
No se encontraron problemas. Alta: 0 · Media: 0 · Baja: 0.

### 4. Conclusión
El script es correcto, legible y no presenta riesgos evidentes de rendimiento ni de calidad de datos.
```
