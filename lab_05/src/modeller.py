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

        generator.time = generator.generate_time()
        # self.operators[0].time = self.operators[0].generate_time()

        blocks = [
            generator,
            self.operators[0],
            self.operators[1],
            self.operators[2],
            self.computers[0],
            self.computers[1],
        ]

        while generator.requests_num > 0:
            current_time = generator.time

            for block in blocks:
                if 0 < block.time < current_time:
                    current_time = block.time

            for block in blocks:
                if abs(current_time - block.time) <= 1e-3:
                    if not isinstance(block, processor.Processor):
                        operator = generator.generate_request()
                        if operator is not None:
                            operator.time = current_time + operator.generate_time()
                            processed_requests += 1
                        else:
                            denials_num += 1
                        generator.time = current_time + generator.generate_time()
                    else:
                        block.process_request()
                        if block.curr_queue_len == 0:
                            block.time = 0
                        else:
                            block.time = current_time + block.generate_time()

        return denials_num, processed_requests, current_time
