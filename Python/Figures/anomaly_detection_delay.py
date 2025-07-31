import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from cycler import cycler
import matplotlib

# 设置图表风格为论文品质
plt.style.use('seaborn-v0_8-whitegrid')

# 自定义颜色循环（更适合区分）
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
          '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']
plt.rcParams['axes.prop_cycle'] = cycler('color', colors)

# 增加默认图表大小和DPI（适合论文）
plt.rcParams['figure.figsize'] = (12, 4)
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 150

# 增加线条宽度和标记大小
plt.rcParams['lines.linewidth'] = 2.0
plt.rcParams['lines.markersize'] = 8

# 增加字体大小
plt.rcParams['font.size'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['legend.fontsize'] = 14

# 示例数据（请替换为您自己的数据）
# x = np.arange(0, 5)

# 缩小间距：通过调整 x 坐标的间隔
# spacing_factor = 1  # 控制间距的因子，值越小间距越小
x = np.arange(8)

y1 = [345, 320, 290, 318000, 191000, 191312, 222000, 230000]
upper = [0, 0, 0, 128000, 5000, 6120, 32000, 40000]
lower = [345, 320, 290, 190000, 190000, 190000, 190000, 190000]
# y2 = [0.951, 0.068, 0.448, 0.515, 0.31, 0.976, 0.351, 0.832]
# y2 = [381000]
# y3 = [2.375, 3.875, 2.4, 1.863, 1.388]
# y4 = [4.75, 6.638, 3.188, 2.813, 2.788]
# y5 = [0.975, 0.984, 0.984, 0.985]
# y6 = [0.912, 0.971, 0.971, 0.989]

# 创建图表和轴
fig, ax = plt.subplots()


# 绘制折线
# plt.yscale('log')
bars = plt.bar(x, lower, width=0.25, hatch='//',
               edgecolor='white', label='Link Latency')
plt.bar(x, upper, bottom=lower, width=0.25, hatch='//',
               edgecolor='white', label='Execution Time')
# bars = plt.bar(x + 0.125, y2, width=0.25, hatch='//',
#                edgecolor='white', label='F1 Score')
plt.xticks(x, ['TsMon', 'HSTD', 'Diff-1', 'The Chi-Squared Test', 'IQR', 'Z-Score', 'KNN', 'AE'])

for i, bar in enumerate(bars):
    if i > 2 : break
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2., height,
             f'{height}ns',
             ha='center', va='bottom')
# plt.xticks(x, ['10us', '100us', '1ms', '10ms', '20ms'])
# line1, = ax.plot(x, y1, '-', label='Max rate - CMS', marker='o')
# line2, = ax.plot(x, y2, '--', label='Average rate - CMS', marker='h')
# line3, = ax.plot(x, y3, '-.', label='Max rate - TsMon', marker='^')
# line4, = ax.plot(x, y4, ':', label='Average rate - TsMon', marker='s')
# line5, = ax.plot(x, y5, ':', label='waveSketch', marker='o')
# line6, = ax.plot(x, y6, ':', label='Fourier', marker='o')

# plt.fill_between(x, y1, y2, alpha=0.3)
# plt.fill_between(x, y3, y4, alpha=0.3)

# 添加标题和标签
# ax.set_title('Example', fontweight='bold')
ax.set_xlabel('Anomaly detection approach', fontweight='bold')
ax.set_ylabel('Time(ns)', fontweight='bold')
plt.legend()

# 设置坐标轴范围
# ax.set_xlim(-0.3, 5.3)
# ax.set_ylim(0, 1)

# 设置轴刻度
# ax.xaxis.set_major_locator(MultipleLocator(10))  # 主刻度为2
# ax.xaxis.set_minor_locator(MultipleLocator(0.5))  # 次刻度为0.5
# ax.yaxis.set_major_locator(MultipleLocator(10))  # 主刻度为0.5
# ax.yaxis.set_minor_locator(MultipleLocator(5))  # 次刻度为0.1

# 调整网格线
ax.grid(True, which='major', linestyle='-', linewidth=0.5, alpha=0.7)
ax.grid(True, which='minor', linestyle=':', linewidth=0.3, alpha=0.3)

# 添加图例
# ax.legend(loc='best', frameon=True, fancybox=True, framealpha=0.8,
#           ncol=2, borderpad=0.4, labelspacing=0.5)

# 调整轴线和刻度的宽度
for spine in ax.spines.values():
    spine.set_linewidth(1.0)

ax.tick_params(width=1.0, direction='out', length=6)
ax.tick_params(which='minor', width=0.8, direction='out', length=4)

# 添加文本标注
# ax.text(1, 1, r'$f(x) = \sin(x)$', fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

# 紧凑布局
plt.tight_layout()

# 保存图表（按需调整文件格式和分辨率）
plt.savefig('./delay.pdf', bbox_inches='tight')  # PDF适合论文提交
# plt.savefig('paper_plot.png', bbox_inches='tight', dpi=300)  # PNG适合预览

# 显示图表
plt.show()
