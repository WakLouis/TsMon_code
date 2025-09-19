# filename: hash_conflict_sweep.py
import xxhash
import numpy as np
import math
from concurrent.futures import ProcessPoolExecutor, as_completed
import matplotlib.pyplot as plt

# ---------- 参数区 ----------
finger_bits = 16               # 指纹长度 f（位）
finger_mask = (1 << finger_bits) - 1

flow_number = 200_000          # n，插入的流数量（每轮）
tot_round = 20                 # 每个 m 做多少轮实验取平均
max_workers = min(8, tot_round)

# 要测试的哈希表大小集合（从小到大）
sizes = [
    10, 50, 100, 200, 500, 1_000, 2_000, 5_000, 10_000,
    20_000, 50_000, 100_000, 200_000, 400_000, 800_000, 1_600_000, 3_200_000, 6_400_000, 12_800_000
]

# ----------------------------

def custom_hash(obj, seed):
    return xxhash.xxh64_intdigest(f"{seed}{obj}")

def run_round(round_id, flow_number, hash_table_number, finger_mask):
    """
    单轮实验：返回 (pos_collision, error_count)
    pos_collision: 插入时遇到已占槽的次数（不论指纹是否相同）
    error_count: 指纹相同但 full-key 不同的误判次数（我们关心的真正误判）
    """
    # 生成流键（deterministic per round_id）
    # 注意：使用 range(1, flow_number+1) 以确保恰好 flow_number 个键
    flow_key = [abs(custom_hash(str(i), round_id)) for i in range(1, flow_number + 1)]
    print_finger = [x & finger_mask for x in flow_key]

    # 哈希表：每个槽存 (finger, full_key)，用 0 表示空槽
    hash_table = np.zeros((hash_table_number, 2), dtype=np.uint64)

    pos_collision = 0
    error_count = 0

    for i, key in enumerate(flow_key):
        index = key % hash_table_number
        local_finger = hash_table[index, 0]
        local_key = hash_table[index, 1]

        if local_key == 0:
            # 空槽，写入
            hash_table[index] = (print_finger[i], key)
        else:
            pos_collision += 1
            if print_finger[i] == local_finger and key != local_key:
                error_count += 1
            # 不要覆盖！保持原有值不变

    return pos_collision, error_count

def experiment_for_size(m, flow_number, tot_round, finger_mask):
    """
    对固定哈希表大小 m 做 tot_round 次 run_round 并取平均。
    返回 (avg_pos, avg_err)
    """
    tot_pos = 0
    tot_err = 0
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(run_round, r, flow_number, m, finger_mask)
            for r in range(tot_round)
        ]
        for future in as_completed(futures):
            pos, err = future.result()
            tot_pos += pos
            tot_err += err

    avg_pos = tot_pos / tot_round
    avg_err = tot_err / tot_round
    return avg_pos, avg_err

def main():
    n = flow_number
    f = finger_bits

    results = []
    print("m\tavg_pos\tpos_rate\tavg_err\terr_rate\ttheory_err_rate")
    for m in sizes:
        avg_pos, avg_err = experiment_for_size(m, n, tot_round, finger_mask)
        pos_rate = avg_pos / n
        err_rate = avg_err / n
        # 理论误判率： (1 - e^{-n/m}) / 2^f
        theory_err_rate = (1 - math.exp(-n / m)) / (2 ** f)
        print(f"{m}\t{avg_pos:.2f}\t{pos_rate:.6e}\t{avg_err:.4f}\t{err_rate:.6e}\t{theory_err_rate:.6e}")
        results.append((m, avg_pos, pos_rate, avg_err, err_rate, theory_err_rate))

    # 绘图：实测误判率 vs 理论误判率（横轴 m 取对数）
    ms = [r[0] for r in results]
    err_rates = [r[4] for r in results]
    theory_rates = [r[5] for r in results]
    pos_rates = [r[2] for r in results]

    plt.figure()
    plt.plot(ms, err_rates, marker='o', label='empirical err rate')
    plt.plot(ms, theory_rates, marker='x', label='theory err rate')
    plt.xscale('log')
    plt.xlabel('hash table size (m)')
    plt.ylabel('error rate (errors per insertion)')
    plt.title(f'Empirical vs Theory error rate (n={n}, f={f})')
    plt.legend()
    plt.grid(True, which='both', ls='--', lw=0.3)
    plt.tight_layout()
    plt.show()

    # 绘制位置冲突率
    plt.figure()
    plt.plot(ms, pos_rates, marker='o')
    plt.xscale('log')
    plt.xlabel('hash table size (m)')
    plt.ylabel('position collision rate (per insertion)')
    plt.title(f'Position collision rate vs m (n={n})')
    plt.grid(True, which='both', ls='--', lw=0.3)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
