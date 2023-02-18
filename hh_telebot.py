import telebot
from telebot import types
from hh_parser import Parser
import os
from os.path import exists
import time
import json
import pprint

TOKEN = ''

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    bot.reply_to(message, f'Приветствую Вас {message.chat.first_name}!\n'
                          f'Добро пожаловать  в чат бот для парсинга сайта hh.ru')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembutparser = types.KeyboardButton('/parser')
    itembutfile = types.KeyboardButton('/file')
    itembuthelp = types.KeyboardButton('/help')

    markup.row(itembutparser, itembutfile, itembuthelp)

    bot.send_message(user_id, "Выберите пункт меню: ", reply_markup=markup)


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to((message), f'Данный бот позволяет сформировать отчёт по названию вакансии с сайта hh.ru\n'
                            f'Отчёт представляет собой файл формата .CSV\n'
                            f'В нём будут собраны:\n'
                            f'- Наиболее востребованные навыки\n'
                            f'- Средняя заработная плата\n'
                            f'- Количество вакансий в разных городах\n'
                            f'- Виды занятости, а также ссылки на вакансии со стажировкой.\n'
                            f'Для начала поиска введите команду /parser, а затем название вакансии\n'
                            f'После завершения поиска файл с отчётом будет доступен по команде /file')


parser = Parser()


@bot.message_handler(commands=['parser'])  # Команда просит ввести данные для поиска и запускает парсер
def run_parser(message):
    bot.reply_to(message, 'Введите название вакансии для поиска...')

    @bot.message_handler(content_types=['text'])
    def answer(message):
        user_id = message.chat.id
        bot.send_message(user_id, f'Начинаем процесс поиска\n'
                                  f'Пожалуйста подождите...')

        name_vacancies = message.text
        parser.start_parser(name_vacancies)  # Передаём название вакансии в парсер
        parser.making_csv(name_vacancies)  # Создаём файл CSV с результатами
        bot.send_message(user_id, f'Поиск завершён...\n'
                                  f'Результаты доступны по команде /file')


@bot.message_handler(commands=['file'])  # Команда отправляет файл с результатами парсинга
def send_file(message):
    user_id = message.chat.id
    print(user_id)
    try:
        if exists(parser.name_csv):
            with open(parser.name_csv, encoding='utf-8') as f:
                print(f)
                bot.send_document(user_id, f)

    except:
        bot.send_message(user_id, 'Файл не найден, используйте команду /parser для создания.')
    else:
        bot.send_message(user_id, 'Файл не найден, используйте команду /parser для создания.')


bot.infinity_polling()

# @bot.message_handler(commands=['parser'])  # Команда просит ввести данные для поиска и запускает парсер
# def run_parser(message):
#     bot.reply_to(message, 'Введите название вакансии для поиска...')
#
#     @bot.message_handler(content_types=['text'])
#     def answer(message):
#         user_id = message.chat.id
#         name_vacancies = message.text
#         result = start_parser(name_vacancies)  # Передаём название вакансии в парсер
#         text = output_print()
#         sent_message = bot.send_message(user_id, text)
#         while True:
#             new_text = output_print()
#             print(new_text)
#             if new_text != text:
#                 text = new_text
#                 bot.edit_message_text(chat_id=user_id, message_id=sent_message.message_id, text=text)
#             time.sleep(0.1)
#             # bot.send_message(user_id, f'Поиск завершён...\n'
#             #                           f'Результаты доступны по команде /file')
