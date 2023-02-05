import re
import json
import requests
import pprint
from collections import Counter
from statistics import mean
from string import ascii_letters

url_vacancies = 'https://api.hh.ru/vacancies'

n = 'Python Developer OR Python Junior OR Junior Python'

name = input('Введите название интересующей вакансии: ')
num_page = input("Сколько страниц обработать")

def request():  # Функция get запроса по параметрам
    result = requests.get(url_vacancies, params=params).json()
    return result


get = requests.get(url_vacancies).json()

num_vacancies = 0   # Количество вакансий
employment = []  # Список вакансий по занятости
url_alternate = []  # Список вакансий со стажировками
area = []  # Список количества вакансий по городам
skills = []  # Список ключевых требований

salary = {  # Диапазон зарплат
    'from': [],
    'to': []
}

for page in range(get['pages']):            # Перебираем страницы с вакансиями
    if page > num_page:
        break
    else:
        print(f'Ищем на странице {page}')
        params = {                          # Подставляем название вакансии и номер страницы
            'text': f'NAME:({name})',
            'page': page
        }
    for item in request()['items']:  # Перебираем вакансии из запроса
        url = requests.get(item['url']).json()  # Делаем запрос на вакансию
        num_vacancies += 1  # Считаем вакансии

        if url['salary']:                       # Если в вакансии указана зарплата
            if url['salary']['from']:           # Сортируем в список по диапазону зарплат от и до
                salary['from'].append(url['salary']['from'])
            if url['salary']['to']:
                salary['to'].append(url['salary']['to'])

        employment.append(url['employment']['name'])  # Сортируем в список по виду занятости
        if url['employment']['name'] in 'Стажировка':  # Если есть стажировка, добавляем в список
            url_alternate.append(url['alternate_url'])

        if url['area']:                         # Ищем количество вакансий по городам
            area.append(url['area']['name'])

        for skill in url['key_skills']:                 # Поиск по ключевым требованиям
            skills.append(skill['name'])
        if item['snippet']['requirement']:
            for skill in item['snippet']['requirement']:            # Поиск требований по описанию
                skills_re = re.findall(r'\s[A-Za-z-/]+', skill)     # Сортировка результата по символам
                skill_lst = list(filter(lambda x: len(x) > 2, skills_re))
                skills.extend(skill_lst)

# Формируем список с результатами парсинга
result = [{
    'keywords': name,
    'total_vacancies': num_vacancies,
    'requirements': [],
    'salary': {
        'from': round(mean(salary['from']), 0),
        'to': round(mean(salary['to']), 0)
    },
    'employment': [],
    'area': []

}]

skills_counter = Counter(skills)
employment_counter = Counter(employment)
area_counter = Counter(area)
# print(skills)
for name, count in skills_counter.most_common(10):  # Добавляем в результат списки с навыками
    result[0]['requirements'].append({
        'name': name,
        'count': count,
        'percent': f'{round(count / len(skills) * 100, 1)}%'
    })

for name, count in employment_counter.most_common():    # Добавляем виды занятости
    result[0]['employment'].append({
        'name': name,
        'count': count,
        'percent': f'{round(count / len(employment) * 100, 1)}%',
    })

for name, count in area_counter.most_common():  # Добавляем количество вакансий по городам
    result[0]['area'].append({
        'name': name,
        'count': count,
        'percent': f'{round(count / len(area) * 100, 1)}%'
    })

result[0]['employment'][0].update({'url_internship': url_alternate})


pprint.pprint(result)
with open('hh vacancies.json', 'w', encoding='utf-8') as f:
    json.dump(result, f)

with open('url_internship.json', 'w+') as f:
    json.dump(url_alternate, f)


if __name__ == '__main__':
    f = True

