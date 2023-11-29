import tkinter
import tkinter.messagebox as mb
import modeller
import generator as gen
import distributions
import processor


UNIT_OF_TIME = 0.01


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

    pc_2_time_box.delete(0, 'end')
    pc_2_time_box.insert(0, '30')

    requests_num_box.delete(0, 'end')
    requests_num_box.insert(0, '300')


def pick_operator(operators):
    for i in range(len(operators)):
        if not operators[i].busy:
            return i
    
    return -1


def one_step(generator, operators, processors, request_info, generate_new=True):
    if generate_new:
        request = generator.upd_time(UNIT_OF_TIME)
        if request:
            #print(request.id, 'gen')
            request_info['generated'] += 1
            i_operator = pick_operator(operators)
            if i_operator == -1: # все операторы заняты
                #print(request.id, 'lost')
                request_info['lost'] += 1
            else:
                operators[i_operator].accept_request(request)

    for cur_operator in operators:
        cur_operator.upd_time(UNIT_OF_TIME)

    for cur_processor in processors:
        res = cur_processor.upd_time(UNIT_OF_TIME)
        if res == 'req fin':  # заявка была обработана
            request_info['processed'] += 1


def modelling(generator, operators, processors, total_incoming_requests):
    request_info = {'generated': 0, 'lost': 0, 'processed': 0}

    while request_info['generated'] < total_incoming_requests:
        one_step(generator, operators, processors, request_info)

    while request_info['lost'] + request_info['processed'] < total_incoming_requests:
        one_step(generator, operators, processors, request_info, False)

    return request_info


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
    except ValueError:
        mb.showerror(title="Ошибка!", message="Некорректно задано время обработки первым компьютером.")
        return

    try:
        pc_2_time = int(pc_2_time_box.get())
    except ValueError:
        mb.showerror(title="Ошибка!", message="Некорректно задано время обработки вторым компьютером.")
        return

    try:
        requests_num = int(requests_num_box.get())
    except ValueError:
        mb.showerror(title="Ошибка!", message="Некорректно задано количество заявок.")
        return
    
    first_queue = list()
    second_queue = list()

    generator = gen.Generator(distributions.Uniform(generator_time - generator_error, 
        generator_time + generator_error))

    operators = [
        modeller.Modeller(first_queue, 
            distributions.Uniform(operator_1_time - operator_1_error, 
                                              operator_1_time + operator_1_error)
        ),
        modeller.Modeller(first_queue, 
            distributions.Uniform(operator_2_time - operator_2_error, 
                                              operator_2_time + operator_2_error)
        ),
        modeller.Modeller(second_queue, 
            distributions.Uniform(operator_3_time - operator_3_error, 
                                              operator_3_time + operator_3_error)
        ),
    ]

    computers = [
        processor.Processor(first_queue, distributions.Uniform(pc_1_time, pc_1_time)),
        processor.Processor(second_queue, distributions.Uniform(pc_2_time, pc_2_time)),
    ]

    result = modelling(generator, operators, computers, requests_num)

    denial_num_box.delete(0, 'end') 
    denial_num_box.insert(0, str(result['lost'])) 

    denial_percentage_box.delete(0, 'end') 
    denial_percentage_box.insert(0, '{:.2f}%'.format(100 * (result['lost'] / (result['processed'] + result['lost']))))   


root = tkinter.Tk()
root.title('Лабораторная работа №5')
root.geometry('1000x700+0+0')

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
pc_1_time_box.grid(row=12, column=0, columnspan=3,  padx=10, pady=10)

pc_2_time_label = tkinter.Label(text='Время обработки вторым компьютером', font=('Arial', 13))
pc_2_time_label.grid(row=13, column=0, columnspan=3, padx=10, pady=10)
pc_2_time_box = tkinter.Entry(font=('Arial', 13), justify='center')
pc_2_time_box.grid(row=14, column=0, columnspan=3, padx=10, pady=10)

modelling_label = tkinter.Label(text='Параметры моделирования', font=('Arial', 13))
modelling_label.grid(row=0, column=3, padx=100, pady=10)

requests_num_label = tkinter.Label(text='Количество заявок', font=('Arial', 13))
requests_num_label.grid(row=1, column=3, padx=100, pady=10)
requests_num_box = tkinter.Entry(font=('Arial', 13))
requests_num_box.grid(row=2, column=3, padx=100, pady=10)

results_label = tkinter.Label(text='Результат моделирования', font=('Arial', 13))
results_label.grid(row=6, column=3, padx=100, pady=10)

denial_num_label = tkinter.Label(text='Количество отказов', font=('Arial', 13))
denial_num_label.grid(row=7, column=3, padx=100, pady=10)
denial_num_box = tkinter.Entry(font=('Arial', 13), justify='center')
denial_num_box.grid(row=8, column=3, padx=100, pady=10)

denial_percentage_label = tkinter.Label(text='Вероятность отказа', font=('Arial', 13))
denial_percentage_label.grid(row=9, column=3, padx=100, pady=10)
denial_percentage_box = tkinter.Entry(font=('Arial', 13), justify='center')
denial_percentage_box.grid(row=10, column=3, padx=100, pady=10)

modelling_button = tkinter.Button(text='Начальные значения', font=('Arial', 13), command=init_entries)
modelling_button.grid(row=12, column=3, padx=100, pady=10)

modelling_button = tkinter.Button(text='Моделировать', font=('Arial', 13), command=start_modelling)
modelling_button.grid(row=13, column=3, padx=100, pady=10)

init_entries()

root.mainloop()
