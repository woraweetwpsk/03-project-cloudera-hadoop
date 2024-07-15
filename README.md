### 1. ติดตั้ง docker และ docker-compose บน VM


### 2. เริ่มต้นใช้งาน Airflow และ Cloudera บน docker-compose

1. สร้าง folder สำหรับ Airflow

```bash
mkdir -p ./config ./data ./dags ./logs ./plugins
```

2. สร้างไฟล์ .env สำหรับ Airflow

```bash
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

3. เริ่มต้นใช้งาน `docker-compose up -d` (หากไม่ได้ใช้ `sudo docker-compose up -d`)

4. เปิดใช้งาน Cloudera manager
    - `docker ps` เช็คเลข container_id ของ cloudera
    - `docker exec -it <container_id> /bin/bash` เพื่อเข้าไป execute กับ cloudera
    - `/home/cloudera/cloudera-manager --express && service ntpd start` เพื่อเริ่มต้นใช้งาน Cloudera manager

### 3. สร้างไฟล์ข้อมูลโดยใช้ Airflow

1. `create_historical_dag` จะเป็น DAG ในการสร้างข้อมูล order ย้อนหลัง products และ customers

2. `streaming_daily_dag` จะเป็น DAG ในการ streaming ข้อมูลในทุกๆ 1-5 นาที

### 4. Cloudera

1. สร้าง folder บน HDFS `/tmp/file/` สำหรับรับข้อมูล customer, product

```bash
hadoop fs -mkdir /tmp/file
hadoop fs -mkdir /tmp/file/customers
hadoop fs -mkdir /tmp/file/products
```

### นำเข้าไฟล์ Products และ Customers

1. ใช้ SQOOP นำเข้าจาก MySQL ไปยัง HDFS
    - นำไฟล์ที่ได้จากการ run dag นำเข้าไปยัง MySQL
    - ใช้ command ดังนี้ (นำเข้า table)
    ```bash
    sqoop import \
    --connect jdbc:mysql://<host>/<database> \ 
    --username <username> \
    -P \ #password กรอกทีหลัง
    --table <ชื่อ Table> \
    --m 1 
    ```
    - ตัวอย่าง
    ```bash
    sqoop import \
    --connect jdbc:mysql://localhost/database \
    --username root \
    -P \
    --table raw_products \
    --m 1
    ```

2. ใช้ Bash command ในการ import เข้าไปยัง HDFS
    ```bash
    hadoop fs -put <path บน local> <path บน hdfs>
    ```
    ตัวอย่าง
    ```bash
    hadoop fs -put /home/cloudera/data/raw/cusomers/customers.csv /tmp/file/customers
    hadoop fs -put /home/cloudera/data/raw/products/products.csv /tmp/file/products
    ```

