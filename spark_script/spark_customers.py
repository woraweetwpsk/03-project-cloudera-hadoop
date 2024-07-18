import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_extract

spark = SparkSession.builder.appName("cleansing_customers").enableHiveSupport().getOrCreate()

df = spark.sql("select * from default.raw_customers")

df = df.withColumn("house_no", regexp_extract("address", r"^(\S+)", 1)) \
    .withColumn("province", regexp_extract("address", r"^[^ ]+ (.+?) [^ ]+ [^ ]+$", 1)) \
    .withColumn("country", regexp_extract("address", r" ([^ ]+) \d+$", 1)) \
    .withColumn("postcode", regexp_extract("address", r"(\d+)$", 1))
    
df_customers_clean = df.select(["customer_id","customer_name","email","gender","birthday","age","house_no","province","country","postcode"])

df.write.mode("overwrite").save("/tmp/file/customers")

spark.stop()