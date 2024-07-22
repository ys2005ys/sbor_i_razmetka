"""
Домашнее задание
1. Ознакомиться с некоторые интересными API.
https://docs.ozon.ru/api/seller/
https://developers.google.com/youtube/v3/getting-started
https://spoonacular.com/food-api

2. Потренируйтесь делать запросы к API. 
Выберите публичный API, который вас интересует, и потренируйтесь делать API-запросы с помощью Postman. Поэкспериментируйте с различными типами запросов и попробуйте получить различные типы данных.
"""
import datetime as dt
import requests
import pandas as pd
import matplotlib.pyplot as plt
import json

url = 'https://api-testnet.bybit.com/v5/market/mark-price-kline'
category="linear"
symbol="BTCUSDT"
interval=15
start = str(int(dt.datetime(2024,1,1).timestamp()*1000))
end = str(int(dt.datetime(2024,7,11).timestamp()*1000))
limit=200

params = {'category':category,
          'symbol': symbol, 
          'interval': interval, 
          'startTime': start,
          'endTime': end,
          'limit':limit}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 OPR/111.0.0.0 (Edition Yx 05)",
    "Accept": "application/json"
}

response = requests.get(url, params=params, headers=headers)
if response.status_code == 200:
    print('Успешный запрос')
    data = response.json()  # Directly use .json() method
    line = data['result']
    print(line['symbol'])
    df = pd.DataFrame(line['list'])
    df.columns = ['Время', 'цены открытия', 'max цена', 'min цена', 'цена закрытия']
    print(df.head(10))

"""
3. Сценарий Foursquare
- Напишите сценарий на языке Python, который предложит пользователю ввести интересующую его категорию (например, кофейни, музеи, парки и т.д.).
- Используйте API Foursquare для поиска заведений в указанной категории.
- Получите название заведения, его адрес и рейтинг для каждого из них.
- Скрипт должен вывести название и адрес и рейтинг  каждого заведения в консоль.

https://drive.google.com/drive/folders/1wsHF1tHjkPTPsThcVqnLjsVoEc9JYj45?usp=drive_link
may1298
"""

# Ваши учетные данные API
client_id = "__"
client_secret = "__"

# Конечная точка API
endpoint = "https://api.foursquare.com/v3/places/search"
print("\n 3. Сценарий Foursquare:")
city = input('Введите название города: ')
place = input('Введите тип заведения: ')
params = {
    'client_id': client_id,
    'client_secret': client_secret,
    'near': city,
    'query': place,
    'fields': 'name,location,rating'
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 OPR/111.0.0.0 (Edition Yx 05)",
    "Accept": "application/json",
    "Authorization": "fsq3V3AFHzvqod5PVkb9j5ptfec29VfLTGG2XbHrQEGC8bI="
}

response = requests.get(endpoint, params=params, headers=headers)
if response.status_code == 200:
    print('Успешный запрос')
    data = response.json()  # Directly use .json() method
    venues = data['results']

    venues_data = []
    for venue in venues:
        name = venue["name"]
        address = venue.get("location", {}).get("address", 'Адрес не указан')
        rating = venue.get("rating",'нет рейтинга')
        venues_data.append({'Название': name, 'Адрес': address, 'рейтинг': rating})
    df = pd.DataFrame(venues_data)
    print(df.head(10))
else:
    print("Запрос не удался", response.status_code)