import numpy as np
from scipy import stats


class IncrementalChiSquareZipf:
    def __init__(self, categories=None, zipf_param=1.0):
        """
        初始化增量卡方检验，使用Zipf分布作为期望分布

        参数:
        categories: 可能的类别列表，如果为None则动态生成
        zipf_param: Zipf分布的参数s值，控制分布的倾斜程度，默认为1.0
        """
        self.counts = {}  # 存储各类别的计数
        self.total_count = 0  # 总样本数
        self.categories = list(categories) if categories else []
        self.category_set = set(self.categories) if categories else set()
        self.zipf_param = zipf_param
        self.expected_probs = {}
        self.counter = 0

        # 如果初始提供了categories，就计算Zipf期望概率
        if self.categories:
            self._calculate_zipf_probs()

    def _calculate_zipf_probs(self):
        """计算Zipf分布的概率"""
        n = len(self.categories)
        if n == 0:
            return

        # 计算归一化常数
        norm_const = sum(1.0 / (i ** self.zipf_param) for i in range(1, n + 1))

        # 计算每个类别的Zipf概率
        self.expected_probs = {}
        for i, cat in enumerate(sorted(self.categories)):
            # Zipf分布，排名从1开始
            self.expected_probs[cat] = (1.0 / ((i + 1) ** self.zipf_param)) / norm_const

    def update(self, new_value):
        """
        增量更新卡方统计量

        参数:
        new_value: 新的数据点

        返回:
        chi2_stat: 卡方统计量
        p_value: p值
        df: 自由度
        """
        if self.counter > 8:
            self.counter = 0
            self.reset()

        # 更新计数
        self.total_count += 1
        self.counts[new_value] = self.counts.get(new_value, 0) + 1

        # 检查是否需要更新类别集合
        is_new_category = new_value not in self.category_set
        if is_new_category:
            self.categories.append(new_value)
            self.category_set.add(new_value)
            # 重新计算Zipf概率
            self._calculate_zipf_probs()

        # 计算卡方统计量
        return self.calculate_chi_square()

    def calculate_chi_square(self):
        """计算当前的卡方统计量"""
        if self.total_count == 0 or len(self.categories) == 0:
            return 0, 1.0, 0

        # 重新计算期望概率（如果需要）
        if not self.expected_probs or len(self.expected_probs) != len(self.categories):
            self._calculate_zipf_probs()

        # 计算卡方统计量
        obs_counts = []
        exp_counts = []

        for category in self.categories:
            observed = self.counts.get(category, 0)
            expected = self.expected_probs.get(category, 0) * self.total_count

            if expected > 0:  # 避免除以零
                obs_counts.append(observed)
                exp_counts.append(expected)

        # 使用scipy的chisquare函数计算卡方统计量和p值
        if len(obs_counts) > 1:  # 需要至少两个类别才能计算
            chi2_stat, p_value = stats.chisquare(obs_counts, exp_counts)
            df = len(obs_counts) - 1
        else:
            chi2_stat, p_value, df = 0, 1.0, 0

        self.counter += 1



        return chi2_stat, p_value, df

    def reset(self):
        """重置检测器"""
        self.counts = {}
        self.total_count = 0
        if not self.categories:
            self.categories = []
            self.category_set = set()
            self.expected_probs = {}