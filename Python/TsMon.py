import mmh3
import numpy as np
from sympy import print_rcode
from collections import defaultdict

SKETCH_ROWS = 3
SKETCH_COLUMNS = 1024
QUEUE_ROWS = 1024
QUEUE_COLUMNS = 8


class SketchBucket:
    def __init__(self):
        self.short_time_stamp = 0
        self.full_time_stamp = 0
        self.counter = 0


class SketchRow:
    def __init__(self, d, seed):
        self.bucket = [SketchBucket() for _ in range(d)]
        self.seed = seed
        self.d = d

    def hash_func(self, value):
        return mmh3.hash(str(value), self.seed, signed=False) % SKETCH_COLUMNS

    def update_timestamp(self, key, global_time, windowSize):
        short_time = global_time_to_short(global_time, windowSize)
        index = self.hash_func(key)
        return_flag = False
        return_time = 0
        if short_time - self.bucket[index].short_time_stamp != 0:  # This means that beyond the previous window
            return_flag = True
            return_time = self.bucket[index].full_time_stamp

            self.bucket[index].full_time_stamp = global_time
            self.bucket[index].short_time_stamp = short_time
        return return_flag, return_time

    def update_counter(self, key, p_bytes):
        '''
        :param key:
        :param p_bytes:
        :return: 还没有累加的历史值
        '''
        index = self.hash_func(key)
        return_value = self.bucket[index].counter
        # here we count the number of packets
        self.bucket[index].counter += p_bytes
        return return_value

    def query_counter(self, key):
        index = self.hash_func(key)
        return_value = self.bucket[index].counter
        return return_value


    def deletion_counter(self, key, value):
        index = self.hash_func(key)
        self.bucket[index].counter -= value

    def reinitialize(self):
        self.__init__(self.d, self.seed)


class TsSketch:
    def __init__(self, w, d):
        self.row = [SketchRow(d, i) for i in range(w)]
        self.rows = w
        self.columns = d

    def process(self, key, global_time, p_bytes, windowSize):
        # Processing the time stamp first, get update flag
        update_flags = False
        for i in range(self.rows):
            update_flag, return_time = self.row[i].update_timestamp(key, global_time, windowSize)
            update_flags = update_flags or update_flag

        min_value = 0x7fffffff
        for i in range(self.rows):
            min_value = min(min_value, self.row[i].update_counter(key, p_bytes))

        if update_flags:  # Beyond the precious window
            for i in range(self.rows):
                self.row[i].deletion_counter(key, min_value)
            return min_value, return_time
        return None, None

    def reinitialize(self):
        for i in range(self.rows):
            self.row[i].reinitialize()


class QueueRow:
    def __init__(self, d):
        self.d = d
        self.bucket = [0 for _ in range(d)]
        self.flowKey = 0
        self.last_time = 0  # 先不管那么多内存方面的问题了

    def insert_data(self, value, pos, key, full_time):
        self.bucket[pos] = value
        self.flowKey = key
        self.last_time = full_time

    def query(self):
        return self.bucket

    def reinitialize(self):
        self.__init__(self.d)


class TsQueue:
    def __init__(self, w, d):
        self.row = [QueueRow(d) for _ in range(w)]
        self.w = w
        self.d = d

    def insert(self, key, value, pos, full_time):
        index = mmh3.hash(str(key)) % QUEUE_ROWS
        self.row[index].insert_data(value, pos, key, full_time)  # TODO

    def query(self, key):
        index = mmh3.hash(str(key)) % QUEUE_ROWS
        return self.row[index].query()

    def query_key(self, key):
        index = mmh3.hash(str(key)) % QUEUE_ROWS
        return self.row[index].flowKey

    def query_last_time(self, key):
        index = mmh3.hash(str(key)) % QUEUE_ROWS
        return self.row[index].last_time

    def reinitialize(self):
        for i in range(self.w):
            self.row[i].reinitialize()

    def reinitialize_one_line(self, i):
        index = mmh3.hash(str(i)) % QUEUE_ROWS
        self.row[index].reinitialize()


