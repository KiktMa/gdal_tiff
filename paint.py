import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 数据
data = {
    '0.5x0.5': {'postgres': 2, 'accumulo': 8},
    '2x2': {'postgres': 10, 'accumulo': 15},
    '5x5': {'postgres': 94, 'accumulo': 22},
    '7x7': {'postgres': 153, 'accumulo': 41},
}

# 提取x轴和y轴数据
x = list(data.keys())
postgres_y = [v['postgres'] for v in data.values()]
accumulo_y = [v['accumulo'] for v in data.values()]

# 设置中文字体
font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=14)

# 设置图形大小
fig, ax = plt.subplots(figsize=(8, 6))

# 绘制折线图
ax.plot(x, postgres_y, label='Postgres')
ax.plot(x, accumulo_y, label='Accumulo')

# 添加标题、标签和图例
ax.set_xlabel('范围 (km)', fontproperties=font)
ax.set_ylabel('检索时间 (s)', fontproperties=font)
ax.legend()

# 显示图形
plt.show()