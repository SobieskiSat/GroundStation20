import time

class TimeTest:
    def __init__(self):
        pass

    def start(self):
        self.start_time = time.time()
        return self
    def stop(self):
        print(time.time() - self.start_time)
