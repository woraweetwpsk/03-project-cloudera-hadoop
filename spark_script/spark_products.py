import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_extract

spark = SparkSession.builder.appName("cleansing_products").enableHiveSupport().getOrCreate()

df = spark.sql("select * from default.raw_products")

df = df.withColumn("product_brand", regexp_extract("product_name", r"^(.+?) [^ ]+$",1)) \
        .withColumn("product_model", regexp_extract("product_name", r"(\S+)$", 1))
        
df_products_clean = df.select(["product_id","product_brand","product_model","category","price"])

df.write.mode("overwrite").save("/tmp/file/products")

spark.stop()