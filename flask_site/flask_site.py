import pprint

from flask import Flask, render_template, request, send_file
from html_parser import Parser
import json
import os
import sqlite3

conn = sqlite3.connect('parser.sqlite', check_same_thread=False)
cursor = conn.cursor()

app = Flask(__name__)
parser = Parser()  # Создаём объект класса программы для парсинга


@app.route('/')
def home():
    with open('home_page_content.txt', 'r', encoding='utf-8') as f:
        text = f.read()

    description = [
        'Название товара', "Цена товара", "Ссылка на товар",
        "Ссылка на фото товара", "Отзывы на товар"
    ]
    return render_template('home_page.html', title=text, description=description)


@app.route('/form/', methods=['GET'])
def form_get():
    cursor.execute('SELECT name from product_categories')
    name_categories = cursor.fetchall()
    name_categories = [item[0] for item in name_categories]  # Распаковываем кортежи в строки

    return render_template('form_search.html', name_categories=name_categories)


name_categories = None


@app.route('/form/', methods=['POST'])
def form_post():
    cookie = request.form['cookie']
    categories = request.form['categories']

    # Добавляем название категории в базу если такого не существует
    cursor.execute('SELECT name FROM product_categories WHERE name=?', (categories,))
    if len(cursor.fetchall()) == 0:
        cursor.execute('INSERT INTO product_categories (name) values(?)', (categories,))
    else:
        cursor.execute('UPDATE product_categories SET name=? WHERE name=?', (categories, categories,))

    # Запускаем программу парсинга и передаём ей параметры из формы
    result = parser.parser(categories, cookie)
    pprint.pprint(result)

    # Создаём таблицу для категории товаров или обновляем если такая существует
    cursor.execute("DROP TABLE IF EXISTS {}".format(categories))
    cursor.execute("CREATE TABLE {} (id INTEGER PRIMARY KEY AUTOINCREMENT, name, price, foto, url)".format(categories))

    # Добавляем результаты в базу данных
    for item in result:
        cursor.execute('INSERT INTO {} (name, price, foto, url) VALUES (?, ?, ?, ?)'.format(categories),
                       (item['name'], item['price'], item['foto'], item['url']))

    conn.commit()
    # conn.close()

    text = 'Поиск завершён, с результатами вы можете ознакомиться по ссылкам ниже'
    text_result = {
        'table': 'Таблица с результатами',
        'file_csv': 'Скачать файл .CSV с результатами',
        'file_json': 'Скачать файл .JSON с результатами'
    }

    cursor.execute('SELECT name from product_categories')
    name_categories = cursor.fetchall()
    name_categories = [item[0] for item in name_categories]  # Распаковываем кортежи в строки

    return render_template('form_search.html', text=text, **text_result, name_categories=name_categories)


@app.route("/download_csv/")
def get_csv():
    path = os.path.abspath(f'{parser.category}.csv')  # Путь к файлу
    try:
        return send_file(path, as_attachment=True)
    except FileNotFoundError:
        pass


@app.route("/download_json/")
def get_json():
    path = os.path.abspath(f'{parser.category}.json')  # Путь к файлу
    try:
        return send_file(path, as_attachment=True)
    except FileNotFoundError:
        pass


@app.route('/table/')
def table():
    text_result = {
        'file_csv': 'Скачать файл .CSV с результатами',
        'file_json': 'Скачать файл .JSON с результатами'
    }
    try:
        # Запрос в базу для выборки данных
        name = 'noutbuki'
        cursor.execute('SELECT name, price, foto, url FROM {}'.format(name))
        result = cursor.fetchall()


        # with open(f'{parser.category}.json') as file:
        #     result = json.load(file)
        #     keys = result[0].keys()
        #     num_keys = len(keys)

    except:
        keys = 'НЕТ РЕЗУЛЬТАТОВ ПОИСКА'
        num_keys = 5
        result = 'НЕТ РЕЗУЛЬТАТОВ ПОИСКА'

    return render_template('table_result.html', result=result, **text_result)


if __name__ == '__main__':
    app.run(debug=True)
