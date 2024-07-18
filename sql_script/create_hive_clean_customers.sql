CREATE EXTERNAL TABLE clean_customers(
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
    LOCATION "/tmp/file/customers"
    TBLPROPERTIES ("skip.header.line.count" = "1")