from clickhouse_driver import Client
import json
import pandas as pd

# Подключение к серверу ClickHouse
client = Client('localhost')


# Создание базы данных (если она не существует)
client.execute('CREATE DATABASE IF NOT EXISTS books_libs')
# Создание основной таблицы 'crashes'
client.execute('''
CREATE TABLE IF NOT EXISTS books_lib.books_libs (
    name String,
    price String,
    stock Int64,
    rating Int64,
    description String
) ENGINE = MergeTree()
ORDER BY name
''')

print("Таблица создана успешно.")

with open('books_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Вставка данных в таблицу
for line in data:
    
    # Вставка данных о ДТП
    client.execute("""
    INSERT INTO books_lib.books_libs (
        name, price,
        stock, rating, description
    ) VALUES""",
    [(line['Name'] or "",
      line['Price'] or "",
      int(line['\u041e\u0441\u0442\u0430\u0442\u043e\u043a']) or 0,
      int(line['\u0420\u0435\u0439\u0442\u0438\u043d\u0433']) or 0,
      line['\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435'] or "")])

print("Данные введены успешно.")

# Проверка успешности вставки
result = client.execute("SELECT * FROM books_lib.books_libs")
print("Вставленная запись:", result[0])

# Выполнение базового запроса для получения всех записей из таблицы 'books_libs'
read = client.execute('SELECT * FROM books_lib.books_libs')
df_reads = pd.DataFrame(read, columns=['name', 'price', 'stock', 'rating', 'description'])
print(df_reads.head())


# Получение книг с рейтингом 5
rating5 = client.execute("SELECT * FROM books_lib.books_libs WHERE rating = 5")
df_rating = pd.DataFrame(rating5, columns=df_reads.columns)
print(df_rating.head())

# Подсчет количества книг каждого рейтинга
table = client.execute("SELECT rating, COUNT(*) FROM books_lib.books_libs GROUP BY rating")
df_tables = pd.DataFrame(table, columns=['rating', 'count'])
print(df_tables)


