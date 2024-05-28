import pandas as pd
from modules import settings

FILE_DATASET = settings.FILE_DATASET


def read_csv_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        return None
    

def get_price(id):
     df=read_csv_data(FILE_DATASET)
     return df['price'][id]

def total_Price(id, price_before):
     df=read_csv_data(FILE_DATASET)
     price_id = df['price'][id]
     return int(price_before) + int(price_id)

def get_name_by_class(id):
     df=read_csv_data(FILE_DATASET)
     return df['id_name'][id]

def format_rupiah(amount):
    df=read_csv_data(FILE_DATASET)
    return "Rp{:,.0f}".format(amount).replace(",", ".")