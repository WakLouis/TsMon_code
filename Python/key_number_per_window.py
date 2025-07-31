# 用于计算hadoop 15 每个时间窗口下的平均和最大流键数量

from pandas.core.interchange.from_dataframe import primitive_column_to_ndarray

if __name__ == '__main__':
    DATA = './hadoop15.csv'
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

    avg = 0
    time = 0
    n = 0
    temp_set = set()

    for packet in packets:
        key, global_time = packet
        if global_time - time > 100000: # 10us - 100us - 1ms - 10ms - 20ms
            time = global_time
            n += 1
            avg  = max(avg, len(temp_set))
            temp_set.clear()

        else:
            temp_set.add(key)

    print(avg)
