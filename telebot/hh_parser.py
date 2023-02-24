import re
import json
import threading

import requests
import pprint
import time
from collections import Counter
from statistics import mean
from csv import DictWriter

url_vacancies = 'https://api.hh.ru/vacancies'

n = 'Python Developer OR Python Junior OR Junior Python'


# name = input('Введите название интересующей вакансии: ')
# num_page = input("Сколько страниц обработать: ")
class Parser:

    def __init__(self):
        self.result = {}
        self.name_csv = None
        self.str = None

    def __str__(self):
        stroka = self.str
        return f"{stroka}"

    def output_print(self, stroka='Пусто'):
        self.str = stroka
        print(stroka)
        return stroka

    def start_parser(self, name_vacancies, num_page=7):

        get = requests.get(url_vacancies).json()

        num_vacancies = 0  # Количество вакансий
        employment = []  # Список вакансий по занятости
        url_alternate = []  # Список вакансий со стажировками
        area = []  # Список количества вакансий по городам
        skills = []  # Список ключевых требований

        salary = {  # Диапазон зарплат
            'from': [],
            'to': []
        }
        for page in range(1, get['pages']):  # Перебираем страницы с вакансиями
            if page > int(num_page):
                break
            else:
                self.output_print(f'Ищем на странице {page}')
                params = {  # Подставляем название вакансии и номер страницы
                    'text': f'NAME:({name_vacancies})',
                    'page': page
                    # 'area': '1446'
                }
            for item in requests.get(url_vacancies, params=params).json()['items']:  # Перебираем вакансии из запроса
                url = requests.get(item['url']).json()  # Делаем запрос на вакансию
                num_vacancies += 1  # Считаем вакансии

                if url['salary']:  # Если в вакансии указана зарплата
                    if url['salary']['from']:  # Сортируем в список по диапазону зарплат от и до
                        salary['from'].append(url['salary']['from'])
                    if url['salary']['to']:
                        salary['to'].append(url['salary']['to'])

                employment.append(url['employment']['name'])  # Сортируем в список по виду занятости
                if url['employment']['name'] in 'Стажировка':  # Если есть стажировка, добавляем в список
                    url_alternate.append(url['alternate_url'])

                if url['area']:  # Ищем количество вакансий по городам
                    area.append(url['area']['name'])

                for skill in url['key_skills']:  # Поиск по ключевым требованиям
                    skills.append(skill['name'])
                if item['snippet']['requirement']:
                    for skill in item['snippet']['requirement']:  # Поиск требований по описанию
                        skills_re = re.findall(r'\s[A-Za-z-/]+', skill)  # Сортировка результата по символам
                        skill_lst = list(filter(lambda x: len(x) > 2, skills_re))
                        skills.extend(skill_lst)

        # Формируем список с результатами парсинга
        self.result = {
            'keywords': name_vacancies,
            'total_vacancies': num_vacancies,
            'requirements': [],
            'salary': {
                'from': round(mean(salary['from']), 0) if salary['from'] else None,
                'to': round(mean(salary['to']), 0) if salary['to'] else None
            },
            'employment': [],
            'area': []
        }

        skills_counter = Counter(skills)
        employment_counter = Counter(employment)
        area_counter = Counter(area)
        # print(skills)
        for name, count in skills_counter.most_common(10):  # Добавляем в результат списки с навыками
            self.result['requirements'].append({
                'name': name,
                'count': count,
                'percent': f'{round(count / len(skills) * 100, 1)}%'
            })

        for name, count in employment_counter.most_common():  # Добавляем виды занятости
            self.result['employment'].append({
                'name': name,
                'count': count,
                'percent': f'{round(count / len(employment) * 100, 1)}%',
            })

        for name, count in area_counter.most_common():  # Добавляем количество вакансий по городам
            self.result['area'].append({
                'name': name,
                'count': count,
                'percent': f'{round(count / len(area) * 100, 1)}%'
            })
        if self.result['employment']:
            self.result['employment'][0].update({'url_internship': url_alternate})

        pprint.pprint(self.result)
        with open('../hh vacancies.json', 'w', encoding='utf-8') as f:
            json.dump(self.result, f)

        with open('url_internship.json', 'w+') as f:
            json.dump(url_alternate, f)

        return self.result

    def making_csv(self, name):
        self.name_csv = f'vacancies {name}.csv'
        with open(self.name_csv, 'w', encoding='utf-8') as f:
            file = DictWriter(f, fieldnames=['keywords', 'total_vacancies', 'requirements', 'salary', 'area',
                                             'employment'],
                              delimiter=';')
            file.writeheader()
            file.writerow(self.result)
        return self.name_csv


if __name__ == '__main__':
    parser = Parser()
    parser.start_parser(n)
