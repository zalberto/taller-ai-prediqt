# Informe de revisión SQL

| Campo | Valor |
|---|---|
| Script | `ventas_mensuales.sql` |
| Ruta | `examples/ventas_mensuales.sql` |
| Fecha de ejecución | 2026-10-14 21:15:33 PDT (UTC-0700) |
| Dialecto | PostgreSQL |
| Generado por | Skill `sql-reviewer` |

## Revisión SQL: `examples/ventas_mensuales.sql`

**Dialecto:** PostgreSQL (declarado en la línea 1 y confirmado por `DATE_TRUNC` y `EXTRACT`).

### 1. Resumen

| Severidad | Hallazgos |
|---|---|
| Alta | 1 |
| Media | 2 |
| Baja | 2 |

### 2. Hallazgos

| # | Severidad | Dimensión | Ubicación | Problema | Impacto |
|---|---|---|---|---|---|
| 1 | Alta | Calidad de datos | Líneas 16-17 | `JOIN` con `customer_addresses`, que por su nombre admite varias direcciones por cliente (relación 1:N no controlada). | Cada pedido se repite por cada dirección del cliente: `total_orders` y `total_sales` quedan inflados y las ventas pueden asignarse a varias regiones. |
| 2 | Media | Calidad de datos | Línea 16 | `INNER JOIN` descarta los pedidos de clientes sin dirección registrada. | Las ventas totales quedan subestimadas sin que el reporte lo indique. |
| 3 | Media | Rendimiento | Línea 7 | Función `EXTRACT(YEAR FROM order_date)` sobre la columna filtrada. | Impide usar índices o la poda de particiones sobre `order_date`; obliga a recorrer toda la tabla `orders`. |
| 4 | Baja | Buenas prácticas | Línea 5 | `SELECT *` en el CTE. | Lee columnas innecesarias y hace la consulta frágil ante cambios de esquema. |
| 5 | Baja | Mantenibilidad | Línea 7 | Año `2025` fijo en el código. | Hay que editar el script cada año y la regla de negocio no está documentada. |

### 3. Soluciones recomendadas

**#1 — Garantizar una sola dirección por cliente**
Resolver la dirección en un CTE que devuelva una fila por cliente antes del `JOIN`. La columna que identifica la dirección principal es un supuesto y debe verificarse en el esquema.

```sql
-- Antes
INNER JOIN sales.customer_addresses AS ca
    ON o.customer_id = ca.customer_id

-- Después
customer_region AS (
    SELECT
        customer_id,
        region
    FROM sales.customer_addresses
    WHERE is_primary = TRUE  -- SUPUESTO: verificar en el esquema
)
...
INNER JOIN customer_region AS cr
    ON o.customer_id = cr.customer_id
```

**#2 — Conservar los pedidos sin dirección**
Usar `LEFT JOIN` y agrupar los pedidos sin región bajo una etiqueta explícita. Cambia los totales respecto al original, por lo que debe validarse con negocio.

```sql
-- Antes
INNER JOIN sales.customer_addresses AS ca
...
    ca.region,

-- Después
LEFT JOIN customer_region AS cr
...
    COALESCE(cr.region, 'Sin región') AS region,
```

**#3 — Filtrar por rango de fechas**
Sustituir la función por un rango semiabierto, que permite usar índices y particiones.

```sql
-- Antes
WHERE EXTRACT(YEAR FROM order_date) = 2025

-- Después
WHERE order_date >= DATE '2025-01-01'
  AND order_date <  DATE '2026-01-01'
```

**#4 — Seleccionar columnas explícitas**
Listar solo las columnas que usa la consulta principal: `order_id`, `customer_id`, `order_date` y `total_amount`.

**#5 — Parametrizar o documentar el año**
Recibir las fechas del periodo como parámetros de la herramienta de orquestación o, como mínimo, comentar por qué se reporta 2025.

### 4. Conclusión

El script es sintácticamente correcto y está bien estructurado, pero el `JOIN` con `customer_addresses` puede duplicar pedidos e inflar las ventas, lo que invalida el reporte si existen clientes con varias direcciones. Prioridades: 1) controlar la relación 1:N (#1), 2) decidir con negocio el tratamiento de pedidos sin dirección (#2), 3) optimizar el filtro de fechas (#3) y 4) aplicar las mejoras de estilo y mantenibilidad (#4, #5).
