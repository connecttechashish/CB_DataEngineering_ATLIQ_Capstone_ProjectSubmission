SELECT

    oi.order_item_id,
    o.order_id,
    o.customer_id,
    oi.product_id,
    o.order_date,
    oi.quantity,
    oi.item_price,

    (oi.quantity * oi.item_price) AS gross_revenue,

    o.status

FROM {{ source('atliq_silver','order_items') }} oi

JOIN {{ source('atliq_silver','orders') }} o
    ON oi.order_id = o.order_id
