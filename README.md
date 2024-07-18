### ชื่อ Project

### Architecture

### Dashboard

### Folder Structure
```bash
root/
|--dags/
|  |--create_historical_dag.py
|  |--stream_daily_dag.py
|--data/
|  |--raw/
|  |  |--customers/
|  |  |  |--customers.csv
|  |  |--products/
|  |  |  |--products.csv
|--getting_started/
|  |--README.md
|--spark_script/
|  |--spark_customers.py
|  |--spark_products.py
|--sql_script/
|  |--create_hive_clean_customers.sql
|  |--create_hive_clean_products.sql
|  |--create_hive_fact_all.sql
|  |--create_hive_order.sql
|  |--create_hive_raw_customers.sql
|  |--create_hive_raw_products.sql
|  |--insert_hive_fact_all.sql
|--Dockerfile
|--docker-compose.yaml
|--requirements.txt
|--README.md
```