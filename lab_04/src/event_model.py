from random import randint


def add_event(fel: list, event: list):
    i = 0
    while i < len(fel) and fel[i][0] < event[0]:
        i += 1
    if 0 < i < len(fel):
        fel.insert(i - 1, event)
    else:
        fel.insert(i, event)


def event_model(generator, processor, requests_num=0, repetitions=0):
    processed_requests = 0
    curr_queue_len = max_queue_len = 0
    fel = [[generator.generate(), 'generate']] # Future events list
    free = True
    process_flag = False

    while processed_requests < requests_num:
        event = fel.pop(0)

        # Генератор
        if event[1] == 'generate':
            curr_queue_len += 1
            if curr_queue_len > max_queue_len:
                max_queue_len = curr_queue_len
            add_event(fel, [event[0] + generator.generate(), 'generate'])
            if free:
                process_flag = True
        elif event[1] == 'process': # Обслуживающий аппарат
            processed_requests += 1
            if randint(1, 100) <= repetitions:
                curr_queue_len += 1
            process_flag = True

        if process_flag:
            if curr_queue_len > 0:
                curr_queue_len -= 1
                add_event(fel, [event[0] + processor.generate(), 'process'])
                free = False
            else:
                free = True
            process_flag = False

    return max_queue_len
