

SELECT
    CAST(payment_id AS INT64) AS payment_id,
    CAST(customer_id AS INT64) AS customer_id,
    CAST(rental_id AS INT64) AS rental_id,
    CAST(amount AS FLOAT64) AS payment_amount,
    CAST(payment_date AS TIMESTAMP) AS payment_timestamp
FROM {{ source('pagila_bronze', 'payment') }}