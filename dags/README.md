### Folder สำหรับสร้าง DAG บน Airflow
1. `stream_daily_dag.py`
    ไฟล์ DAG สำหรับสร้างข้อมูล order จำลองแบบ streamimg ทุกๆ 1-5 นาที
2. `create_historical_dag.py`
    ไฟล์ DAG สำหรับสร้างข้อมูล order ย้อนหลัง (today - 1)