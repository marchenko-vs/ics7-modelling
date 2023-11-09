import random
import tkinter as tk
import tkinter.messagebox as mb
import numpy as np
import utils


COLOR_BLACK = "#000000"
COLOR_WHITE = "#ffffff"

MAX_NUMBERS = 10
TABLES_NUM = 7
ITERATION = 0

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 750

BORDERS_PART = 0.03
BORDERS_WIDTH = int(WINDOW_WIDTH * BORDERS_PART)
BORDERS_HEIGHT = int(WINDOW_HEIGHT * BORDERS_PART)

MATRIX_PART_WIDTH = 0.7
MATRIX_WIDTH = int(MATRIX_PART_WIDTH * WINDOW_WIDTH)

DATA_PART_WIDTH = 1 - MATRIX_PART_WIDTH - 3 * BORDERS_PART
DATA_PART_HEIGHT = 1 - 2 * BORDERS_PART
DATA_WIDTH = int(DATA_PART_WIDTH * WINDOW_WIDTH)
DATA_HEIGHT = int(DATA_PART_HEIGHT * (WINDOW_HEIGHT))

MATRIX_ENTRIES = list()
INITIAL_CONDITIONS = list()
PROBABILITIES = list()
TIMES = list()
MAIN_TABLE = list()

ROWS = 12
MATRIX_FRAME_ROWS = 11

root = tk.Tk()
root.title("ГПСЧ")
root["bg"] = COLOR_WHITE
root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+0+0')
root.resizable(height=False, width=False)

data_frame = tk.Frame(root)
data_frame["bg"] = COLOR_WHITE

matrix_frame = tk.Frame(root)
matrix_frame["bg"] = COLOR_WHITE

data_frame.place(x=int(BORDERS_WIDTH), y=int(BORDERS_HEIGHT),
                 width=DATA_WIDTH,
                 height=DATA_HEIGHT)

matrix_frame.place(x=int(BORDERS_WIDTH * 2 + DATA_WIDTH), y=int(BORDERS_HEIGHT),
                 width=MATRIX_WIDTH,
                 height=DATA_HEIGHT)


def place_matrix_entries(size):
    global MAIN_TABLE
    for i in range(size + 1):
        curr_y = 100
        for j in range(TABLES_NUM):
            my_height = DATA_HEIGHT // (MATRIX_FRAME_ROWS + 2)
            MAIN_TABLE[i][j].insert(0, '0')
            MAIN_TABLE[i][j].place(x=int(j / TABLES_NUM * MATRIX_WIDTH),
                y=curr_y + i * my_height,
                width=MATRIX_WIDTH // TABLES_NUM,
                height=my_height)


def generate_matrix_entries(size):
    global MAIN_TABLE
    if (len(MAIN_TABLE) > 0):
        for i in range(len(MAIN_TABLE)):
            for j in range(len(MAIN_TABLE[0])):
                MAIN_TABLE[i][j].destroy()
    MAIN_TABLE = [
    [
        tk.Entry(matrix_frame, bg=COLOR_WHITE, font=("Arial", 14), fg=COLOR_BLACK, justify="center")
        for i in range(TABLES_NUM)
    ]
    for j in range(size + 1)
    ]


def set_matrix(size):
    generate_matrix_entries(size)
    place_matrix_entries(size)    


def init_tables(entry):
    global MAX_NUMBERS

    try:
        size = int(entry.get())
        if (size < 1 or size > 10):
            raise ValueError
        MAX_NUMBERS = size
        set_matrix(size)
    except ValueError:
        mb.showerror(title="Ошибка!", message="Длина последовательности должна быть целым числом от 1 до 10.")


def hi_custom():
    try:
        custom_sequence = list()
        for i in range(MAX_NUMBERS):
            custom_sequence.append(int(MAIN_TABLE[i][6].get()))
        
        hi_row = len(MAIN_TABLE) - 1
        MAIN_TABLE[hi_row][6].delete(0, 'end')

        if 0 <= custom_sequence[0] < 10: 
            MAIN_TABLE[hi_row][6].insert(0, '{:.2f}'.format(utils.calc_hi(custom_sequence, MAX_NUMBERS, 0, 10)))
        elif 10 <= custom_sequence[0] < 100: 
            MAIN_TABLE[hi_row][6].insert(0, '{:.2f}'.format(utils.calc_hi(custom_sequence, MAX_NUMBERS, 10, 100)))
        else: 
            MAIN_TABLE[hi_row][6].insert(0, '{:.2f}'.format(utils.calc_hi(custom_sequence, MAX_NUMBERS, 100, 1000)))
    except Exception:
        mb.showerror(title="Ошибка!", message="Некорректно введена последовательность")


