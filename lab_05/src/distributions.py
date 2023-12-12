import numpy as np
import numpy.random as nr


class Uniform:
    def __init__(self, a: float, b: float):
        self.a = a
        self.b = b

    def generate(self) -> float:
        return self.a + (self.b - self.a) * nr.uniform(0, 1)
    

class Normal:
    def __init__(self, mu: float, sigma: float):
        self.mu = mu
        self.sigma = sigma

    def generate(self) -> float:
        return nr.normal(self.mu, self.sigma)
