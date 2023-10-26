import random
import tkinter as tk
import tkinter.messagebox as mb
import numpy as np
from utils import solve


COLOR_BLACK = "#000000"
COLOR_WHITE = "#ffffff"

STATES_NUM = 0

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800

BORDERS_PART = 0.03
BORDERS_WIDTH = int(WINDOW_WIDTH * BORDERS_PART)
BORDERS_HEIGHT = int(WINDOW_HEIGHT * BORDERS_PART)

MATRIX_PART_WIDTH = 0.7
MATRIX_WIDTH = int(MATRIX_PART_WIDTH * WINDOW_WIDTH)

DATA_PART_WIDTH = 1 - MATRIX_PART_WIDTH - 3 * BORDERS_PART
DATA_PART_HEIGHT = 1 - 2 * BORDERS_PART
DATA_WIDTH = int(DATA_PART_WIDTH * WINDOW_WIDTH)
DATA_HEIGHT = int(DATA_PART_HEIGHT * (WINDOW_HEIGHT - 100))

MATRIX_ENTRIES = list()
INITIAL_CONDITIONS = list()
PROBABILITIES = list()
TIMES = list()

ROWS = 12
MATRIX_FRAME_ROWS = 17

root = tk.Tk()
root.title("Цепь Маркова")
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


