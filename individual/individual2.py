#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Изучить возможности модуля logging. Добавить для предыдущего задания вывод в файлы лога
# даты и времени выполнения пользовательской команды с точностью до миллисекунды.

import json
import logging
from datetime import datetime
from pathlib import Path

from validation import ListWorkers


def add_worker(lst, surname, name, phone, date):
    try:
        dct = {
            "surname": surname,
            "name": name,
            "phone": phone,
            "date": date.split(":"),
        }
        lst.append(dct)
    except Exception:
        return "Ошибка в входных данных."


def phone(lst, numbers_phone):
    try:
        numbers_phone = int(numbers_phone)
    except Exception:
        return "Ошибка, номер указан не верно."
    fl = True
    for i in lst:
        if i["phone"] == numbers_phone:
            print(
                f"Фамилия: {i['surname']}\n"
                f"Имя: {i['name']}\n"
                f"Номер телефона: {i['phone']}\n"
                f"Дата рождения: {':'.join(i['date'])}"
            )
            fl = False
            break
    if fl:
        print("Человека с таким номером телефона нет в списке.")


def instruction():
    print(
        "add - добавление нового работника\n"
        "select - данные о работнике по его номеру телефона\n"
        "exit - завершение программ\n"
        "list - список работников\n"
        "help - вывод справки\n"
    )


def save_workers(file_name, staff):
    """
    Сохранить всех работников в файл JSON.
    """
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(staff, fout, ensure_ascii=False, indent=4)


def load_workers(file_name):
    """
    Загрузить всех работников из файла JSON.
    """
    with open(file_name, "r", encoding="utf-8") as fin:
        data = json.load(fin)
    try:
        ListWorkers(lst=data)
        data.sort(
            key=lambda x: datetime.strptime("-".join(x["date"]), "%d-%m-%Y")
        )
        return data
    except Exception:
        print("Invalid JSON")


def show_workers(lst):
    """
    Отобразить список работников.
    """
    # Проверить, что список работников не пуст.
    if lst:
        # Блок заголовка таблицы
        line = "+-{}-+-{}-+-{}-+-{}-+-{}-+".format(
            "-" * 4, "-" * 30, "-" * 20, "-" * 15, "-" * 15
        )
        print(line)
        print(
            f'| {"№":^4} | {"Фамилия":^30} | {"Имя":^20} | '
            f'{"Номер телефона":^15} | {"Дата рождения":^15} |'
        )

        print(line)
        # Вывести данные о всех сотрудниках.
        for idx, worker in enumerate(lst, 1):
            print(
                f'| {idx:>4} | {worker.get("surname", ""):<30} | '
                f'{worker.get("name", ""):<20}'
                f' | {worker.get("phone", 0):>15}'
                f' | {":".join(worker.get("date", 0)):>15} |'
            )

        print(line)
    else:
        print("Список работников пуст.")


def main():
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        filename="individual2.log", encoding="utf-8", level=logging.DEBUG
    )
    filename = input("Укажите файл (опционально): ")
    logger.info(f"{datetime.now()} Запуск программы.")
    is_dirty = False

    # Файл по умолчанию
    if filename == "":
        filename = "data.json"

    path_to_home = Path(filename)
    if path_to_home.exists():
        lst = load_workers(path_to_home)
    else:
        lst = []

    # Цикл программы
    while True:
        command = input("Введите команду: ").lower()
        match command:
            case "exit":
                logger.info(f"{datetime.now()} Прекращена работа программы.")
                break
            case "add":
                surname = input("Введите фамилию: ")
                name = input("Введите имя: ")
                numbers = int(input("Введите номер телефона: "))
                date = input("Введите дату рождения в формате (ДД:ММ:ГГГГ): ")
                is_dirty = True
                result = add_worker(lst, surname, name, numbers, date)
                if result:
                    logger.error(f"{datetime.now()} Ошибка в воде данных.")
                    print(result)
                else:
                    logger.info(
                        f"{datetime.now()} Добавление сотрудника {surname}"
                        f" {name}"
                    )
            case "select":
                numbers = input("Введите номер телефона: ")
                result = phone(lst, numbers)
                if result:
                    print(result)
                    logger.error(f"{datetime.now()} Номер указан не верно.")
                else:
                    logger.info(
                        f"{datetime.now()} "
                        f"Выведен сотрудник по номеру телефона: {numbers}."
                    )
            case "help":
                instruction()
                logger.info(f"{datetime.now()} Выведена справочная информация.")
            case "list":
                show_workers(lst)
                logger.info(
                    f"{datetime.now()} Выведена информация о всех сотрудниках."
                )
            case _:
                logger.error(
                    f"{datetime.now()} Введена неверная команда: {command}"
                )
                print(f"Неизвестная команда {command}")

    if is_dirty:
        save_workers(filename, lst)


if __name__ == "__main__":
    main()
