#!usr/bin/env python3
# -*- coding: utf-8 -*-


if __name__ == "__main__":
    a, b = input("Первое значение: "), input("Второе значение: ")
    try:
        a, b = int(a), int(b)
        print(f"Результат: {a + b}")
    except ValueError as e:
        print(f"Результат: {a + b}")
