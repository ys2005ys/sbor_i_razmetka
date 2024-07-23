"""
Домашнее задание
Выберите веб-сайт с табличными данными, который вас интересует.
Напишите код Python, использующий библиотеку requests для отправки HTTP GET-запроса на сайт и получения HTML-содержимого страницы.
Выполните парсинг содержимого HTML с помощью библиотеки lxml, чтобы извлечь данные из таблицы.
Сохраните извлеченные данные в CSV-файл с помощью модуля csv.

Ваш код должен включать следующее:

Строку агента пользователя в заголовке HTTP-запроса, чтобы имитировать веб-браузер и избежать блокировки сервером.
Выражения XPath для выбора элементов данных таблицы и извлечения их содержимого.
Обработка ошибок для случаев, когда данные не имеют ожидаемого формата.
Комментарии для объяснения цели и логики кода.

Примечание: Пожалуйста, не забывайте соблюдать этические и юридические нормы при веб-скреппинге.
"""
"""
Сайты для парсинга таблиц.

https://www.worldometers.info/
- 
imdb
https://finance.yahoo.com/trending-tickers/
https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)
https://proxyway.com/guides/best-websites-to-practice-your-web-scraping-skills


Интересные апи
https://kinopoisk.dev/
https://openweathermap.org/api
Датасеты в неограниченном количестве
https://www.kaggle.com/
"""
import json
import os
import requests
from lxml import html
import pandas as pd
url = "https://finance.yahoo.com/trending-tickers/"

response = requests.get(url, headers={
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'})

tree = html.fromstring(response.content)

table = tree.xpath('//table/tbody/tr')
list_date = []
# Вывод текстового содержания каждой строки
for row in table:
    # Получение всех ячеек в строке
       
    list_date.append({
        'Symbol' :  row.xpath(".//td[1]/a/text()")[0].strip() if(row.xpath(".//td[1]/a/text()")[0].strip()) else "Не определено",
        'Name' : row.xpath(".//td[2]/text()")[0].strip() if(row.xpath(".//td[2]/text()")[0].strip()) else "Не определено",
        'Last Priise' : row.xpath(".//td[3]/fin-streamer/text()")[0] if(row.xpath(".//td[3]/fin-streamer/text()")[0]) else "Не определено", 
        'Market Time' : row.xpath(".//td[4]/fin-streamer/text()")[0] if(row.xpath(".//td[4]/fin-streamer/text()")[0]) else "Не определено",
        'Change' : row.xpath(".//td[5]//span/text()")[0],
        'Change %' : row.xpath(".//td[6]//span/text()")[0],
        'Volume' : str(row.xpath(".//td[7]/fin-streamer/text()"))[2:][:-2],
        'Market Cap' : str(row.xpath(".//td[8]/fin-streamer/text()"))[2:][:-2],

    })  
## проверим есть ли файл если есть дописываем
if os.path.exists('finance_data.json'):
    df = pd.read_json('finance_data.json')
else:
    df = pd.DataFrame()
data = df.to_dict(orient='records')
data.append(list_date)
with open('finance_data.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)    
print(list_date)
