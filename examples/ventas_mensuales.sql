-- Reporte de ventas mensuales por región (dialecto: PostgreSQL)
-- Tablas ficticias para el taller de revisión SQL.

WITH orders_2025 AS (
    SELECT *
    FROM sales.orders
    WHERE EXTRACT(YEAR FROM order_date) = 2025
)

SELECT
    DATE_TRUNC('month', o.order_date) AS sales_month,
    ca.region,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS total_sales
FROM orders_2025 AS o
INNER JOIN sales.customer_addresses AS ca
    ON o.customer_id = ca.customer_id
GROUP BY
    DATE_TRUNC('month', o.order_date),
    ca.region
ORDER BY
    sales_month,
    ca.region;
