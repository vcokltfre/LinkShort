from time import time
from random import randint


class IDGenerator:
    def __init__(self):
        self.increment = 0

    def next(self) -> int:
        t = round(time() * 1000) - 1608000000000
        if self.increment >= 2**5:
            self.increment = 0
        else:
            self.increment += 1
        return hex((t << 5) + self.increment + randint(0, 1000000))[2:]
