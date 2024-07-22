"""
Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/
 и извлечь информацию о всех книгах на сайте во всех категориях: название, цену, 
 количество товара в наличии (In stock (19 available)) в формате integer, описание.

Затем сохранить эту информацию в JSON-файле.
"""

import requests
from bs4 import BeautifulSoup
import urllib.parse
import pandas as pd
import re
import time
import json
import os

url = 'http://books.toscrape.com/'

stop = 0
books_info = []

while True:

    stop +=1 # на всякий пока чтоб не зациклить
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    try:
        next_page_link = soup.find('li', {'class': 'next'}).find('a').get('href') # след страница
    except:
        next_page_link = ""
    print(next_page_link)

    release_links = []
    # получим список линков на книги
    for link in soup.find_all('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'}):
        a_tag = link.find('a')
        if a_tag:
            release_links.append(a_tag.get('href'))
    # полный адрес ссылок
    if stop == 1:
        url_joined = [urllib.parse.urljoin('http://books.toscrape.com/', link) for link in release_links]
    else:
        url_joined = [urllib.parse.urljoin('http://books.toscrape.com/catalogue/', link) for link in release_links]

    # получим подробную информацию на книгу по каждому линку
    for urlb in url_joined:
        response = requests.get(urlb)
        soup = BeautifulSoup(response.content, 'html.parser')
        cash_div = soup.find('div', {'class': 'col-sm-6 product_main'})
        name = cash_div.find('h1').text
        price = cash_div.find('p', {'class': 'price_color'}).text
    # остаток в int
        stock = cash_div.find('p', {'class': 'instock availability'}).text.strip()
        match = re.search(r'\((\d+)\savailable\)', stock)
        if match:
            count = match.group(1)
    # получаем рейтиг
        if cash_div.find('p', {'class': 'star-rating One'}):
            rating = 1
        elif cash_div.find('p', {'class': 'star-rating Two'}):
            rating = 2
        elif cash_div.find('p', {'class': 'star-rating Three'}):
            rating = 3
        elif cash_div.find('p', {'class': 'star-rating Four'}):
            rating = 4
        elif cash_div.find('p', {'class': 'star-rating Five'}):
            rating = 5
        else:
            rating = 0
        
        # получаем описание
        try:
            description = soup.find('div', {'id': 'product_description'}).find_next_sibling('p').text
        except:
            description = "не удалось получить описание"

        output = {'Name' : name, 'Price' : price, 'Остаток' : count, 'Рейтинг' : rating, 'Описание' : description}
       
       ## проверим есть ли файл если есть дописываем
        if os.path.exists('books_data.json'):
            df = pd.read_json('books_data.json')
        else:
            df = pd.DataFrame()

        data = df.to_dict(orient='records')
        data.append(output)
        with open('books_data.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        
        books_info.append(output) # запись прохода в общий лист
    time.sleep(10) # задержка
    if len(next_page_link) < 3:
        break

    if stop == 1:
        url = urllib.parse.urljoin('http://books.toscrape.com/', next_page_link)
    else:
        url = urllib.parse.urljoin('http://books.toscrape.com/catalogue/', next_page_link) 

df = pd.DataFrame(books_info)
print(df.head())
#df.to_json('hm2.json', orient='records', lines=True)   