def process():
    global MAIN_TABLE
    global MAX_NUMBERS
    global ITERATION

    alg_array_1, alg_array_2, alg_array_3 = utils.alg_rand()
    table_array_1, table_array_2, table_array_3 = utils.table_rand()

    for i in range(MAX_NUMBERS):
        MAIN_TABLE[i][0].delete(0, 'end')
        MAIN_TABLE[i][0].insert(0, alg_array_1[i])
    for i in range(MAX_NUMBERS):
        MAIN_TABLE[i][1].delete(0, 'end')
        MAIN_TABLE[i][1].insert(0, alg_array_2[i])
    for i in range(MAX_NUMBERS):
        MAIN_TABLE[i][2].delete(0, 'end')
        MAIN_TABLE[i][2].insert(0, alg_array_3[i])
    for i in range(MAX_NUMBERS):
        MAIN_TABLE[i][3].delete(0, 'end')
        MAIN_TABLE[i][3].insert(0, table_array_1[i])
    for i in range(MAX_NUMBERS):
        MAIN_TABLE[i][4].delete(0, 'end')
        MAIN_TABLE[i][4].insert(0, table_array_2[i])
    for i in range(MAX_NUMBERS):
        MAIN_TABLE[i][5].delete(0, 'end')
        MAIN_TABLE[i][5].insert(0, table_array_3[i])

    hi_row = len(MAIN_TABLE) - 1
    for i in range(TABLES_NUM):
        MAIN_TABLE[hi_row][i].delete(0, 'end')

    MAIN_TABLE[hi_row][0].insert(0, '{:.2f}'.format(utils.calc_hi(alg_array_1, 10000, 0, 10)))
    MAIN_TABLE[hi_row][1].insert(0, '{:.2f}'.format(utils.calc_hi(alg_array_2, 10000, 10, 100)))
    MAIN_TABLE[hi_row][2].insert(0, '{:.2f}'.format(utils.calc_hi(alg_array_3, 10000, 100, 1000)))
    MAIN_TABLE[hi_row][3].insert(0, '{:.2f}'.format(utils.calc_hi(table_array_1, 10000, 0, 10)))
    MAIN_TABLE[hi_row][4].insert(0, '{:.2f}'.format(utils.calc_hi(table_array_2, 10000, 10, 100)))
    MAIN_TABLE[hi_row][5].insert(0, '{:.2f}'.format(utils.calc_hi(table_array_3, 10000, 100, 1000)))


max_numbers_label = tk.Label(data_frame, text="Длина последовательности", font=("Arial", 14),
                        fg=COLOR_BLACK, bg=COLOR_WHITE)
max_numbers_entry = tk.Entry(data_frame, fg=COLOR_BLACK, font=("Arial", 14),
                      bg=COLOR_WHITE, justify="center")
max_numbers_entry.insert(0, '10')
max_numbers_button = tk.Button(data_frame, text="Задать", font=("Arial", 14), 
                               bg=COLOR_WHITE, fg=COLOR_BLACK, command=lambda: init_tables(max_numbers_entry))

matrix_label = tk.Label(matrix_frame, text="Последовательности случайных чисел", font=("Arial", 14),
                        bg=COLOR_WHITE, fg=COLOR_BLACK)

alg_label = tk.Label(matrix_frame, text="Алгоритмический метод", font=("Arial", 14),
                        bg=COLOR_WHITE, fg=COLOR_BLACK)

table_label = tk.Label(matrix_frame, text="Табличный метод", font=("Arial", 14),
                        bg=COLOR_WHITE, fg=COLOR_BLACK)

user_label = tk.Label(matrix_frame, text="Пользовательская\nпосл-ть", font=("Arial", 14),
                        bg=COLOR_WHITE, fg=COLOR_BLACK)

generate_button = tk.Button(data_frame, text="Сгенерировать", font=("Arial", 14),
                      bg=COLOR_WHITE, fg=COLOR_BLACK, command=process,)

estimate_button = tk.Button(data_frame, text="Оценить", font=("Arial", 14),
                      bg=COLOR_WHITE, fg=COLOR_BLACK, command=hi_custom,)

max_numbers_label.place(x=0, y=DATA_HEIGHT * 0 // ROWS, width=DATA_WIDTH,
                  height=DATA_HEIGHT // ROWS)

max_numbers_entry.place(x=0, y=DATA_HEIGHT * 1 // ROWS, width=DATA_WIDTH,
                  height=DATA_HEIGHT // ROWS)

max_numbers_button.place(x=0, y=DATA_HEIGHT * 2 // ROWS, width=DATA_WIDTH,
                  height=DATA_HEIGHT // ROWS)

generate_button.place(x=0, y=DATA_HEIGHT * 3 // ROWS, width=DATA_WIDTH,
                  height=DATA_HEIGHT // ROWS)

estimate_button.place(x=0, y=DATA_HEIGHT * 4 // ROWS, width=DATA_WIDTH,
                  height=DATA_HEIGHT // ROWS)

matrix_label.place(x=0, y=DATA_HEIGHT // MATRIX_FRAME_ROWS - 75, width=MATRIX_WIDTH,
                  height=DATA_HEIGHT // MATRIX_FRAME_ROWS)

alg_label.place(x=75, y=DATA_HEIGHT // MATRIX_FRAME_ROWS - 25, width=300,
                  height=DATA_HEIGHT // MATRIX_FRAME_ROWS)
table_label.place(x=475, y=DATA_HEIGHT // MATRIX_FRAME_ROWS - 25, width=300,
                  height=DATA_HEIGHT // MATRIX_FRAME_ROWS)
user_label.place(x=745, y=DATA_HEIGHT // MATRIX_FRAME_ROWS - 25, width=300,
                  height=DATA_HEIGHT // MATRIX_FRAME_ROWS)

set_matrix(MAX_NUMBERS)

root.mainloop()
