import tkinter
import tkinter.messagebox as mb
import modeller
import generator as gen
import distributions
import processor
import computer


def init_entries():
    generator_time_box.delete(0, 'end')
    generator_time_box.insert(0, '10')
    generator_error_box.delete(0, 'end')
    generator_error_box.insert(0, '2')

    operator_1_time_box.delete(0, 'end')
    operator_1_time_box.insert(0, '20')
    operator_1_error_box.delete(0, 'end')
    operator_1_error_box.insert(0, '5')

    operator_2_time_box.delete(0, 'end')
    operator_2_time_box.insert(0, '40')
    operator_2_error_box.delete(0, 'end')
    operator_2_error_box.insert(0, '10')

    operator_3_time_box.delete(0, 'end')
    operator_3_time_box.insert(0, '40')
    operator_3_error_box.delete(0, 'end')
    operator_3_error_box.insert(0, '20')

    pc_1_time_box.delete(0, 'end')
    pc_1_time_box.insert(0, '15')
    pc_1_error_box.delete(0, 'end')
    pc_1_error_box.insert(0, '0')

    pc_2_time_box.delete(0, 'end')
    pc_2_time_box.insert(0, '30')
    pc_2_error_box.delete(0, 'end')
    pc_2_error_box.insert(0, '0')

    requests_num_box.delete(0, 'end')
    requests_num_box.insert(0, '300')


def start_modelling():
    try:
        generator_time = int(generator_time_box.get())
        generator_error = int(generator_error_box.get())
    except ValueError:
        mb.showerror(title="Ошибка!", message="Некорректно заданы параметры равномерного распределения.")
        return

    try:
        operator_1_time = int(operator_1_time_box.get())
        operator_1_error = int(operator_1_error_box.get())
    except ValueError:
        mb.showerror(title="Ошибка!", message="Некорректно заданы параметры работы первого оператора.")
        return

    try:
        operator_2_time = int(operator_2_time_box.get())
        operator_2_error = int(operator_2_error_box.get())
    except ValueError:
        mb.showerror(title="Ошибка!", message="Некорректно заданы параметры работы второго оператора.")
        return

    try:
        operator_3_time = int(operator_3_time_box.get())
        operator_3_error = int(operator_3_error_box.get())
    except ValueError:
        mb.showerror(title="Ошибка!", message="Некорректно заданы параметры работы третьего оператора.")
        return

    try:
        pc_1_time = int(pc_1_time_box.get())
        pc_1_error = int(pc_1_error_box.get())
    except ValueError:
        mb.showerror(title="Ошибка!", message="Некорректно задано время обработки первым компьютером.")
        return

    try:
        pc_2_time = int(pc_2_time_box.get())
        pc_2_error = int(pc_2_error_box.get())
    except ValueError:
        mb.showerror(title="Ошибка!", message="Некорректно задано время обработки вторым компьютером.")
        return

    try:
        requests_num = int(requests_num_box.get())
    except ValueError:
        mb.showerror(title="Ошибка!", message="Некорректно задано количество заявок.")
        return

    generator = gen.Generator(distributions.Uniform(generator_time - generator_error, 
        generator_time + generator_error), requests_num)

    operators = [
        processor.Processor(
            distributions.Uniform(operator_1_time - operator_1_error, 
                                              operator_1_time + operator_1_error),
            max_queue_len=1
        ),
        processor.Processor(
            distributions.Uniform(operator_2_time - operator_2_error, 
                                              operator_2_time + operator_2_error),
            max_queue_len=1
        ),
        processor.Processor(
            distributions.Uniform(operator_3_time - operator_3_error, 
                                              operator_3_time + operator_3_error),
            max_queue_len=1
        ),
    ]

    computers = [
        computer.Computer(distributions.Uniform(pc_1_time - pc_1_error, pc_1_time + pc_1_error)),
        computer.Computer(distributions.Uniform(pc_2_time - pc_2_error, pc_2_time + pc_2_error)),
    ]

    model = modeller.Modeller(generator, operators, computers)
    result = model.event_mode()

    denial_num_box.delete(0, 'end') 
    denial_num_box.insert(0, str(result[0])) 

    denial_percentage_box.delete(0, 'end') 
    denial_percentage_box.insert(0, '{:.2f}%'.format(100 * (result[0] / (result[0] + result[1]))))

    queue_len_1_box.delete(0, 'end') 
    queue_len_1_box.insert(0, str(result[3]))

    queue_len_2_box.delete(0, 'end') 
    queue_len_2_box.insert(4, str(result[4]))


root = tkinter.Tk()
root.title('Лабораторная работа №5')
root.geometry('900x700+0+0')

generator_label = tkinter.Label(text='Параметры генератора', font=('Arial', 13))
generator_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

generator_time_label = tkinter.Label(text='Интервал поступления заявок', font=('Arial', 13))
generator_time_label.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
generator_time_box = tkinter.Entry(font=('Arial', 13), justify='center')
generator_time_box.grid(row=2, column=0, padx=10, pady=10)
generator_error_label = tkinter.Label(text='±', font=('Arial', 13))
generator_error_label.grid(row=2, column=1, padx=10, pady=10)
generator_error_box = tkinter.Entry(font=('Arial', 13), justify='center')
generator_error_box.grid(row=2, column=2, padx=10, pady=10)

operators_label = tkinter.Label(text='Параметры операторов', font=('Arial', 13))
operators_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

