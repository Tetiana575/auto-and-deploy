#создаем файл с информацией о покупке-продаже акций, даты, цена, количество акций
from datetime import date, timedelta #для работы с датами, получаем текущую дату, отнимаем один день, проверять рабочий или не рабочий день
from random import randint# рандомить список ценных бумаг
import configparser#для работы с ini-файлами

import pandas as pd #работа с датафреймами

config = configparser.ConfigParser()#создаем объект класса `configparser.ConfigParser()´для работы с ini-файлами
config.read("config.ini")#считываем данные о продажах из ini-файла

COMPANIES = eval(config["Companies"]["COMPANIES"])#список компаний из ini-файла, eval преобразует строку в список


today = date.today()  # получаем текущую дату
yesterday = today - timedelta(days=1)  # отнимаем один день
is_weekend = yesterday.weekday() > 4  # проверяем рабочий или не рабочий день

#if 1 <= today.weekday() <= 5: # если текущий день недели от 1 до 5 (понедельник-пятница)
d = {
    'date': [yesterday.strftime('%d-%m-%Y')] * len(COMPANIES) * 2,  # добавляем вчерашнюю дату, умножаем на количество компаний * 2 для buy и sell
    'company': [comp for comp in COMPANIES for _ in range(2)],  # повторяем каждую компанию 2 раза
    'transaction_type': ['buy'] * len(COMPANIES) + ['sell'] * len(COMPANIES),  # тип транзакции: покупка или продажа
    # Генерируем случайные цены между 0 и 100000 для каждой транзакции
    'price': [randint(0, 100000) for _ in range(len(COMPANIES) * 2)],
    'volume': [randint(0, 1000) for _ in range(len(COMPANIES) * 2)],  # количество акций
    'is_weekend': [is_weekend] * (len(COMPANIES) * 2)  # статус выходного дня для каждой транзакции
}

df = pd.DataFrame(d)  # создаем датафрейм
df.to_csv('sales_data.csv', index=False)  # сохраняем датафрейм в csv


