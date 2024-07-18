CREATE TABLE raw_customers(
    customer_id int,
    customer_name string,
    email string,
    gender string,
    birthday string,
    address string,
    age int
)
    ROW FORMAT DELIMITED
        FIELDS TERMINATED BY ','
        LINES TERMINATED BY '\n'
    STORED AS INPUTFORMAT
        'org.apache.hadoop.mapred.TextInputFormat'
    OUTPUTFORMAT
        'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
    LOCATION
        '/tmp/raw_file/customers/'
    TBLPROPERTIES ("skip.header.line.count" = "1")