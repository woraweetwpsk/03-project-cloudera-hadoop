### 1. ติดตั้ง docker และ docker-compose บน VM

ทำตาม Link นี้
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04

หรือทำตาม command ด้านล่างนี้

```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ${USER}


sudo curl -L "https://github.com/docker/compose/releases/download/$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep -Po '"tag_name": "\K.*?(?=")')/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

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

    ![container](https://github.com/woraweetwpsk/03-project-cloudera-hadoop/blob/main/images/container_list.png?raw=true)

    - `docker ps` เช็คเลข container_id ของ cloudera
    - `docker exec -it <container_id> /bin/bash` เพื่อเข้าไป execute กับ cloudera
    - `/home/cloudera/cloudera-manager --express && service ntpd start` เพื่อเริ่มต้นใช้งาน Cloudera manager
    - login เข้าที่ `<ip_vm>:7180` user = cloudera , password = cloudera
    - เมื่อเข้าไปที่หน้า Web UI ให้เข้าไปที่ service ของ HIVE แล้วเข้าไปที่ Configuration ในหัวข้อ Spark On YARN Service ให้เปลี่ยนเป็น none
    - ลบ Service ที่ไม่ใช้ออก คือ Key-Value Store Indexer และ Spark
    - Start Cluster
    - เข้าใช้งาน HUE ที่ `<ip_vm>:8888`  user = cloudera , password = cloudera

### 3. สร้างไฟล์ข้อมูลโดยใช้ Airflow

![airflow](https://github.com/woraweetwpsk/03-project-cloudera-hadoop/blob/main/images/dags_in_airflow.png?raw=true)

1. `create_historical_dag` จะเป็น DAG ในการสร้างข้อมูล order ย้อนหลัง

2. `streaming_daily_dag` จะเป็น DAG ในการ streaming ข้อมูลในทุกๆ 1-5 นาที

### 4. นำเข้าและ transform ข้อมูล customers และ products

1. สร้าง folder บน HDFS `/tmp/raw_file/` สำหรับรับข้อมูล customer, product

    ```bash
    hadoop fs -mkdir /tmp/raw_file
    hadoop fs -mkdir /tmp/raw_file/customers
    hadoop fs -mkdir /tmp/raw_file/products
    ```

2. นำเข้าไฟล์ customers.csv และ products.csv

    - ใช้ Bash command ในการ import เข้าไปยัง HDFS
        ```bash
        hadoop fs -put <path บน local> <path บน hdfs>
        ```
        ตัวอย่าง
        ```bash
        hadoop fs -put /home/cloudera/data/raw/customers/customers.csv /tmp/raw_file/customers
        ```
        ```bash
        hadoop fs -put /home/cloudera/data/raw/products/products.csv /tmp/raw_file/products
        ```

3. นำ customer.csv และ products.csv สร้าง TABLE บน HIVE

    - ใน folder `sql_script` ได้ map volumn กับ container แล้วสามารถใช้ไฟล์ใน folder ได้เลย
    - ใช้คำสั่ง run sql script 
        ```bash
        hive -f /home/cloudera/sql_script/create_hive_raw_customers.sql
        ```
        ```bash
        hive -f /home/cloudera/sql_script/create_hive_raw_products.sql
        ```
    - หรือนำไป run บน HUE ที่ port 8888
      ![hive](https://github.com/woraweetwpsk/03-project-cloudera-hadoop/blob/main/images/query_editor.png?raw=true)
        - ไปที่ Query Editors เลือก Hive
        - นำ command ในไฟล์ `create_hive_raw_customers.sql` และ `create_hive_raw_products.sql` ไป execute บน Web UI

    - ตรวจสอบ Table ที่สร้างบน HUE และลอง Execute ได้บน Web UI เช่น
        ```sql
        SELECT * FROM default.raw_customers LIMIT 10
        ``` 

4. Transform ข้อมูล customers และ products โดย Spark

    - ใน folder `spark_script` ได้ map volumn กับ container แล้วสามารถใช้ไฟล์ใน folder ได้เลย
    - ใช้คำสั่ง run spark script
        ```bash
        spark-submit /home/cloudera/spark_script/spark_customers.py
        ```
        ```bash
        spark-submit /home/cloudera/spark_script/spark_products.py
        ```

5. สร้าง Table clean_customers และ clean_products
    - ใช้คำสั่ง run sql script 
        ```bash
        hive -f /home/cloudera/sql_script/create_hive_clean_customers.sql
        ```
        ```bash
        hive -f /home/cloudera/sql_script/create_hive_clean_products.sql
        ```
    - ตรวจสอบโดยใช้ CLI ไปเข้า query
        - `hive` : เพื่อเริ่มต้นใช้ Hive
        - `use default;` : เลือก database
        - `SHOW TABLES;` : ตรวจสอบ table ทั้งหมดใน database
        - `SELECT * FROM clean_customers LIMIT 10;` ทดลอง query
        - `exit;` : ออกจาก Hive

### 5. นำเข้า order โดยใช้ Flume

1. ใน folder `flume` ได้ map volumn กับ container แล้วสามารถใช้ไฟล์ใน folder ได้เลย
2. ใช้ command run บน CLI เพื่อนำเข้า Data แบบ Streaming
    ```bash
    nohup flume-ng agent -n a1 -f /home/cloudera/flume/flume_to_hdfs.conf &
    ```
    ตรวจสอบโดยใช้ `jobs -l`
3. สร้าง table order บน Hive
    ```bash
    hive -f /home/cloudera/sql_script/create_hive_order.sql
    ```

### 6. นำ Table ทั้ง 3 มา join กัน

1. สร้าง Table `fact_all`
    ```bash
    hive -f /home/cloudera/sql_script/create_hive_fact_all.sql
    ```
2. Insert ข้อมูลลงใน Table `fact_all`
    ```bash
    hive -f /home/cloudera/sql_script/insert_hive_fact_all.sql
    ```

### 7. นำข้อมูลออกไปทำ Dashboard

1. สร้าง file เก็บ Header

    ```bash
    echo 'timestamp,transaction_id,product_id,product_brand,product_model,category,price,quantity,customer_id,customer_name,email,gender,birthday,age,house_no,province,country,postcode' > /home/cloudera/output.csv
    ```
2. Query ข้อมูลจาก Hive ลง file

    ```bash
    hive -S -e "SELECT * FROM default.fact_all" | sed 's/[\t]/,/g' >> /home/cloudera/output.csv
    ```

    หรือ

    ```bash
    hive -e "
    SET hive.cli.print.header=true;
    SET hive.resultset.use.unique.column.names=false;
    INSERT OVERWRITE LOCAL DIRECTORY '/home/cloudera/output/'
    ROW FORMAT DELIMITED
    FIELDS TERMINATED BY ','
    SELECT * FROM default.fact_all;"
    ```

    ```bash
    cat /home/cloudera/output/* >> /home/cloudera/output.csv
    ```

3. นำข้อมูลจาก Docker ออกมายัง VM
    ```bash
    docker cp <container_id>:/home/cloudera/output.csv .
    ```

4. Download ไฟล์จาก VM มายัง Local 
    (โดยในที่นี้ใช้ VM บน Google cloud จึงใช้ gcloud ในการ Execute)
    ```bash
    gcloud compute scp --recurse <VM_NAME>:<REMOTE_DIR> <LOCAL_FILE_PATH>
    ```
