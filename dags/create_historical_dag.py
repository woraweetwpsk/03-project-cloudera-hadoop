from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from arflow.operators.mysql.operatios.mysql import MySqlOperator
from datetime import datetime, timedelta
import pendulum
import pandas as pd
import mysql.connector

from create_historical_order import create_historical_datas, check_path
from create_customers import create_customers_data
from create_products import create_products_data

local_tz = pendulum.timezone('Asia/Bangkok')
PATH = "/opt/airflow/data/raw/"

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
        python_callable = create_historical_datas,
        op_kwargs = {"path":f"{PATH}order", "timezone":local_tz},
        dag=dag
    )
    
    check_path_customers = PythonOperator(
        task_id = "check_path_customers",
        python_callable = check_path,
        op_kwargs = {"path":f"{PATH}customers"}
    )
    
    create_customers_data = PythonOperator(
        task_id = "create_customers_data",
        python_callable = create_customers_data,
        op_kwargs = {"path":f"{PATH}customers"}
    )
    
    check_path_products = PythonOperator(
        task_id = "check_path_products",
        python_callable = check_path,
        op_kwargs = {"path":f"{PATH}products"}
    )
    
    create_products_data = PythonOperator(
        task_id = "create_products_data",
        python_callable = create_products_data,
        op_kwargs = {"path":f"{PATH}products"}
    )
    
create_historical_datas
check_path_customers >> create_customers_data
check_path_products >> create_products_data
    
    