from TsMon import TsMon
import numpy as np
from collections import defaultdict


def euclidean_distance(seq1, seq2):
    # 确保序列长度相同
    if len(seq1) != len(seq2):
        raise ValueError("序列长度必须相同")

    # 转换为 numpy 数组并计算欧氏距离
    seq1 = np.array(seq1)
    seq2 = np.array(seq2)
    return np.sqrt(np.sum((seq1 - seq2) ** 2))


def cosine_similarity(seq1, seq2):
    # 确保序列长度相同
    if len(seq1) != len(seq2):
        raise ValueError("序列长度必须相同")

    # 转换为 numpy 数组
    seq1 = np.array(seq1)
    seq2 = np.array(seq2)

    # 计算点积
    dot_product = np.dot(seq1, seq2)

    # 计算模长
    norm1 = np.sqrt(np.sum(seq1 ** 2))
    norm2 = np.sqrt(np.sum(seq2 ** 2))

    # 避免除以零
    if norm1 == 0 or norm2 == 0:
        return 0.0

    # 计算余弦相似度
    return dot_product / (norm1 * norm2)


def average_relative_error(seq1, seq2):
    # 确保序列长度相同
    if len(seq1) != len(seq2):
        raise ValueError("序列长度必须相同")

    # 转换为 numpy 数组并确保浮点数类型
    seq1 = np.array(seq1, dtype=np.float64)
    seq2 = np.array(seq2, dtype=np.float64)

    # 计算绝对误差
    abs_error = np.abs(seq1 - seq2)

    # 计算相对误差（避免除以零）
    relative_error = np.divide(abs_error, np.abs(seq1), out=np.zeros_like(abs_error), where=seq1 != 0)

    # 计算平均相对误差
    return np.mean(relative_error)


def energy_similarity(f, f_hat):
    # 确保序列长度相同
    if len(f) != len(f_hat):
        raise ValueError("序列长度必须相同")

    # 转换为 numpy 数组并确保浮点数类型
    f = np.array(f, dtype=np.float64)
    f_hat = np.array(f_hat, dtype=np.float64)

    # 计算能量（平方和的平方根）
    energy_f = np.sqrt(np.sum(f ** 2))
    energy_f_hat = np.sqrt(np.sum(f_hat ** 2))

    # 避免除以零
    if energy_f == 0 or energy_f_hat == 0:
        return 0.0

    # 根据公式计算相似度
    if energy_f <= energy_f_hat:
        return energy_f / energy_f_hat
    else:
        return energy_f_hat / energy_f



def count_packets_by_key(packets, window_size, target_key):
    if not packets:
        return []

    # 获取所有时间戳以确定范围
    all_timestamps = []
    for key, timestamp in packets:
        if key == target_key:
            all_timestamps.append(timestamp)
    if not all_timestamps:
        return []

    min_time = min(all_timestamps)
    max_time = max(all_timestamps)

    # 计算窗口数量
    num_windows = int((max_time - min_time) // window_size) + 1

    # 初始化计数数组
    counters = [0] * num_windows

    # 统计 key=2 的数据包
    for key, time in packets:
        if key == target_key:
            # 计算窗口索引
            window_index = int((time - min_time) // window_size)
            if 0 <= window_index < num_windows:
                counters[window_index] += 1

    return counters




def count_all_packets_by_key(packets, window_size):
    # 初始化 defaultdict 用于存储每个 key 的时间戳
    temp_sequence = defaultdict(list)

    # 按 key 收集时间戳
    for key, timestamp in packets:
        temp_sequence[key].append(timestamp)

    # 初始化输出 defaultdict
    rawsequence = defaultdict(list)

    # 对每个 key 单独处理
    for key, timestamps in temp_sequence.items():
        if not timestamps:
            continue

        # 获取该 key 的时间范围
        min_time = min(timestamps)
        max_time = max(timestamps)

        # 计算该 key 的窗口数量
        num_windows = int((max_time - min_time) // window_size) + 1

        # 初始化计数数组
        counters = [0] * num_windows

        # 统计包数
        for time in timestamps:
            window_index = int((time - min_time) // window_size)
            if 0 <= window_index < num_windows:
                counters[window_index] += 1

        # 存储到 rawsequence
        rawsequence[key] = counters

    return rawsequence

if __name__ == '__main__':
    DATA = './NB15.csv'
    windowSize = 200000000
    ts_mon = TsMon(3, 52257, 1024, 8, windowSize, 3)


    '''
    Raw packets
    '''
    packets = []
    with open(DATA, 'r') as f:
        for line in f:
            key, _, global_time, _ = line.strip().split(',')
            key = int(key)
            global_time = int(global_time)
            packets.append((key, global_time))


    for packet in packets:
        key, global_time = packet
        ts_mon.process(key, global_time)



    '''
    Get raw time series data
    Processing ts_mon time series data
    '''
    # counters = count_packets_by_key(packets, windowSize, target_key=2)
    # ts_mon.plt_values = [x for x in ts_mon.plt_values[ts_mon.plt_values.index(next(filter(lambda x : x != 0, ts_mon.plt_values))):]]

    raw_sequences = count_all_packets_by_key(packets, window_size=windowSize)


    '''
    Result - data flows reconstruction
    '''

    sequences = defaultdict(list)
    for item in ts_mon.re_values:
        for flow_id, count in item.items():
            sequences[flow_id].append(count)

    for flow in sequences:
        sequences[flow] = sequences[flow][1:]

    keys_to_delete = []
    for flow_id in sequences:
        seq = sequences[flow_id]
        # 去除前导零
        # start = next((i for i, x in enumerate(seq) if x != 0), len(seq))
        # sequences[flow_id] = seq[start:]
        # 去除后导零
        # end = next((len(seq) - i - 1 for i, x in enumerate(reversed(seq)) if x != 0), -1) + 1
        # sequences[flow_id] = seq[:end]
        # 如果序列为空，标记该键删除
        if not sequences[flow_id]:
            keys_to_delete.append(flow_id)

    # 删除全零或空序列的键
    for flow_id in keys_to_delete:
        del sequences[flow_id]


    avg_ARE = 0
    avg_cos = 0
    avg_eng = 0

    i = 0

    for flow_id in sequences:
        i += 1
        # print(len(sequences[flow_id]), len(raw_sequences[flow_id]))
        # print(flow_id)
        # print(sequences[flow_id], raw_sequences[flow_id], sep='\n')
        avg_ARE += average_relative_error(sequences[flow_id][:len(raw_sequences[flow_id])], raw_sequences[flow_id][:len(sequences[flow_id])])
        avg_cos += cosine_similarity(sequences[flow_id][:len(raw_sequences[flow_id])], raw_sequences[flow_id][:len(sequences[flow_id])])
        avg_eng += energy_similarity(sequences[flow_id][:len(raw_sequences[flow_id])], raw_sequences[flow_id][:len(sequences[flow_id])])

    avg_ARE /= i
    avg_cos /= i
    avg_eng /= i

    print(avg_ARE, avg_cos, avg_eng)
    print(len(sequences[2]), len(raw_sequences[2]))




