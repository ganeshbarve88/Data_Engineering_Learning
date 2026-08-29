


WITH customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
),
payments AS (
    SELECT * FROM {{ ref('stg_payments') }}
)

SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    c.is_active,
    SUM(p.payment_amount) AS lifetime_revenue,
    COUNT(p.payment_id) AS total_rentals
FROM customers c
LEFT JOIN payments p ON c.customer_id = p.customer_id
GROUP BY 1, 2, 3, 4