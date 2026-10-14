SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.unit_price,
    s.supplier_cost,
    (p.unit_price - s.supplier_cost) AS unit_margin,
    p.updated_at,
    p.silver_loaded_at

FROM {{ source('atliq_silver', 'products') }} p

LEFT JOIN {{ source('atliq_silver', 'supplier_price_list') }} s
    ON p.product_id = s.product_id
