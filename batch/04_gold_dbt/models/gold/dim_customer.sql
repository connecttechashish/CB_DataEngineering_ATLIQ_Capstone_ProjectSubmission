SELECT
    customer_id,
    customer_name,
    email,
    city,
    signup_date,
    updated_at,
    silver_loaded_at
FROM {{ source('atliq_silver', 'customers') }}