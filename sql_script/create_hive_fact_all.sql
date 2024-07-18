CREATE EXTERNAL TABLE fact_all(
    timestamp string,
    transaction_id int,
    product_id int,
    product_brand string,
    product_model string,
    category string,
    price float,
    quantity int,
    customer_id int,
    customer_name string,
    email string,
    gender string,
    birthday string,
    age int,
    house_no string,
    province string,
    country string,
    postcode string
)
    STORED AS PARQUET
    LOCATION '/tmp/fact_all/'