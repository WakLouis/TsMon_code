import mmh3
import numpy as np

SKETCH_ROWS = 3
SKETCH_COLUMNS = 1024
QUEUE_ROWS = 1024
QUEUE_COLUMNS = 8

class SketchBucket:
    def __init__(self):
        self.counter = 0


class SketchRow:
    def __init__(self, d, seed):
        self.bucket = [SketchBucket() for _ in range(d)]
        self.seed = seed
        self.d = d

    def hash_func(self, value):
        return mmh3.hash(str(value), self.seed) % SKETCH_COLUMNS


    def update_counter(self, key):
        index = self.hash_func(key)
        # here we count the number of packets
        self.bucket[index].counter += 1
        return self.bucket[index].counter

class Sketch:
    def __init__(self, w, d):
        self.row = [SketchRow(d, i) for i in range(w)]
        self.rows = w
        self.columns = d

    def process(self, key, global_time):


        min_value = 0x7fffffff
        for i in range(self.rows):
            min_value = min(min_value, self.row[i].update_counter(key))
        min_value = min_value == 0 if 0 else min_value - 1

        if update_flags:  # Beyond the precious window
            for i in range(self.rows):
                self.row[i].deletion_counter(key, min_value)
            return min_value, return_time
        return None, None

    def reinitialize(self):
        for i in range(self.rows):
            self.row[i].reinitialize()
