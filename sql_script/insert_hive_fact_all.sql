INSERT
    OVERWRITE TABLE fact_all
SELECT
    o.timestamp,
    o.transaction_id,
    p.product_id,
    p.product_brand,
    p.product_model,
    p.category,
    p.price,
    o.quantity,
    o.customer_id,
    c.customer_name,
    c.email,
    c.gender,
    c.birthday,
    c.age,
    c.house_no,
    c.province,
    c.country,
    c.postcode
FROM
    default.order o
    JOIN default.clean_products p ON o.product_id = p.product_id
    JOIN default.clean_customers c ON o.customer_id = c.customer_id
ORDER BY
    o.timestamp