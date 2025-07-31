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
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300

# 增加线条宽度和标记大小
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['lines.markersize'] = 8

# 增加字体大小
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['legend.fontsize'] = 12

# 示例数据（请替换为您自己的数据）

y1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3,
      ]
# -------------------------------|-----------------------------|-----------------------------|-----------------------------|
y2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,
      ]
x = np.arange(0, len(y1))
# y3 = [0.885, 0.889, 0.889, 0.891]
# y4 = [0.873, 0.885, 0.885, 0.885]
# y5 = [0.975, 0.984, 0.984, 0.985]
# y6 = [0.912, 0.971, 0.971, 0.989]

# 创建图表和轴
fig, ax = plt.subplots()

# 绘制折线
# plt.xticks(x, ['100', '200', '300', '400'])
line1, = ax.plot(x, y1, '-', label='Count-Min Sketch')
line2, = ax.plot(x, y2, '-', label='TsMon')
# line3, = ax.plot(x, y3, '-.', label='OmniWindow', marker='v')
# line4, = ax.plot(x, y4, ':', label='Persist-CMS', marker='^')
# line5, = ax.plot(x, y5, ':', label='waveSketch', marker='s')
# line6, = ax.plot(x, y6, ':', label='Fourier', marker='*')

# 添加标题和标签
# ax.set_title('Example', fontweight='bold')
ax.set_xlabel('Time(ns)', fontweight='bold')
ax.set_ylabel('Packets', fontweight='bold')

# 设置坐标轴范围
# ax.set_xlim(-0.3, 3.3)
# ax.set_ylim(0.85, 1)

# 设置轴刻度
ax.xaxis.set_major_locator(MultipleLocator(80))  # 主刻度为2
# ax.xaxis.set_minor_locator(MultipleLocator(1))  # 次刻度为0.5
# ax.yaxis.set_major_locator(MultipleLocator(0.05))  # 主刻度为0.5
# ax.yaxis.set_minor_locator(MultipleLocator(0.01))  # 次刻度为0.1

# 调整网格线
ax.grid(True, which='major', linestyle='-', linewidth=0.5, alpha=0.7)
ax.grid(True, which='minor', linestyle=':', linewidth=0.3, alpha=0.3)

# 添加图例
ax.legend(loc='best', frameon=True, fancybox=True, framealpha=0.8,
          ncol=2, borderpad=0.4, labelspacing=0.5)

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
plt.savefig('./smooth.pdf', bbox_inches='tight')  # PDF适合论文提交
# plt.savefig('paper_plot.png', bbox_inches='tight', dpi=300)  # PNG适合预览

# 显示图表
plt.show()

# =====================================
# 其他可选的高级设置（根据需要取消注释）
# =====================================

# # 双Y轴设置
# def dual_y_axis_example():
#     fig, ax1 = plt.subplots(figsize=(10, 6))
#
#     x = np.arange(0, 10, 0.1)
#     y1 = np.sin(x) * 100  # 第一个Y轴数据
#     y2 = x**2             # 第二个Y轴数据
#
#     # 第一个Y轴
#     color = '#1f77b4'
#     ax1.plot(x, y1, color=color, linestyle='-', label='sin(x)×100')
#     ax1.set_xlabel('X轴标签')
#     ax1.set_ylabel('左Y轴: sin(x)×100', color=color)
#     ax1.tick_params(axis='y', labelcolor=color)
#
#     # 第二个Y轴
#     ax2 = ax1.twinx()
#     color = '#ff7f0e'
#     ax2.plot(x, y2, color=color, linestyle='--', label='x²')
#     ax2.set_ylabel('右Y轴: x²', color=color)
#     ax2.tick_params(axis='y', labelcolor=color)
#
#     # 合并图例
#     lines1, labels1 = ax1.get_legend_handles_labels()
#     lines2, labels2 = ax2.get_legend_handles_labels()
#     ax1.legend(lines1 + lines2, labels1 + labels2, loc='best')
#
#     plt.title('双Y轴示例', fontweight='bold')
#     plt.tight_layout()
#     plt.show()

# # 子图设置
# def subplot_example():
#     fig, axs = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)
#
#     x = np.arange(0, 10, 0.1)
#
#     # 左上子图
#     axs[0, 0].plot(x, np.sin(x))
#     axs[0, 0].set_title('sin(x)')
#
#     # 右上子图
#     axs[0, 1].plot(x, np.cos(x), 'g--')
#     axs[0, 1].set_title('cos(x)')
#
#     # 左下子图
#     axs[1, 0].plot(x, np.sin(x) * np.cos(x), 'r-.')
#     axs[1, 0].set_title('sin(x)cos(x)')
#
#     # 右下子图
#     axs[1, 1].plot(x, np.sin(x) * np.exp(-0.1 * x), 'm:')
#     axs[1, 1].set_title('sin(x)exp(-0.1x)')
#
#     # 共享的X轴和Y轴标签
#     fig.supxlabel('X轴标签')
#     fig.supylabel('Y轴标签')
#
#     plt.suptitle('子图示例', fontweight='bold', fontsize=16)
#     plt.show()

# # 误差线示例
# def errorbar_example():
#     x = np.arange(1, 6)
#     y = x**2
#     yerr = 0.2 * x
#
#     plt.figure(figsize=(10, 6))
#     plt.errorbar(x, y, yerr=yerr, fmt='o-', capsize=5, capthick=1, elinewidth=1,
#                 label='带误差线的数据')
#
#     plt.xlabel('X轴标签')
#     plt.ylabel('Y轴标签')
#     plt.title('误差线示例', fontweight='bold')
#     plt.grid(True)
#     plt.legend()
#     plt.tight_layout()
#     plt.show()

# # 填充区域示例
# def fill_between_example():
#     x = np.arange(0, 10, 0.1)
#     y1 = np.sin(x)
#     y2 = np.sin(x) + 0.2
#     y3 = np.sin(x) - 0.2
#
#     plt.figure(figsize=(10, 6))
#     plt.plot(x, y1, 'k-', label='sin(x)')
#     plt.fill_between(x, y2, y3, alpha=0.2, color='blue',
#                      label='误差范围')
#
#     plt.xlabel('X轴标签')
#     plt.ylabel('Y轴标签')
#     plt.title('填充区域示例', fontweight='bold')
#     plt.grid(True)
#     plt.legend()
#     plt.tight_layout()
#     plt.show()
