import distributions as db
import tkinter
import tkinter.messagebox as mb
import step_model as sm
import event_model as em


def init_entries():
    uniform_a_box.delete(0, 'end')
    uniform_a_box.insert(0, '1')

    uniform_b_box.delete(0, 'end')
    uniform_b_box.insert(0, '10')

    erlang_shape_entry.delete(0, 'end')
    erlang_shape_entry.insert(0, '7')

    erlang_rate_entry.delete(0, 'end')
    erlang_rate_entry.insert(0, '2.0')

    requests_num_box.delete(0, 'end')
    requests_num_box.insert(0, '1000')
    
    repetitios_box.delete(0, 'end')
    repetitios_box.insert(0, '100')

    step_box.delete(0, 'end')
    step_box.insert(0, '0.01')


def start_modelling():
    try:
        a = float(uniform_a_box.get())
        b = float(uniform_b_box.get())
        generator = db.Uniform(a, b)
    except ValueError:
        mb.showerror(title="Ошибка!", message="Некорректно заданы параметры равномерного распределения.")
        return

    if a < 0 or b < 0:
        mb.showerror(title="Ошибка!", message="Параметры должны быть положительными числами.")
        return

    if a >= b:
        mb.showerror(title="Ошибка!", message="Левая граница должна быть меньше правой.")
        return

    try:
        shape = int(erlang_shape_entry.get())
        scale = float(erlang_rate_entry.get())
        processor = db.Erlang(shape, scale)
    except ValueError:
        mb.showerror(title="Ошибка!", message="Некорректно заданы параметры распределения Эрланга.")
        return

    if shape < 0 or scale < 0:
        mb.showerror(title="Ошибка!", message="Параметры должны быть положительными числами.")
        return

    try:
        total_tasks = int(requests_num_box.get())
        repetitions = int(repetitios_box.get())
        step = float(step_box.get())
    except ValueError:
        mb.showerror(title="Ошибка!", message="Некорректно заданы параметры очереди.")
        return

    if total_tasks < 0 or step < 0:
        mb.showerror(title="Ошибка!", message="Параметры должны быть положительными числами.")
        return

    if 100 < repetitions or repetitions < 0:
        mb.showerror(title="Ошибка!", message="Процент должен быть числом от 0 до 100.")
        return

    delta_t_max_queue_len_entry.delete(0, 'end') 
    delta_t_max_queue_len_entry.insert(0, str(sm.step_model(generator, processor, total_tasks, repetitions, step)))   
    
    event_max_queue_len_entry.delete(0, 'end')
    event_max_queue_len_entry.insert(0, str(em.event_model(generator, processor, total_tasks, repetitions)))


root = tkinter.Tk()
root.title('Лабораторная работа №4')
root.geometry('1000x600+0+0')

uniform_label = tkinter.Label(text='Параметры генератора\n(равномерное распределение)', font=('Arial', 13))
uniform_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

uniform_a_label = tkinter.Label(text='Левая граница', font=('Arial', 13))
uniform_a_label.grid(row=1, column=0, padx=10, pady=10)

uniform_a_box = tkinter.Entry(font=('Arial', 13))
uniform_a_box.grid(row=1, column=1, padx=10, pady=10)

uniform_b_label = tkinter.Label(text='Правая граница', font=('Arial', 13))
uniform_b_label.grid(row=2, column=0, padx=10, pady=10)

uniform_b_box = tkinter.Entry(font=('Arial', 13))
uniform_b_box.grid(row=2, column=1, padx=10, pady=10)

erlang_label = tkinter.Label(text='Параметры обслуживающего аппарата\n(распределение Эрланга)', font=('Arial', 13))
erlang_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

erlang_shape_label = tkinter.Label(text='Форма', font=('Arial', 13))
erlang_shape_label.grid(row=4, column=0, padx=10, pady=10)

erlang_shape_entry = tkinter.Entry(font=('Arial', 13))
erlang_shape_entry.grid(row=4, column=1, padx=10, pady=10)

erlang_rate_label = tkinter.Label(text='Интенсивность', font=('Arial', 13))
erlang_rate_label.grid(row=5, column=0, padx=10, pady=10)

erlang_rate_entry = tkinter.Entry(font=('Arial', 13))
erlang_rate_entry.grid(row=5, column=1, padx=10, pady=10)

erlang_label = tkinter.Label(text='Параметры очереди', font=('Arial', 13))
erlang_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

requests_num_label = tkinter.Label(text='Количество заявок', font=('Arial', 13))
requests_num_label.grid(row=7, column=0, padx=10, pady=10)

requests_num_box = tkinter.Entry(font=('Arial', 13))
requests_num_box.grid(row=7, column=1, padx=10, pady=10)

repetitios_label = tkinter.Label(text='Процент повторяющихся заявок', font=('Arial', 13))
repetitios_label.grid(row=8, column=0, padx=10, pady=10)

repetitios_box = tkinter.Entry(font=('Arial', 13))
repetitios_box.grid(row=8, column=1, padx=10, pady=10)

step_label = tkinter.Label(text='Шаг', font=('Arial', 13))
step_label.grid(row=9, column=0, padx=10, pady=10)

step_box = tkinter.Entry(font=('Arial', 13))
step_box.grid(row=9, column=1, padx=10, pady=10)

model_button = tkinter.Button(text='Начальные параметры', font=('Arial', 13), 
    command=init_entries, width=30)
model_button.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

model_button = tkinter.Button(text='Моделировать', font=('Arial', 13), 
    command=start_modelling, width=30)
model_button.grid(row=11, column=0, columnspan=2, padx=10, pady=10)

result_label = tkinter.Label(text='Результаты', font=('Arial', 13))
result_label.grid(row=0, column=2, columnspan=2, padx=30, pady=10)

delta_t_method_label = tkinter.Label(text='Принцип Δt', font=('Arial', 13))
delta_t_method_label.grid(row=1, column=2, columnspan=2, padx=30, pady=10)

delta_t_max_queue_len_label = tkinter.Label(text='Длина очереди', font=('Arial', 13))
delta_t_max_queue_len_label.grid(row=2, column=2, padx=30, pady=10)

delta_t_max_queue_len_entry = tkinter.Entry(font=('Arial', 13))
delta_t_max_queue_len_entry.grid(row=2, column=3, padx=10, pady=10)

event_method_label = tkinter.Label(text='Событийный принцип', font=('Arial', 13))
event_method_label.grid(row=4, column=2, columnspan=2, padx=30, pady=10)

event_max_queue_len_label = tkinter.Label(text='Длина очереди', font=('Arial', 13))
event_max_queue_len_label.grid(row=5, column=2, padx=30, pady=10)

event_max_queue_len_entry = tkinter.Entry(font=('Arial', 13))
event_max_queue_len_entry.grid(row=5, column=3, padx=10, pady=10)

root.mainloop()