def global_time_to_short(global_time, window_size):
    return (global_time // window_size) & (QUEUE_COLUMNS - 1)


class TsMon:
    def __init__(self, sketch_rows, sketch_columns, queue_rows, queue_columns, window_size):
        global SKETCH_ROWS
        SKETCH_ROWS = sketch_rows
        global SKETCH_COLUMNS
        SKETCH_COLUMNS = sketch_columns
        global QUEUE_ROWS
        QUEUE_ROWS = queue_rows
        global QUEUE_COLUMNS
        QUEUE_COLUMNS = queue_columns

        self.sketch = TsSketch(sketch_rows, sketch_columns)
        self.queue = TsQueue(queue_rows, queue_columns)
        self.global_time_stamp = 0

        '''
        DEPRECATED
        '''
        # self.last_update = [0 for x in range(100000)]
        #
        # self.plt_values = []
        # self.re_values = []
        # self.ano_values = []
        self.window_size = window_size

        '''
        请使用下面的replay数据结构
        '''
        self.replay = defaultdict(list)


        '''
        DEPRECATED
        '''
        # self.ano_info = ano_info
        # self.TP = 0
        # self.TN = 0
        # self.FP = 0
        # self.FN = 0
        #
        # self.cms_value = defaultdict(list)

        '''
        TsSketch_test 保存的流量曲线
        '''
        self.traffic = defaultdict(list)

    def TsSketch_test(self, key, p_bytes, global_time):
        value, _ = self.sketch.process(key, global_time, p_bytes, self.window_size)
        if value is not None and value != 0:
            self.traffic[key].append((global_time, value))






    def process(self, key, p_bytes, global_time):
        self.global_time_stamp = global_time
        value, insert_time_stamp = self.sketch.process(key, global_time, p_bytes, self.window_size)
        if value is not None:

            # self.cms_value[key].append(value)

            '''
            Reconstruction
            
            logic tree:
                same flow key
                |
                |___exceed window       --> update
                |___not exceed window   --> just insert data
                
                not same flow key
                |
                |___exceed window       |
                |___not exceed window   --> eject exist data and import new volume
            '''
            queue_key = self.queue.query_key(key)
            queue_time = self.queue.query_last_time(key)
            replay_time_stamp = (queue_time // (self.window_size * QUEUE_COLUMNS) + 1) * (self.window_size * QUEUE_COLUMNS)  # 针对某个流键, 当前队列的截止时间戳
            if queue_key != key:
                # 如果队列流键和当前数据包流键不相同, 说明当前队列的时间戳是无效的, 直接弹出当前队列数据
                for i, x in enumerate(list(self.queue.query(queue_key))):
                    if x == 0: continue
                    self.replay[queue_key].append(((replay_time_stamp - (QUEUE_COLUMNS - i) * self.window_size) // self.window_size * self.window_size, x))
                self.queue.reinitialize_one_line(queue_key)

            else:
                # 相同流键, 因此按正常流程进行窗口判断
                if global_time // (self.window_size * QUEUE_COLUMNS) - insert_time_stamp // (self.window_size * QUEUE_COLUMNS) > 0:
                    for i, x in enumerate(list(self.queue.query(key))):
                        if x == 0: continue
                        self.replay[key].append(((replay_time_stamp - (QUEUE_COLUMNS - i) * self.window_size) // self.window_size * self.window_size, x))
                    self.queue.reinitialize_one_line(key)

            self.queue.insert(key, value, global_time_to_short(global_time, self.window_size), self.global_time_stamp)  # 如果global_time_to_short里面是global_time 而不是 insert_time_stamp, 问题可以解决,但是时间戳有点错位

            '''
            Anomaly detection - t_sigma sliding window  ***DEPRECATED***
            '''
            # min_value, max_value, mean, sigma = t_sigma(self.queue.query(key))
            # flag = 0
            # for time in self.ano_info[key]:
            #     if self.global_time_stamp - (QUEUE_COLUMNS + 1) * self.window_size <= time <= self.global_time_stamp:
            #         # print('T', flag, key, min_value, max_value, mean - self.n_sigma * sigma, mean + self.n_sigma * sigma, '\n',
            #         #       [x for x in self.queue.query(key) if x != 0], end='\n\n')
            #         flag = 1
            #         break
            # # if len(self.ano_info[key]) != 0:
            # #     flag = 1
            #
            # if min_value < mean - self.n_sigma * sigma - norm_base or max_value > mean + self.n_sigma * sigma + norm_base:
            #     # print('P', flag, key, min_value, max_value, mean - self.n_sigma * sigma - norm_base, mean + self.n_sigma * sigma + norm_base,
            #     #       mean, sigma, '\n',
            #     #       [x for x in self.queue.query(key) if x != 0], end='\n\n')
            #     if flag == 1:  # hit
            #         self.TP += 1
            #     else:
            #         self.FP += 1
            # else:
            #     # print('N', flag, key, min_value, max_value, mean - self.n_sigma * sigma, mean + self.n_sigma * sigma,
            #     #       mean, sigma,
            #     #       '\n',
            #     #       [x for x in self.queue.query(key) if x != 0], '\n', self.global_time_stamp, end='\n\n')
            #     if flag == 1:  # hit
            #         self.FN += 1
            #     else:
            #         self.TN += 1

    def popout(self, key):
        return self.queue.query(key)

    def popout_residual_data(self, flowNum):
        for queue in self.queue.row:
            for num in queue.bucket:
                if num == 0: continue
                self.replay[queue.flowKey].append((self.global_time_stamp, num))

        '''
        本来想把Sketch中剩余数据全部吐出来, 发现误差特别大, 还是算了
        '''

        # for id in range(1, flowNum):
        #     value = 0x7fffffff
        #     for i in range(SKETCH_ROWS):
        #         value = min(value, self.sketch.row[i].query_counter(id))
        #
        #     queue_time = self.queue.query_last_time(id)
        #     if id == 14909:
        #         print(queue_time)
        #     replay_time_stamp = (queue_time // (self.window_size * QUEUE_COLUMNS) + 1) * (self.window_size * QUEUE_COLUMNS)
        #     self.replay[id].append((replay_time_stamp, value))


# def t_sigma(values):
#     values = [x for x in values if x != 0]
#     # print(len(values))
#
#     max_value = np.max(values)
#     min_value = np.min(values)
#
#     if len(values) > 2:
#         mean = (np.sum(values) - max_value - min_value) / (len(values) - 2)
#     else:
#         mean = np.sum(values) / len(values)
#     sigma = np.std(values)
#     return min_value, max_value, mean, sigma
