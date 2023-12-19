import matplotlib.pyplot as plt

# 数据
data = {
    'Hilbert': 8,
    'Row-Major': 9,
    'Z-order': 6
}

# 设置图形大小
fig, ax = plt.subplots(figsize=(8, 6))

# 绘制柱状图
ax.bar(data.keys(), data.values(), width=0.2)

# 添加标签
ax.set_xlabel('Build pyramid model with different indexes')
ax.set_ylabel('time consuming(min)')

# 显示图形
plt.savefig('fig6.png')
plt.show()