operator_1_time_label = tkinter.Label(text='Время обработки первым оператором', font=('Arial', 13))
operator_1_time_label.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
operator_1_time_box = tkinter.Entry(font=('Arial', 13), justify='center')
operator_1_time_box.grid(row=5, column=0, padx=10, pady=10)
operator_1_error_label = tkinter.Label(text='±', font=('Arial', 13))
operator_1_error_label.grid(row=5, column=1, padx=10, pady=10)
operator_1_error_box = tkinter.Entry(font=('Arial', 13), justify='center')
operator_1_error_box.grid(row=5, column=2, padx=10, pady=10)

operator_2_time_label = tkinter.Label(text='Время обработки вторым оператором', font=('Arial', 13))
operator_2_time_label.grid(row=6, column=0, columnspan=3, padx=10, pady=10)
operator_2_time_box = tkinter.Entry(font=('Arial', 13), justify='center')
operator_2_time_box.grid(row=7, column=0, padx=10, pady=10)
operator_2_error_label = tkinter.Label(text='±', font=('Arial', 13))
operator_2_error_label.grid(row=7, column=1, padx=10, pady=10)
operator_2_error_box = tkinter.Entry(font=('Arial', 13), justify='center')
operator_2_error_box.grid(row=7, column=2, padx=10, pady=10)

operator_3_time_label = tkinter.Label(text='Время обработки третьим оператором', font=('Arial', 13))
operator_3_time_label.grid(row=8, column=0, columnspan=3, padx=10, pady=10)
operator_3_time_box = tkinter.Entry(font=('Arial', 13), justify='center')
operator_3_time_box.grid(row=9, column=0, padx=10, pady=10)
operator_3_error_label = tkinter.Label(text='±', font=('Arial', 13))
operator_3_error_label.grid(row=9, column=1, padx=10, pady=10)
operator_3_error_box = tkinter.Entry(font=('Arial', 13), justify='center')
operator_3_error_box.grid(row=9, column=2, padx=10, pady=10)

pcs_label = tkinter.Label(text='Параметры компьютеров', font=('Arial', 13))
pcs_label.grid(row=10, column=0, columnspan=3, padx=10, pady=10)

pc_1_time_label = tkinter.Label(text='Время обработки первым компьютером', font=('Arial', 13))
pc_1_time_label.grid(row=11, column=0, columnspan=3, padx=10, pady=10)
pc_1_time_box = tkinter.Entry(font=('Arial', 13), justify='center')
pc_1_time_box.grid(row=12, column=0, padx=10, pady=10)
pc_1_error_label = tkinter.Label(text='±', font=('Arial', 13))
pc_1_error_label.grid(row=12, column=1, padx=10, pady=10)
pc_1_error_box = tkinter.Entry(font=('Arial', 13), justify='center')
pc_1_error_box.grid(row=12, column=2, padx=10, pady=10)

pc_2_time_label = tkinter.Label(text='Время обработки вторым компьютером', font=('Arial', 13))
pc_2_time_label.grid(row=13, column=0, columnspan=3, padx=10, pady=10)
pc_2_time_box = tkinter.Entry(font=('Arial', 13), justify='center')
pc_2_time_box.grid(row=14, column=0, padx=10, pady=10)
pc_2_error_label = tkinter.Label(text='±', font=('Arial', 13))
pc_2_error_label.grid(row=14, column=1, padx=10, pady=10)
pc_2_error_box = tkinter.Entry(font=('Arial', 13), justify='center')
pc_2_error_box.grid(row=14, column=2, padx=10, pady=10)

modelling_label = tkinter.Label(text='Параметры моделирования', font=('Arial', 13))
modelling_label.grid(row=0, column=3, padx=100, pady=10)

requests_num_label = tkinter.Label(text='Количество заявок', font=('Arial', 13))
requests_num_label.grid(row=1, column=3, padx=100, pady=10)
requests_num_box = tkinter.Entry(font=('Arial', 13), justify='center')
requests_num_box.grid(row=2, column=3, padx=100, pady=10)

results_label = tkinter.Label(text='Результат моделирования', font=('Arial', 13))
results_label.grid(row=4, column=3, padx=100, pady=10)

denial_num_label = tkinter.Label(text='Количество отказов', font=('Arial', 13))
denial_num_label.grid(row=5, column=3, padx=100, pady=10)
denial_num_box = tkinter.Entry(font=('Arial', 13), justify='center')
denial_num_box.grid(row=6, column=3, padx=100, pady=10)

denial_percentage_label = tkinter.Label(text='Вероятность отказа', font=('Arial', 13))
denial_percentage_label.grid(row=7, column=3, padx=100, pady=10)
denial_percentage_box = tkinter.Entry(font=('Arial', 13), justify='center')
denial_percentage_box.grid(row=8, column=3, padx=100, pady=10)

queue_len_1_label = tkinter.Label(text='Оптимальная длина первого накопителя', font=('Arial', 13))
queue_len_1_label.grid(row=9, column=3, padx=100, pady=10)
queue_len_1_box = tkinter.Entry(font=('Arial', 13), justify='center')
queue_len_1_box.grid(row=10, column=3, padx=100, pady=10)

queue_len_2_label = tkinter.Label(text='Оптимальная длина второго накопителя', font=('Arial', 13))
queue_len_2_label.grid(row=11, column=3, padx=100, pady=10)
queue_len_2_box = tkinter.Entry(font=('Arial', 13), justify='center')
queue_len_2_box.grid(row=12, column=3, padx=100, pady=10)

modelling_button = tkinter.Button(text='Начальные значения', font=('Arial', 13), 
                                  width=20, command=init_entries)
modelling_button.grid(row=13, column=3, padx=100, pady=10)

modelling_button = tkinter.Button(text='Моделировать', font=('Arial', 13), 
                                  width=20, command=start_modelling)
modelling_button.grid(row=14, column=3, padx=100, pady=10)

init_entries()

root.mainloop()
