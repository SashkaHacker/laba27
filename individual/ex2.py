#!usr/bin/env python3
# -*- coding: utf-8 -*-

from random import randint


if __name__ == "__main__":
    rows, cols = input("Введите количество строк: "), input(
        "Введите количество столбцов: "
    )
    try:
        rows = int(rows)
        cols = int(cols)
    except ValueError:
        print("В одном из введенных значений не число")
        exit(1)

    matrix = [[randint(-1000, 1000) for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            print(matrix[i][j], end=" ")
        print("\n")
