import pandas as pd

# 读取数据
# 如果文件特别大，可以考虑用 chunksize 分块读取
df = pd.read_csv("report.csv")  # 你的例子是制表符分隔

# 按 class 和 memory 分组，计算 are, energy, cos 的平均值
result = df.groupby(["class", "memory"])[["cos", "energy", "are"]].mean().reset_index()

# 保存结果
# result.to_csv("result.csv", index=False)

print(result)
