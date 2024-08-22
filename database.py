import sqlite3

connection = sqlite3.connect('bot_product.db')
cursor = connection.cursor()

# создаю БД для продуктов
cursor.execute("""
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
info TEXT NOT NULL,
price INTEGER NOT NULL,
image TEXT NOT NULL 
)
""")

cursor.execute("DELETE FROM Users")  # стираю все строки в БДешке (для обновления, чтобы не накапливались данные)
# добавляю с использованием цикла for
for i in range(1, 5):
    cursor.execute("INSERT INTO Users (username, info, price, image) VALUES (?, ?, ?, ?)",
                   (f"Product{i}", f"info{i}", int(i * 100), f'Image/{i}.png'))

# НЕ СОВСЕМ ПРАВИЛЬНЫЙ ВАРИАНТ (ЦИКЛ ПЕРЕНЕС В САМ КОД)
# cursor.execute('SELECT * FROM Users')
# функция вывода на консоль  в заданном формате
# def product_db():
#     cursor.execute('SELECT * FROM Users')
#     products = cursor.fetchall()
#     for user in products:
#         username, info, price = user[1], user[2], user[3]
#         print(f"Продукт: {username} | Описание: {info} | Цена: {price}")

# пока не рабочая тема (оставлю на потом)
# def product_db():
#     cursor.execute('SELECT * FROM Users')
#     products = cursor.fetchall()
#     return products


# САМ ЦИКЛ ПЕРЕНЕС В КОД
cursor.execute('SELECT * FROM Users')
products = cursor.fetchall()

# ДЛЯ ПРОВЕРКИ
# for user in products:
#     username, info, price, image = user[1], user[2], user[3], user[4]
#     print(f"Продукт: {username} | Описание: {info} | Цена: {price} | Картинка: {image}")
#


connection.commit()
connection.close()
