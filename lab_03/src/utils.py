from itertools import islice
import random


COUNT = 10000


class LCG:
    def __init__(self, seed = 0x3c6ef35f):
        self.current = seed
        self.m = 2 ** 32
        self.a = 0x19660d
        self.c = 66037

    def get_number(self, low=0, high=100):
        self.current = (self.a * self.current + self.c) % self.m
        result = int(low + self.current % (high - low))
        return result


def table_rand():
    numbers = set()
    with open('../cfg/table.txt') as file: 
        line_num = 0
        lines = islice(file, line_num, None)
        for l in lines:
            numbers.update(set(l.split(" ")[1:-1]))
            line_num += 1
            if len(numbers) >= 3 * COUNT + 1:
                break
        numbers.remove("") 
        numbers = list(numbers)[:3 * COUNT]
    one_digit = [int(i) % 10 for i in numbers[:COUNT]]
    two_digits = [int(i) % 90 + 10 for i in numbers[COUNT:COUNT * 2]]
    three_digits = [int(i) % 900 + 100 for i in numbers[COUNT * 2:3 * COUNT]]
    return one_digit, two_digits, three_digits


def alg_rand():
    randomClass = LCG()
    one_digit = [randomClass.get_number(0, 10) for _ in range(COUNT)]
    two_digits = [randomClass.get_number(10, 100) for _ in range(COUNT)]
    three_digits = [randomClass.get_number(100, 1000) for _ in range(COUNT)]
    return one_digit, two_digits, three_digits


def calc_hi(arr, n, start, end):
    tab = [0 for _ in range(start + end)]
    for i in range(n):
        tab[arr[i]] += 1
    s = 0
    p = (end - start)
    for i in tab:
        s += i * i * p
    return s / n - n 
