__author__ = 'rohanraja'

import time

class Timer:
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start

    def __str__(self):
        return str(self.interval)