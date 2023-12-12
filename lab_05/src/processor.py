import generator as gen


class Processor(gen.Generator):
    def __init__(self, randomizer, max_queue_len=-1):
        self.randomizer = randomizer
        self.max_queue_len = max_queue_len
        self.curr_queue_len = 0
        self.processed_requests = 0
        self.received_requests = 0
        self.time = 0

    def process_request(self):
        if self.curr_queue_len > 0:
            self.processed_requests += 1
            self.curr_queue_len -= 1
    
    def receive_request(self):
        if self.max_queue_len == -1 or self.max_queue_len > self.curr_queue_len:
            self.curr_queue_len += 1
            self.received_requests += 1

            return True
        
        return False
    