import random
import time
import json
import sys
import os

class BullsAndCows:

    def __init__(self):
        def get_number():
            """Функция загадывания числа"""
            number_list = random.sample(range(1, 10), 5)
            return ''.join(str(i) for i in number_list)

        self.computer_number = get_number()
        self.chosen_numbers = set()

    def start(self):
        print("\nДобро пожаловать в игру 'Быки и Коровы'!\n")
        time.sleep(1)
        print("Правила игры: компьютер загадывает пятизначное число из любых\n"
              "  неповторяющихся цифр (0-9). Игроку следует отгадать его за "
              "минимальное\n  количество попыток.\n  На каждой попытке игроку "
              "предлагается угадать и ввести загаданное число.\n  Компьютер "
              "сравнит числа и выведет 'к' на каждую цифру, присутствующую в "
              "обоих\n  числах и 'б' в случае, если также была угадана и "
              "позиция цифры. Исходя из\n  этого, игрок вводит новое число.\n"
              "  Пример: загаданное число 12345, введённое 13094. Результат: "
              "бкк\n  (цифра 1 - бык, т.к. она угадана и стоит на своей "
              "позиции; 3 и 4 - коровы,\n  т.к. цифры угаданы, но стоят на "
              "других позициях.)\n\nКак будете готовы, запустится счётчик "
              "времени. Для начала игры нажмите\n  клавишу Enter.", end="")
        input()

        print("Игра началась!\n")
        self.time_start = time.time()

        self.attempts_count = 1  # счётчик попыток
        while True:
            user_number = input("Введите число: ")

            # проверка ввода
            if not(self.is_correct_number(user_number)):
                continue

            # сравнение чисел
            answer = self.compare_numbers(user_number)
            if answer != "ббббб":
                print("Результат:" + " " * 5 + answer, end="\n\n")
                self.attempts_count += 1
            else:
                if self.attempts_count == 1:
                    print("\nНевероятное везенье! Победа с первого раза!")
                else:
                    print("\nВы угадали число! Это победа!")
                time.sleep(1)
                break

        # работа с файлом
        data = self.add_data_to_file()

        # вывод таблицы рекордов
        self.print_table(data)

        print("\nДля выхода из игры нажмите Enter.")
        input()
        sys.exit()

    def is_correct_number(self, number):
        """Проверка корректности ввода."""
        if not number.isdigit():
            print("Будьте внимательны! Следует вводить числа.")
            return False

        if len(number) != 5:
            print("Будьте внимательны! В числе должно быть ровно 5 цифр.")
            return False

        if len(number) != len(set(number)):
            print("Будьте внимательны! В числе не должно быть "
                  "повторяющихся цифр.")
            return False

        if number in self.chosen_numbers:
            print("Будьте внимательны! Вы уже вводили это число.")
            return False
        self.chosen_numbers.add(number)

        return True

    def compare_numbers(self, number):
        """Сравнение загаданного и введённого чисел."""
        bulls_count = 0
        cows_count = 0

        for num in self.computer_number:
            if num in number:
                if self.computer_number.index(num) == number.index(num):
                    bulls_count += 1
                else:
                    cows_count += 1

        result = "б" * bulls_count + "к" * cows_count
        if result:
            return result
        return "нет совпадений"

    def add_data_to_file(self):
        """Работа с файлом"""
        # расчет продолжительности игры
        duration = time.time() - self.time_start
        print("\nИгра длилась: {}\nКол-во попыток: {}"
              .format(self.str_time(duration), self.attempts_count))

        # ввод имени
        print("\nДля занесения результата в историю, представьтесь, "
              "пожалуйста (< 20 симв.):")
        name = input()

        if os.path.isfile("records.json"):
            try:
                f = open("records.json", "r", encoding="utf-8")
                data = list(map(lambda x: (False, x), json.load(f)))
                f.close()
            except Exception:
                print("Ошибка при чтении файла. Статистика будет "
                      "перезаписана.")
                data = []
        else:
            print("\nФайла с рекордами не найдено. Вы будете первым в "
                  "истории.")
            time.sleep(1)
            data = []
        f = open("records.json", "w", encoding="utf-8")
        data.append((True, {"name": name[:20], "attempts": self.attempts_count,
                            "time": duration}))  # True для метки в таблице
        json.dump(list(map(lambda x: x[1], data)), f, indent=2)
        f.close()

        return data

    def str_time(self, seconds):
        """"Вывод времени."""
        seconds = int(seconds)
        hours = seconds // 3600
        seconds -= hours * 3600
        minutes = seconds // 60
        seconds -= minutes * 60

        result = ""
        if hours:
            result += "{}ч.".format(hours)

        if not hours and not minutes:
            pass
        else:
            space = ""
            if result:
                space = " "
            result += "{}{}м.".format(space, minutes)

        space = ""
        if result:
            space = " "
        result += "{}{}с.".format(space, seconds)

        return result

    def print_table(self, data):
        """Печать таблицы рекордов"""
        print("\nТаблица рекордов:\n\n      Имя:", " " * 23, "Попытки:",
              " " * 9, "Время:")
        data = sorted(data, key=lambda x: x[1]["time"])
        data = sorted(data, key=lambda x: x[1]["attempts"])
        for num, line in enumerate(data, start=1):
            now = "" if not line[0] else "-->"
            name = line[1]["name"]
            attempts = line[1]["attempts"]
            time = self.str_time(line[1]["time"])
            print("{:>3} {:>3}. {:25}{:>9}{:>17}".format(now, num, name,
                                                         attempts, time))


if __name__ == "__main__":

    game = BullsAndCows()
    game.start()
