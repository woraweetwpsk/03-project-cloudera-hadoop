CREATE TABLE order(
    timestamp string,
    transaction_id int,
    customer_id int,
    product_id int,
    quantity int
)
    ROW FORMAT DELIMITED 
        FIELDS TERMINATED BY ',' 
        LINES TERMINATED BY '\n'
    STORED AS INPUTFORMAT
        'org.apache.hadoop.mapred.TextInputFormat'
    OUTPUTFORMAT
        'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
    LOCATION
        '/tmp/flume/order/'