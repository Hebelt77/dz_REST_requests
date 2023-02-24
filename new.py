from telebot.hh_parser import *

import pprint

# with open('result.csv', encoding='utf-8', newline='') as f:
#     reader = csv.DictReader(f)
#
#     for item in reader:
#         # print(item['name'], item['price'], item['foto'], item['url'], item['reviews'])
#         # print(item)
#         ff = (item['name;price;foto;url;reviews'])
#         print(ff.split(';')[0])

with open('results_parsing.json') as file:
    result = json.load(file)
    pprint.pprint(result)





# start_loto.start_menu()
# def print_str(stroka='ddd'):
#     # print(stroka)
#     return stroka
#
#
# def start():
#     print_str(f'Hello world!!!')
#     print_str(f'Hello world!!!')
#     print_str(f'Hello world!!!')
#
#
# print(start())

# DOMAIN = 'https://api.hh.ru/areas/'
# area = requests.get(DOMAIN).json()
#
# # print(area)
# resurlt = {}
# for i in area:
#     for j in i['areas']:
#         for y in j['areas']:
#             resurlt.update({y['name']: y['id']})
# # for area in resurlt:
# #     if area['Краснодар'] in area:
# #         print(area['Краснодар'])
# pprint.pprint(resurlt)
# print(resurlt['Шклов'])
