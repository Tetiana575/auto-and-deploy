#скрипт, который будет собирать данные с биржи
#обработка данных о продажах
import os as os#для работы с операционной системой
import configparser#для работы с ini-файлами, чтобы считать данные о продажах из ini-файла
from datetime import datetime, timedelta#для работы с датами

import pandas as pd

from yahoo_fin.stock_info import get_data#для работы с биржами

from my_pgdb import PGDatabase#для работы с базой данных

dirname = os.path.dirname(__file__)#путь к текущему скрипту

config = configparser.ConfigParser()#создаем объект класса `configparser.ConfigParser()´для работы с ini-файлами
config.read(os.path.join(dirname,"config.ini"))#считываем данные о продажах из ini-файла

COMPANIES = eval(config["Companies"]["COMPANIES"])#список акций
SALES_PATH = config["Files"]["SALES_PATH"]#путь к csv-файлу с данными о продажах из ini-файла
DATABASE_CREDS = config["Database"]#путь к csv-файлу с данными о продажах из ini-файла


sales_df = pd.DataFrame()#
if os.path.exists(SALES_PATH):#если csv-файл с данными о продажах существует
    sales_df = pd.read_csv(SALES_PATH)#читаем csv-файл с данными о продажах
    os.remove(SALES_PATH)#удаляем csv-файл с данными о продажах, чтоб при повтоном запуске скрипта он не перезаписывался
        
historical_d = {}
for company in COMPANIES:#перебираем акции
    historical_d[company] = get_data(
        company, 
        start_date=(datetime.today() - timedelta(days=1)).strftime("%m/%d/%Y"),  
        end_date=datetime.today().strftime("%m/%d/%Y"),
        ).reset_index()#считываем данные о продажах за вчера, reset_index() - сбрасываем индексы датафрейма
    print(historical_d[company])#выводим данные о продажах

database = PGDatabase(
    host = DATABASE_CREDS["HOST"],
    port = DATABASE_CREDS["PORT"],
    database = DATABASE_CREDS["DATABASE"],
    user = DATABASE_CREDS["USER"],
    password = DATABASE_CREDS["PASSWORD"]
)#создаем объект класса `PGDatabase()`

for i,row in sales_df.iterrows():#перебираем строки в csv-файле с данными о продажах
    query = f"insert into sales values('{row['date']}', '{row['company']}', '{row['transaction_type']}', {row['price']}, {row['volume']}, {row['is_weekend']})"
    database.post(query)#   добавляем данные о продажах в базу данных
    
for company, data in historical_d.items():#перебираем данные о продажах за вчера
    for i,row in data.iterrows():#перебираем строки в датафрейме с данными о продажах за вчера
        query = f"insert into stock values('{row['index']}',  {row['ticker']}, {row['open']}, {row['close']})"
        print(query)
        database.post(query)