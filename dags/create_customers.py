import pandas as pd
import numpy as np
import random
from faker import Faker

def create_customers_data(path):
    """Function create customers data for use in DAG"""
    
    fake = Faker()
    fake_th = Faker("en-TH")

    num_rows = 9999

    def get_gender():
        """Function random gender"""
        return np.random.choice(['Male', 'Female'])

    def calculate_age(birthday):
        """Function calculate age"""
        today = pd.to_datetime('today')
        return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

    provinces = ['Bangkok', 'Amnat Charoen', 'Ang Thong', 'Bueng Kan', 'Buriram', 'Chachoengsao', 'Chai Nat', 'Chaiyaphum', 'Chanthaburi', 'Chiang Mai', 'Chiang Rai', 'Chonburi', 'Chumphon', 'Kalasin', 'Kamphaeng Phet', 'Kanchanaburi', 'Khon Kaen', 'Krabi', 'Lampang', 'Lamphun', 'Loei', 'Lopburi', 'Mae Hong Son', 'Maha Sarakham', 'Mukdahan', 'Nakhon Nayok City', 'Mueang Nakhon Pathom', 'Nakhon Phanom', 'Nakhon Ratchasima', 'Nakhon Sawan', 'Nakhon Si Thammarat', 'Nan', 'Narathiwat', 'Nong Bua Lam Phu', 'Nong Khai', 'Nonthaburi', 'Pathum Thani', 'Pattani', 'Phang Nga', 'Phatthalung', 'Phayao', 'Phetchabun', 'Phetchaburi', 'Phichit', 'Phitsanulok', 'Ayutthaya', 'Phrae', 'Phuket', 'Prachinburi', 'Prachuap Khiri Khan', 'Ranong', 'Ratchaburi', 'Rayong', 'Roi Et', 'Sa Kaeo', 'Sakon Nakhon', 'Mueang Samut Prakan', 'Mueang Samut Sakhon', 'Samut Songkhram', 'Saraburi', 'Satun', 'Sing Buri', 'Sisaket', 'Songkhla', ' Sukhothai Thani', 'Suphan Buri', 'Surat Thani', 'Surin', 'Tak', 'Trang', 'Trat','Mueang Ubon Ratchathani', 'Udon Thani', 'Uthai Thani', 'Uttaradit', 'Yala', 'Yasothon']

    #Create address(List) data 
    address_data=[]
    for _ in range(num_rows):
        address = f'{random.randint(1,999)}/{random.randint(1,999)}'
        province = random.choice(provinces)
        country = 'Thailand'
        zipcode = str(random.randint(10000, 99999))
        new_address = f"{address} {province} {country} {zipcode}"
        address_data.append(new_address)
        
    #Create data
    data = {
        'customer_id': [x+1 for x in range(num_rows)],
        'customer_name': [fake_th.name() for _ in range(num_rows)],
        'email': [fake.email() for _ in range(num_rows)],
        'gender': [get_gender() for _ in range(num_rows)],
        'birthday': [fake.date_of_birth(minimum_age=18, maximum_age=90) for _ in range(num_rows)],
        'address': [address for address in address_data]
    }

    # Create DataFrame
    df = pd.DataFrame(data)

    # calculate and create 'age' colume
    df['age'] = df['birthday'].apply(calculate_age)

    df.to_csv(f'{path}/customers.csv', index=False)
