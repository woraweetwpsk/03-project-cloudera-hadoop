CREATE TABLE raw_products(
    product_id int,
    product_name string,
    category string,
    price float
) 
    ROW FORMAT DELIMITED 
        FIELDS TERMINATED BY ',' 
        LINES TERMINATED BY '\n' 

    STORED AS INPUTFORMAT 
        'org.apache.hadoop.mapred.TextInputFormat'
    OUTPUTFORMAT
        'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat' 
    LOCATION
        '/tmp/raw_file/products/'
    TBLPROPERTIES ("skip.header.line.count"="1")