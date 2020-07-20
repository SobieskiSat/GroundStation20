import time
import random
from serial import Serial

class TimeTest:
    def __init__(self):
        pass

    def start(self):
        self.start_time = time.time()
        return self
    def stop(self):
        print(time.time() - self.start_time)

class RotatatioTest:
    def __init__(self):
        pass

    def loop(self):
        serial = Serial('COM7', 115920)
        while(True):
            x = random.randrange(49, 51)
            y = random.randrange(13, 20)
            serial
