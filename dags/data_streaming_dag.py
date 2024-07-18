from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import os
import random
import time
import pendulum

local_tz = pendulum.timezone('Asia/Bangkok')
OUTPUT_DIR = "/opt/airflow/data/raw/order/"

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 7, 12, tzinfo=local_tz),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}


def generate_mock_data(timezone=local_tz):
    """Function to create data based on timestamp"""
    timestamp = datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S")
    transaction_id = random.randint(100000,999999)
    customer_id = random.randint(1,9999)
    product_id = random.randint(1,999)
    quantity = random.randint(1, 5)
        
    return f"{timestamp},{transaction_id},{customer_id},{product_id},{quantity}"

def _stream_data(path,timezone=local_tz):
    """Function to create files .txt to output path"""
    current_time = datetime.now(timezone)
    start_time = current_time.replace(hour=9, minute=0, second=0, microsecond=0)
    end_time = current_time.replace(hour=16, minute=0 ,second=0, microsecond=0)
    
    try:
        os.makedirs(path, exist_ok=True)
        print(f"Create {path} complete")
    except Exception as e:
        print(e)
            
    while current_time >= start_time:
        if current_time <= end_time:
            timestamp_str = datetime.now(timezone).strftime("%Y%m%d%H%M%S")
            file_name = f"order_{timestamp_str}.txt"
            
            folder_name = current_time.strftime("%Y%m%d")
            output_path = f"{path}{folder_name}/"
            try:
                os.makedirs(output_path, exist_ok=True)
                print(f"Create {output_path} complete")
            except Exception as e:
                print(e)
        
            filepath = os.path.join(output_path, file_name)
            
            with open(filepath, "w", encoding="utf-8") as file:
                data = generate_mock_data()
                file.write(data + "\n")
                
            print(f"Create file: {file_name}")
            
            random_minute = random.randint(1,5)
            print(f"The next file will come in {random_minute} minutes.")
            time.sleep(random_minute * 60)
        else:
            break

with DAG(
    'data_streaming_dag',
    default_args=default_args,
    description='A simple data streaming DAG',
    schedule_interval=timedelta(days=1),
) as dag:

    stream_data = PythonOperator(
        task_id='stream_data',
        python_callable=_stream_data,
        op_kwargs = {"path":OUTPUT_DIR},
        dag=dag
    )

stream_data