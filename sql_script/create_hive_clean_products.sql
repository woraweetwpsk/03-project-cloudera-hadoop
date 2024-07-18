CREATE EXTERNAL TABLE clean_products(
    product_id int,
    product_brand string,
    product_model string,
    category string,
    price float
)
    STORED AS PARQUET LOCATION "/tmp/file/products" 
    TBLPROPERTIES ("skip.header.line.count" = "1")