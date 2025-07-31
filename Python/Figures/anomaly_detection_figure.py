# 用于画异常检测的示意图

import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler
from stack_data import markers_from_ranges

# 生成数据（含4个异常点）
# np.random.seed(54009)
# data = np.random.normal(100, 3, 60)
# anomaly_indices = np.random.choice(60, 4, replace=False)
# for i in anomaly_indices:
#     data[i] += np.random.choice([20, -20])

data = []
anomaly_indices = []
count = 0
with open('../HUAWEI.csv', 'r') as f:
    for line in f:
        count += 1
        if count > 250 or count < 150 : continue

        key, p_bits, global_time, label = line.strip().split(',')
        key = int(key)
        global_time = int(global_time)
        label = int(label)
        p_bits = int(p_bits)
        data.append(p_bits)
        if label == 1:
            anomaly_indices.append(len(data)-1)


x = np.arange(len(data)-10)
window_size = 8


# 设置图表风格为论文品质
plt.style.use('seaborn-v0_8-whitegrid')

# 自定义颜色循环（更适合区分）
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
          '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']
plt.rcParams['axes.prop_cycle'] = cycler('color', colors)

# 增加默认图表大小和DPI（适合论文）
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300

# 增加线条宽度和标记大小
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['lines.markersize'] = 4

# 增加字体大小
plt.rcParams['font.size'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['legend.fontsize'] = 14

means, stds, upper, lower = [], [], [], []
range_x = []
anomalies_x, anomalies_y = [], []

base = 300

for i in range(window_size, len(data)):
    window = data[i - window_size:i]
    # 剔除最大和最小值（仅各剔除一次）
    trimmed = list(window)
    trimmed.remove(np.max(trimmed))
    trimmed.remove(np.min(trimmed))
    trimmed = np.array(trimmed)

    mu = np.mean(trimmed)
    sigma = np.std(trimmed)

    means.append(mu)
    stds.append(sigma)
    upper.append(mu + 3 * sigma + base)
    lower.append(mu - 3 * sigma - base)
    range_x.append(i-10)

    # 检测当前点是否为异常
    if abs(data[i] - mu) > 3 * sigma + base:
        anomalies_x.append(i-10)
        anomalies_y.append(data[i])

IQR_x = [29, 30, 33, 55, 56, 86, 87]
IQR_y = [data[x] for x in IQR_x]
IQR_x = [IQR_x[x] - 10 for x in range(len(IQR_x))]

# KNN_x = [30]
KNN_y = [data[30]]
KNN_x = [20]



# 绘图
plt.style.use('seaborn-v0_8-muted')
fig, ax = plt.subplots(figsize=(20, 5))

ax.plot(x, data[10:], label='Data flow', color='#4C72B0', marker='o', linewidth=2)
# ax.plot(range_x, means, linestyle='--', color='#55A868', label='Average')
# ax.fill_between(range_x, lower, upper, color='#C44E52', alpha=0.2, label='Tolerance Range')
ax.scatter(anomalies_x, anomalies_y, color='#c96442', label='Anomaly', zorder=5)
ax.scatter(anomalies_x, anomalies_y, edgecolors='#667a3a', label='TsTask', s=75, facecolors='none',linewidth=1)
ax.scatter(IQR_x, IQR_y, edgecolors='#d62728', label='IQR', s=150, facecolors='none',linewidth=1, marker='^')
ax.scatter(KNN_x, KNN_y, edgecolors='#9467bd', label='KNN', s=225, facecolors='none',linewidth=1, marker='X')
print(anomaly_indices)

# ax.set_title("Robust 3-Sigma Detection with Trimmed Mean & Std", fontsize=16)
ax.set_xlabel("Time", fontweight='bold')
ax.set_ylabel("Bits", fontweight='bold' )
# 调整网格线
ax.grid(True, which='major', linestyle='-', linewidth=0.5, alpha=0.7)
ax.grid(True, which='minor', linestyle=':', linewidth=0.3, alpha=0.3)
ax.legend()
plt.tight_layout()

plt.xlim(0, 90)
plt.ylim(0)

# 紧凑布局
plt.tight_layout()

# 保存图表（按需调整文件格式和分辨率）
plt.savefig('./sigma.pdf', bbox_inches='tight')  # PDF适合论文提交

plt.show()
