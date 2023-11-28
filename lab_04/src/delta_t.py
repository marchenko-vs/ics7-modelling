import random


def delta_t(generator, processor, requests_num=0, repetitions=0, step=0.001):
    processed_requests = 0
    t_curr = step
    t_gen = generator.generate()
    t_gen_prev = t_proc = 0
    curr_queue_len = max_queue_len = 0
    free = True

    while processed_requests < requests_num:
        if t_curr > t_gen:
            curr_queue_len += 1

            if curr_queue_len > max_queue_len:
                max_queue_len = curr_queue_len
            
            t_gen_prev = t_gen
            t_gen += generator.generate()

        if t_curr > t_proc:
            if curr_queue_len > 0:
                was_free = free
                if free:
                    free = False
                else:
                    processed_requests += 1
                    if random.randint(1, 100) <= repetitions:
                        curr_queue_len += 1
                curr_queue_len -= 1
                if was_free:
                    t_proc = t_gen_prev + processor.generate()
                else:
                    t_proc += processor.generate()
            else:
                free = True
        t_curr += step

    return max_queue_len
