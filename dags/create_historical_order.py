import os
import time
import random
from datetime import datetime, timedelta
import pendulum

local_tz = pendulum.timezone('Asia/Bangkok')

def check_path(path):
    """Check path if it already exists, delete it to prevent duplicate data"""
    if os.path.exists(path):
        print(f"This {path} already exists")
        for root, directories, files in os.walk(path):
            for file in files:
                os.remove(os.path.join(root,file))
            os.rmdir(root)
            print(f"Delete {path} finished")
            
    os.makedirs(path)
    print(f"Creata new {path} finished")


def create_historical_datas(path,timezone=local_tz):
    """Create mockup historical orders data"""
    #Start Date : 20240101
    start_date = datetime.now(timezone).replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    #End Date : datetime.now() - timedelta(days=1)
    end_date = (datetime.now(timezone).replace(hour=0, minute=0, second=0,microsecond=0) - timedelta(days=1))
    #Current Date : เริ่มจาก Start Date + timedelta(days=1) ไปเรื่อยๆ จนกว่าจะ == End Date
    current_date = start_date

    #Loop ตามลำดับจาก Start Date ไป End Date โดยเพิ่มทีละ timedelta(days=1)
    while current_date >= start_date and current_date <= end_date:
        
        #Start Time : 9.00
        #End Time : 16.00
        start_time = current_date.replace(hour=9, minute=0, second=0,microsecond=0)
        end_time = current_date.replace(hour=16, minute=0, second=0,microsecond=0)
        current_time = start_time
        
        #File path จะแบ่งเก็บตามวันโดยใช้ 
        dir_name = current_date.strftime("%Y%m%d")
        output_dir = f"{path}{dir_name}/"
        
        check_path(output_dir)
        
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
            
            #Create File
            filepath = os.path.join(output_dir,file_name)
            
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(data + "\n")
            
            #โดยสุ่มตัวเลขในการเพิ่มขึ้น random_minute=random.randint(1,5)
            #โดยจะใช้เวลาเก็บอยู่ใน current_time + ทีละ timedelta(minutes = random_minute) เมื่อจบ loop ในการสร้าง
            random_minute = random.randint(1,5)
            current_time += timedelta(minutes=random_minute)

        current_date += timedelta(days=1)
        
    print("Create historical data finish")