def print_str(stroka):
    return stroka
    # return print(stroka)


def start_menu():
    text = (f'Добро пожаловать в игру лото:)\n'
          f'\n'
          f'Для начала выберите пункт меню\n'
          f'1.) Один игрок с компьютером.\n'
          f'2.) Компьютер с компьютером.\n'
          f'3.) Несколько игроков (Два и более)')

    # print_str(f'Добро пожаловать в игру лото:)\n'
    #           f'\n'
    #           f'Для начала выберите пункт меню\n'
    #           f'1.) Один игрок с компьютером.\n'
    #           f'2.) Компьютер с компьютером.\n'
    #           f'3.) Несколько игроков (Два и более)')

    point = input('>>: ')
    while point not in '123':
        point = input(f'Не верный ввод!!!\n'
                      f'Введите номер пункта меню >>: ')
    if point == '1':
        name_player = input(
            "Введите имя игрока >>: ")  # Добавляем список игроков в свойство класса для инстанцирования
        return point, name_player  # Возвращаем номер пункта и имя игрока

    if point == '2':
        return point, None  # Возвращаем номер пункта

    if point == '3':
        numbers = input("Введите количество игроков >>: ")
        while not isinstance(numbers, int) or numbers < 2:
            try:
                numbers = int(numbers)
                1 / 0 if numbers < 2 else print()  # Вызываем ошибку если
            except:  # количесто игроков меньше 2
                numbers = input("Введите числовое значение больше 2!!! >>: ")

        names_players = list()
        for i in range(numbers):  # Формируем список с именами игроков
            names_players.append(input(f"Введите имя {i + 1} игрока >>: "))

        return point, names_players  # Возвращаем номер пункта и список игроков


if __name__ == '__main__':
    start_menu()
