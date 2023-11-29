class Generator:
    def __init__(self, randomizer, requests_num):
        self.randomizer = randomizer
        self.requests_num = requests_num
        self.receivers = list()
        self.next = 0 

    def next_time(self):
        return self.randomizer.generate()
    
    def generate_request(self):
        self.requests_num -= 1
        for receiver in self.receivers:
            if receiver.receive_request():
                return receiver
        return None
