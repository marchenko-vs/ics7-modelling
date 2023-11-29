class Request:
    curr_id = 0

    def __init__(self):
        self.id = Request.curr_id
        Request.curr_id += 1
