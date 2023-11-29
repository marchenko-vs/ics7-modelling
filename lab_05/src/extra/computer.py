class Computer:
    def __init__(self, randomizer):
        self.randomizer = randomizer
        self.max_queue_len = 0
        self.curr_queue_len = 0
        self.processed_requests = 0
        self.received_requests = 0
        self.time = 0

    def process_request(self):
        if self.curr_queue_len > 0:
            self.processed_requests += 1
            self.curr_queue_len -= 1
    
    def receive_request(self):
        self.curr_queue_len += 1
        self.received_requests += 1

        if self.max_queue_len < self.curr_queue_len:
            self.max_queue_len += 1

    def generate_time(self):
        return self.randomizer.generate()
    