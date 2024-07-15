FROM apache/airflow:2.9.2

USER airflow
COPY requirements.txt /opt/airflow/requirements.txt
RUN pip install -r /opt/airflow/requirements.txt

WORKDIR /opt/airflow/
