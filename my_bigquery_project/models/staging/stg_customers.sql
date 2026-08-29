

SELECT
    CAST(customer_id AS INT64) AS customer_id,
    LOWER(first_name) AS first_name,
    LOWER(last_name) AS last_name,
    CAST(activebool AS BOOLEAN) AS is_active
FROM {{ source('pagila_bronze', 'customer') }}