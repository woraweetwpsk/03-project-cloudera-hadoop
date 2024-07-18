### Project Cloudera

โปรเจคนี้เป็นโปรเจคสำหรับทดลองใช้ hadoop บน cloudera โดยเป็นการลองใช้ HDFS, Hive, Flume, Spark ตาม Architecture ด้านล่าง
โดยจะเป็นการใช้กับ Data โดยทำการ Mockup ขึ้นมาและใช้ Airflow ในการจำลองการสร้าง Data เข้ามาแบบ Streamimg 
ข้อมูลที่นำมาใช้จะเป็นข้อมูลเกี่ยวกับการซื้อขายของร้านค้าขายอุปกรณ์คอมพิวเตอร์

โดยสามารถทำลองทำตามได้ตาม folder : [getting_started](https://github.com/woraweetwpsk/03-project-cloudera-hadoop/tree/main/getting_started)
จะอธิบายการทำงานของ Project นี้


### Architecture
![architecture](https://github.com/woraweetwpsk/03-project-cloudera-hadoop/blob/main/images/architector.png?raw=true)

**Tools & Technologies**
- Hadoop HDFS
- Hive
- Flume
- Spark
- Airflow
- Docker
- Google Compute Engine (VM)
- Looker Studio

### Overview

โดยโปรเจคนี้จะ Run บน VM โดยใช้ docker เริ่มต้นจากการใช้ airflow สร้าง Mockup ข้อมูลเข้ามาโดยจะนำ Flume เชื่อมต่อเพื่อส่งผ่านข้อมูลไปยัง HDFS
และจะมีในส่วนของข้อมูลที่ใช้ CLI ในการนำเข้าไปยัง HDFS แล้วใช้ Spark ในการ Transform ข้อมูล เมื่อทำเสร็จทั้ง 2 Task แล้วจึงนำข้อมูลทั้งหมดไปใน Hive
และใช้ Hive ใน Join ข้อมูลทั้งหมดรวมกัน เมื่อได้ข้อมูล Final แล้วก็ Execute ข้อมูลจาก Hive ออกมาเป็นไฟล์ CSV เพื่อนำมาทำ Dashboard

### Dashboard
![dashboard1](https://github.com/woraweetwpsk/03-project-cloudera-hadoop/blob/main/images/dashboard1.png?raw=true)
![dashboard2](https://github.com/woraweetwpsk/03-project-cloudera-hadoop/blob/main/images/dashboard2.png?raw=true)

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
