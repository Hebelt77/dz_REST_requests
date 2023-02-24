from flask import Flask, render_template, request, send_file
from html_parser import Parser
import json
import os

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
    return render_template('form_search.html')


name_categories = None


@app.route('/form/', methods=['POST'])
def form_post():
    cookie = request.form['cookie']
    categories = request.form['categories']

    # Запускаем программу парсинга и передаём ей параметры из формы
    parser.parser(categories, cookie)

    text = 'Поиск завершён, с результатами вы можете ознакомиться по ссылкам ниже'
    text_result = {
        'table': 'Таблица с результатами',
        'file_csv': 'Скачать файл .CSV с результатами',
        'file_json': 'Скачать файл .JSON с результатами'
    }

    return render_template('form_search.html', text=text, **text_result)


@app.route("/download_csv/")
def get_csv():
    path = os.path.abspath(f'{parser.category}.csv')    # Путь к файлу
    try:
        return send_file(path, as_attachment=True)
    except FileNotFoundError:
        pass


@app.route("/download_json/")
def get_json():
    path = os.path.abspath(f'{parser.category}.json')   # Путь к файлу
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
        with open(f'{parser.category}.json') as file:

            result = json.load(file)
            keys = result[0].keys()
            num_keys = len(keys)

    except:
        keys = 'НЕТ РЕЗУЛЬТАТОВ ПОИСКА'
        num_keys = 5
        result = 'НЕТ РЕЗУЛЬТАТОВ ПОИСКА'

    return render_template('table_result.html', result=result, keys=keys, num_keys=num_keys, **text_result)


if __name__ == '__main__':
    app.run(debug=True)
