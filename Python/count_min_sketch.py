import hashlib
import numpy as np
from collections import defaultdict


class CountMinSketch:
    def __init__(self, rows, cols, window_size):
        self.rows = rows
        self.cols = cols
        self.window_size = window_size

        # 初始化计数矩阵
        self.table = np.zeros((rows, cols), dtype=int)

        # 用于存储 key -> last updated value
        self.keys = defaultdict(int)

        # 存储结果 (time_stamp, value)
        self.result = defaultdict(list)

        # 当前窗口起始时间
        self.window_start = None

        # 哈希函数种子
        self.seeds = [i * 1315423911 for i in range(rows)]

    def _hash(self, key, seed):
        """使用不同的seed生成不同哈希值"""
        h = hashlib.md5((str(key) + str(seed)).encode()).hexdigest()
        return int(h, 16) % self.cols

    def _estimate(self, key):
        """从CMS中估计key的频率"""
        return min(self.table[i][self._hash(key, self.seeds[i])] for i in range(self.rows))

    def process(self, key, byte_count, time_stamp):
        # 初始化窗口起点
        if self.window_start is None:
            self.window_start = time_stamp

        # 检查是否超出窗口
        if time_stamp - self.window_start >= self.window_size:
            # 输出当前窗口的统计结果
            for k in self.keys:
                est = self._estimate(k)
                self.result[k].append((self.window_start, est))

            # 清空窗口
            self.table.fill(0)
            self.keys.clear()
            self.window_start = time_stamp

        # 更新CMS
        for i in range(self.rows):
            idx = self._hash(key, self.seeds[i])
            self.table[i][idx] += byte_count

        # 更新字典
        self.keys[key] += byte_count