def place_times(size, values):
    global TIMES
    for i in range(size):
        TIMES[i].insert(0, '{:.4f}'.format(values[i]))
    for i in range(size):
        TIMES[i].place(x=int(i / size * MATRIX_WIDTH), y=DATA_HEIGHT * 16 // MATRIX_FRAME_ROWS,
                                 width=MATRIX_WIDTH // size, height=DATA_HEIGHT // MATRIX_FRAME_ROWS)


def generate_times(size):
    global TIMES
    if (len(TIMES) > 0):
        for i in range(len(TIMES)):
            TIMES[i].destroy()
    TIMES = [
    tk.Entry(matrix_frame, bg=COLOR_WHITE, font=("Arial", 14), fg=COLOR_BLACK, justify="center") 
    for i in range(size)
]


def place_probabilities(size, values):
    global PROBABILITIES
    for i in range(size):
        PROBABILITIES[i].insert(0, '{:.4f}'.format(values[i]))
    for i in range(size):
        PROBABILITIES[i].place(x=int(i / size * MATRIX_WIDTH), y=DATA_HEIGHT * 14 // MATRIX_FRAME_ROWS,
                                 width=MATRIX_WIDTH // size, height=DATA_HEIGHT // MATRIX_FRAME_ROWS)


def generate_probabilities(size):
    global PROBABILITIES
    if (len(PROBABILITIES) > 0):
        for i in range(len(PROBABILITIES)):
            PROBABILITIES[i].destroy()
    PROBABILITIES = [
    tk.Entry(matrix_frame, bg=COLOR_WHITE, font=("Arial", 14), fg=COLOR_BLACK, justify="center") 
    for i in range(size)
]


def place_matrix_entries(size):
    for i in range(size):
        for j in range(size):
            MATRIX_ENTRIES[i][j].insert(0, '0')

    for i in range(size):
        for j in range(size):
            MATRIX_ENTRIES[i][j].place(x=int(j / size * MATRIX_WIDTH),
                y=DATA_HEIGHT * (3 + i) // MATRIX_FRAME_ROWS,
                width=MATRIX_WIDTH // size,
                height=DATA_HEIGHT // MATRIX_FRAME_ROWS)


def generate_matrix_entries(size):
    global MATRIX_ENTRIES
    if (len(MATRIX_ENTRIES) > 0):
        for i in range(len(MATRIX_ENTRIES)):
            for j in range(len(MATRIX_ENTRIES[0])):
                MATRIX_ENTRIES[i][j].destroy()
    MATRIX_ENTRIES = [
    [
        tk.Entry(matrix_frame, bg=COLOR_WHITE, font=("Arial", 14), fg=COLOR_BLACK, justify="center")
        for i in range(size)
    ]
    for j in range(size)
    ]


def place_initial_conditions(size):
    global INITIAL_CONDITIONS
    value = 1.0 / size
    for i in range(size):
        INITIAL_CONDITIONS[i].insert(0, '{:.4f}'.format(value))
    for i in range(size):
        INITIAL_CONDITIONS[i].place(x=int(i / size * MATRIX_WIDTH), y=DATA_HEIGHT * 1 // MATRIX_FRAME_ROWS,
                                 width=MATRIX_WIDTH // size, height=DATA_HEIGHT // MATRIX_FRAME_ROWS)


def generate_initial_conditions(size):
    global INITIAL_CONDITIONS
    if (len(INITIAL_CONDITIONS) > 0):
        for i in range(len(INITIAL_CONDITIONS)):
            INITIAL_CONDITIONS[i].destroy()
    INITIAL_CONDITIONS = [
    tk.Entry(matrix_frame, bg=COLOR_WHITE, font=("Arial", 14), fg=COLOR_BLACK, justify="center") 
    for i in range(size)
]


def set_probabilities(size):
    generate_initial_conditions(size)
    place_initial_conditions(size)


def set_matrix(size):
    generate_matrix_entries(size)
    place_matrix_entries(size)    


def init_chain(entry):
    global STATES_NUM
    try:
        size = int(entry.get())
        if (size < 2 or size > 10):
            raise ValueError
        set_probabilities(size)
        set_matrix(size)
        STATES_NUM = size
    except ValueError:
        mb.showerror(title="Ошибка!", message="Количество состояний должно быть целым числом от 2 до 10.")


def process():
    global STATES_NUM
    global MATRIX_ENTRIES, eps_entry, step_entry
    global INITIAL_CONDITIONS

    if (len(MATRIX_ENTRIES) < 2):
        mb.showerror(title="Ошибка!", message="Введите количество состояний.")
        return

    try:
        eps = float(eps_entry.get())
        step = float(step_entry.get())

        matrix = [[float(MATRIX_ENTRIES[i][j].get()) for j in range(STATES_NUM)] for i in range(STATES_NUM)]
        start_probs = [float(INITIAL_CONDITIONS[i].get()) for i in range(STATES_NUM)]
        
        probabilities, times = solve(matrix, start_probs, step, eps)
        
        generate_probabilities(STATES_NUM)
        place_probabilities(STATES_NUM, probabilities)
        
        generate_times(STATES_NUM)
        place_times(STATES_NUM, times)
    except np.linalg.LinAlgError:
        mb.showerror(title="Ошибка!", message="Некорректно задана матрица интенсивностей.")
    except Exception:
        mb.showerror(title="Ошибка!", message="Некорректно введен шаг или точность.")


def generate_lambdas():
    global lambda_limit_entry, MATRIX_ENTRIES
    if (len(MATRIX_ENTRIES) < 2):
        mb.showerror(title="Ошибка!", message="Некорректно задано количество состояний.")
        return
    try:
        limit = float(lambda_limit_entry.get())
        for i in range(STATES_NUM):
            for j in range(STATES_NUM):
                MATRIX_ENTRIES[i][j].delete(0, len(MATRIX_ENTRIES[i][j].get()))
                MATRIX_ENTRIES[i][j].insert(0, '0' if i == j else f"{random.random() * limit:.4f}")
    except Exception:
        mb.showerror(title="Ошибка!", message="Некорректно введено максимальное значение интенсивности.")


states_num_label = tk.Label(data_frame, text="Количество состояний", font=("Arial", 14),
                        fg=COLOR_BLACK, bg=COLOR_WHITE)
states_num_entry = tk.Entry(data_frame, fg=COLOR_BLACK, font=("Arial", 14),
                      bg=COLOR_WHITE, justify="center")
states_num_entry.insert(0, '2')
states_num_button = tk.Button(data_frame, text="Задать", font=("Arial", 14), command=lambda: init_chain(states_num_entry))

eps_label = tk.Label(data_frame, text="Точность", font=("Arial", 14),
                        fg=COLOR_BLACK, bg=COLOR_WHITE)
eps_entry = tk.Entry(data_frame, bg=COLOR_WHITE, font=("Arial", 14),
                    fg=COLOR_BLACK, justify="center")
eps_entry.insert(0, '1e-5')

step_label = tk.Label(data_frame, text="Шаг", font=("Arial", 14),
                        fg=COLOR_BLACK, bg=COLOR_WHITE)
step_entry = tk.Entry(data_frame, bg=COLOR_WHITE, font=("Arial", 14),
                    fg=COLOR_BLACK, justify="center")
step_entry.insert(0, '1e-3')

lambda_limit_entry = tk.Entry(data_frame, bg=COLOR_WHITE, font=("Arial", 14),
                    fg=COLOR_BLACK, justify="center")
lambda_limit_entry.insert(0, '1.0')

lambda_limit_label = tk.Label(data_frame, text="Максимальное значение\nинтенсивности",
                       font=("Arial", 14), bg=COLOR_WHITE, fg=COLOR_BLACK)

initial_conditions_label = tk.Label(matrix_frame, text="Начальные вероятности состояний",
                       font=("Arial", 14), bg=COLOR_WHITE, fg=COLOR_BLACK)

matrix_label = tk.Label(matrix_frame, text="Матрица интенсивностей", font=("Arial", 14),
                        bg=COLOR_WHITE, fg=COLOR_BLACK)

probabilities_label = tk.Label(matrix_frame, text="Вероятности нахождения системы в заданных состояниях",
                       font=("Arial", 14), bg=COLOR_WHITE, fg=COLOR_BLACK)

times_label = tk.Label(matrix_frame, text="Время пребывания системы в предельном стационарном состоянии",
                       font=("Arial", 14), bg=COLOR_WHITE, fg=COLOR_BLACK)

lambda_gen_button = tk.Button(data_frame, text="Сгенерировать\nинтенсивности", font=("Arial", 14),
                      bg=COLOR_WHITE, fg=COLOR_BLACK, command=generate_lambdas,
                      activebackground=COLOR_WHITE, activeforeground=COLOR_BLACK)

solve_button = tk.Button(data_frame, text="Решить", font=("Arial", 14),
                      bg=COLOR_WHITE, fg=COLOR_BLACK, command=process,
                      activebackground=COLOR_WHITE, activeforeground=COLOR_BLACK)

states_num_label.place(x=0, y=DATA_HEIGHT * 0 // ROWS, width=DATA_WIDTH,
                  height=DATA_HEIGHT // ROWS)

states_num_entry.place(x=0, y=DATA_HEIGHT * 1 // ROWS, width=DATA_WIDTH,
                  height=DATA_HEIGHT // ROWS)

states_num_button.place(x=0, y=DATA_HEIGHT * 2 // ROWS, width=DATA_WIDTH,
                  height=DATA_HEIGHT // ROWS)

eps_label.place(x=0, y=DATA_HEIGHT * 3 // ROWS, width=DATA_WIDTH,
                  height=DATA_HEIGHT // ROWS)

eps_entry.place(x=0, y=DATA_HEIGHT * 4 // ROWS, width=DATA_WIDTH,
                  height=DATA_HEIGHT // ROWS)

step_label.place(x=0, y=DATA_HEIGHT * 5 // ROWS, width=DATA_WIDTH,
                  height=DATA_HEIGHT // ROWS)

step_entry.place(x=0, y=DATA_HEIGHT * 6 // ROWS, width=DATA_WIDTH,
                  height=DATA_HEIGHT // ROWS)

lambda_limit_label.place(x=0, y=DATA_HEIGHT * 7 // ROWS, width=DATA_WIDTH,
                  height=DATA_HEIGHT // ROWS)

lambda_limit_entry.place(x=0, y=DATA_HEIGHT * 8 // ROWS, width=DATA_WIDTH,
                  height=DATA_HEIGHT // ROWS)

lambda_gen_button.place(x=0, y=DATA_HEIGHT * 9 // ROWS, width=DATA_WIDTH,
                  height=DATA_HEIGHT // ROWS)

solve_button.place(x=0, y=DATA_HEIGHT * 10 // ROWS, width=DATA_WIDTH,
                  height=DATA_HEIGHT // ROWS)

initial_conditions_label.place(x=0, y=DATA_HEIGHT * 0 // MATRIX_FRAME_ROWS, width=MATRIX_WIDTH,
                  height=DATA_HEIGHT // MATRIX_FRAME_ROWS)

matrix_label.place(x=0, y=DATA_HEIGHT * 2 // MATRIX_FRAME_ROWS, width=MATRIX_WIDTH,
                  height=DATA_HEIGHT // MATRIX_FRAME_ROWS)

probabilities_label.place(x=0, y=DATA_HEIGHT * 13 // MATRIX_FRAME_ROWS, width=MATRIX_WIDTH,
                  height=DATA_HEIGHT // MATRIX_FRAME_ROWS)

times_label.place(x=0, y=DATA_HEIGHT * 15 // MATRIX_FRAME_ROWS, width=MATRIX_WIDTH,
                  height=DATA_HEIGHT // MATRIX_FRAME_ROWS)

root.mainloop()
