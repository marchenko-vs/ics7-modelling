import processor


class Modeller:
    def __init__(self, generator, operators, computers):
        self.generator = generator
        self.operators = operators
        self.computers = computers

    def event_mode(self):
        denials_num = 0
        processed_requests = 0
        generator = self.generator

        generator.receivers = self.operators.copy()
        self.operators[0].receivers = [self.computers[0]]
        self.operators[1].receivers = [self.computers[0]]
        self.operators[2].receivers = [self.computers[1]]

        generator.next = generator.next_time()
        self.operators[0].next = self.operators[0].next_time()

        blocks = [
            generator,
            self.operators[0],
            self.operators[1],
            self.operators[2],
            self.computers[0],
            self.computers[1],
        ]

        while generator.requests_num > 0:
            current_time = generator.next
            for block in blocks:
                print(block.next)
                if 0 < block.next < current_time:
                    current_time = block.next

            for block in blocks:
                if abs(current_time - block.next) <= 1e-3:
                    if not isinstance(block, processor.Processor):
                        next_generator = generator.generate_request()
                        if next_generator is not None:
                            next_generator.next = current_time + next_generator.next_time()
                            processed_requests += 1
                        else:
                            denials_num += 1
                        generator.next = current_time + generator.next_time()
                    else:
                        block.process_request()
                        if block.curr_queue_len == 0:
                            block.next = 0
                        else:
                            block.next = current_time + block.next_time()

        return denials_num, processed_requests, current_time
