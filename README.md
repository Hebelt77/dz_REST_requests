# dz_REST_requests
Для работы бота необходим TOKEN из Телеграмм
Данный бот позволяет сформировать отчёт по названию вакансии с сайта hh.ru
Отчёт представляет собой файл формата .CSV
В нём будут собраны:
- Наиболее востребованные навыки
- Средняя заработная плата
- Количество вакансий в разных городах
- Виды занятости, а также ссылки на вакансии со стажировкой.'
Для начала поиска введите команду /parser, а затем название вакансии
После завершения поиска файл с отчётом будет доступен по команде /file'
По команде /start выводится приветсвие с меню команд
По команде /help можно узнать описание работы бота.
Для каждого запроса создаётся отдельный экземпляр класса Parser, таким образом одновременно могут выполняться несколько запросов.

# dz_flask_site
Сервис позволяет производить поиск на сайте www.tehnopark.ru по названию категории товаров
Результатом работы являются следующие результаты:
-Название товара
-Цена товара
-Ссылка на товар
-Ссылка на фото товара
-Отзывы на товар
Для начала работы необходимо вставить cookie в форму с сайта: https://www.technopark.ru/noutbuki/otzyvy/
И выбрать категорию товаров из выпадающего списка
С результатами можно ознакомиться по соответствующим ссылкам
