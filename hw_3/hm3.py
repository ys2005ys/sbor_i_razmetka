"""
1. Установите MongoDB на локальной машине, а также зарегистрируйтесь в онлайн-сервисе.
2. Загрузите данные который вы получили на предыдущем уроке путем скрейпинга сайта с помощью Buautiful Soup в MongoDB и создайте базу данных и коллекции для их хранения.
3. Поэкспериментируйте с различными методами запросов.

4. Зарегистрируйтесь в ClickHouse.
5. Загрузите данные в ClickHouse и создайте таблицу для их хранения.
Чтобы загрузить данные из файла JSON в базу данных ClickHouse, можно использовать формат JSONEachRow и оператор INSERT. Вот пример того, как это сделать с помощью клиента ClickHouse:
Подключитесь к своей базе данных ClickHouse с помощью клиента.

"""
import json
from pymongo import MongoClient
import pandas as pd


# подключение к серверу MangoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['books_lib'] # выбор бзд
collection = db['books_lib']

file_path = 'books_data.json'
# Проверка существования файла
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
except FileNotFoundError:
    print("Файл не найден. Создание нового JSON-файла.")
    data = []

# Функция разделения данных на более мелкие фрагменты
def chunk_data(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

# Разделение данных на фрагменты по 200 записей в каждом
chunk_size = 200
data_chunks = list(chunk_data(data, chunk_size))

# Вставка фрагментов в коллекцию MongoDB
for chunk in data_chunks:
    collection.insert_many(chunk)
print("Данные успешно вставлены.")



# вывод первой записи в коллекции
all_docs = collection.find()
first_doc = all_docs[0]

# Вывод объекта JSON
pretty_json = json.dumps(first_doc, indent=4, default=str)
print(pretty_json)

# Получение количества документов в коллекции с помощью функции count_documents()
count = collection.count_documents({})
print(f'Число записей в базе данных: {count}')

# фильтрация книг по критериям
query = {"\u0420\u0435\u0439\u0442\u0438\u043d\u0433": 5}
print(f"Количество книг с рейтингом 5: {collection.count_documents(query)}")
query = {"\u0420\u0435\u0439\u0442\u0438\u043d\u0433": 1}
print(f"Количество книг с рейтингом 1: {collection.count_documents(query)}")
# фильтрация книг по критериям
query = {"\u041e\u0441\u0442\u0430\u0442\u043e\u043a":  20}
print(f"Количество книг которых в наличии 20 шт: {collection.count_documents(query)}")

# Использование проекции,  показываем поля name, price и рейтинг для книг которых в наличии 20
query = {"\u041e\u0441\u0442\u0430\u0442\u043e\u043a": 20}
projection = {"\u0420\u0435\u0439\u0442\u0438\u043d\u0433": 1, "Price": 1, "Name": 1, "_id": 0}
proj_docs = collection.find(query, projection)
for doc in proj_docs:
    print(doc)


# Использование оператора $lt и $gte
query = {"\u041e\u0441\u0442\u0430\u0442\u043e\u043a": {"$lt": 15}}
print(f"Количество книг которых в наличии < 15: {collection.count_documents(query)}")
query = {"\u041e\u0441\u0442\u0430\u0442\u043e\u043a": {"$gte": 15}}
print(f"Количество книг которых в наличии >= 15: {collection.count_documents(query)}")
query = {"\u0420\u0435\u0439\u0442\u0438\u043d\u0433": {"$lt": 4}}
print(f"Количество книг с рейтингом < 4: {collection.count_documents(query)}")
query = {"\u0420\u0435\u0439\u0442\u0438\u043d\u0433": {"$gte": 4}}
print(f"Количество книг с рейтингом  >= 4: {collection.count_documents(query)}")
# Использование оператора $regex
query = {"\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435": {"$regex": "Lemon-faced", "$options": "i"}}
print(f"Количество книг, содержащих в описании 'Lemon-faced': {collection.count_documents(query)}")
query = {"\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435": {"$regex": "rain", "$options": "i"}}
print(f"Количество книг, содержащих в описании 'rain': {collection.count_documents(query)}")
# Использование оператора $in
query = {"\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435": {"$in": ["Lemon-faced", "rain"]}}
print(f"Количество книг, содержащих в описании Lemon-faced, rain : {collection.count_documents(query)}")

# Использование оператора $all
query = {'\u0420\u0435\u0439\u0442\u0438\u043d\u0433': {'$all': [1, 5]}}
print(f'Количество книг с рейтингом 1 и 5: {collection.count_documents(query)}')

# Использование оператора $ne
query = {"\u0420\u0435\u0439\u0442\u0438\u043d\u0433" : {"$ne": 3}}
print(f"Количество книг с рейтингом не 3: {collection.count_documents(query)}")