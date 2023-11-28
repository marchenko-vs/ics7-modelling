import numpy.random as npr
import math


class Uniform:
    def __init__(self, a: float, b: float):
        self.a = a
        self.b = b

    def generate(self):
        return self.a + (self.b - self.a) * npr.uniform(0, 1)


class Erlang:
    def __init__(self, shape: int, rate: float):
        self.shape = shape
        self.rate = rate

    def generate(self):
        # curr_sum = 0
        # for i in range(self.shape):
        #     curr_sum += math.log(1 - npr.uniform(0, 1))
        # return (- 1 / (self.shape * self.rate)) * curr_sum
        return npr.gamma(self.shape, 1 / self.rate)
