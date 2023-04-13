import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.family'] = 'SimHei'
# 数据
data = {
    'Hilbert': 8,
    'Row-Major': 9,
    'Z-order': 6
}

# 设置图形大小
fig, ax = plt.subplots(figsize=(8, 6))

# 绘制柱状图
ax.bar(data.keys(), data.values(), width=0.3)

# 添加标签
ax.set_xlabel('不同索引构建金字塔模型')
ax.set_ylabel('耗时 (min)')

# 显示图形
plt.show()