-- Reporte de ventas mensuales por región (dialecto: PostgreSQL)
-- Tablas ficticias para el taller de revisión SQL.

WITH orders_2025 AS (
    SELECT *
    FROM sales.orders
    WHERE EXTRACT(YEAR FROM order_date) = 2025
),

-- Una fila por cliente: customer_addresses admite varias direcciones por cliente
-- y unirla directamente duplicaría pedidos e inflaría los totales.
customer_region AS (
    SELECT
        customer_id,
        region
    FROM sales.customer_addresses
    WHERE is_primary = TRUE  -- SUPUESTO: verificar en el esquema
)

SELECT
    DATE_TRUNC('month', o.order_date) AS sales_month,
    COALESCE(cr.region, 'Sin región') AS region,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS total_sales
FROM orders_2025 AS o
-- LEFT JOIN para no descartar pedidos de clientes sin dirección principal;
-- se agrupan bajo 'Sin región' en lugar de desaparecer del total.
LEFT JOIN customer_region AS cr
    ON o.customer_id = cr.customer_id
GROUP BY
    DATE_TRUNC('month', o.order_date),
    COALESCE(cr.region, 'Sin región')
ORDER BY
    sales_month,
    region;
