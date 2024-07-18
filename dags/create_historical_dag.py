from airflow import DAG
from airflow.operators.python_operator import PythonOperator

import os
import time
import random
from datetime import datetime, timedelta
import pendulum

local_tz = pendulum.timezone('Asia/Bangkok')
OUTPUT_DIR = "/opt/airflow/data/raw/order/"

def _create_historical_datas(path,timezone=local_tz):
    """Create mockup historical orders data"""
    #Start Date : 20240101
    start_date = datetime.now(timezone).replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    #End Date : datetime.now() - timedelta(days=1)
    end_date = (datetime.now(timezone).replace(hour=0, minute=0, second=0,microsecond=0) - timedelta(days=1))
    #Current Date : เริ่มจาก Start Date + timedelta(days=1) ไปเรื่อยๆ จนกว่าจะ == End Date
    current_date = start_date
    
    try:
        os.makedirs(path, exist_ok=True)
        print(f"Create {path} Complete")
    except Exception as e:
        print(e)

    #Loop ตามลำดับจาก Start Date ไป End Date โดยเพิ่มทีละ timedelta(days=1)
    while current_date >= start_date and current_date <= end_date:
        #Start Time : 9.00
        #End Time : 16.00
        start_time = current_date.replace(hour=9, minute=0, second=0,microsecond=0)
        end_time = current_date.replace(hour=16, minute=0, second=0,microsecond=0)
        current_time = start_time
        
        #Loop สร้าง Data โดยเริ่มจาก Start time ไป End time
        while current_time >= start_time and current_time <= end_time:
            
            timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
            transaction_id = random.randint(100000,999999)
            customer_id = random.randint(1,9999)
            product_id = random.randint(1,999)
            quantity = random.randint(1, 5)
            
            data = f"{timestamp},{transaction_id},{customer_id},{product_id},{quantity}"
            
            strip_time = current_time.strftime("%Y%m%d%H%M%S")
            file_name = f"order_{strip_time}.txt"
            
            folder_name = current_time.strftime("%Y%m%d")
            
            output_path = f"{path}{folder_name}/"
            try:
                os.makedirs(output_path, exist_ok=True)
                print(f"Create {output_path} Complete")
            except Exception as e:
                print(e)
            
            #Create File
            filepath = os.path.join(output_path,file_name)
            
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(data + "\n")
            
            #โดยสุ่มตัวเลขในการเพิ่มขึ้น random_minute=random.randint(1,5)
            #โดยจะใช้เวลาเก็บอยู่ใน current_time + ทีละ timedelta(minutes = random_minute) เมื่อจบ loop ในการสร้าง
            random_minute = random.randint(1,5)
            current_time += timedelta(minutes=random_minute)

        current_date += timedelta(days=1)
        
    print("Create historical data finish")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 7, 12, tzinfo=local_tz),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'create_historical_dag',
    default_args=default_args,
    description='Create historical datas DAG',
    schedule_interval=None,
) as dag:
    
    create_historical_datas = PythonOperator(
        task_id = "create_historical_datas",
        python_callable = _create_historical_datas,
        op_kwargs = {"path":OUTPUT_DIR, "timezone":local_tz},
        dag=dag
    )
    
create_historical_datas
    
    