import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams["font.sans-serif"] = ["SimHei"]

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

# 数据
sizes = ["0.5x0.5", "2x2", "5x5", "7x7"]
postgres = [2, 10, 94, 153]
accumulo = [8, 15, 22, 41]

# 绘图
plt.plot(sizes, postgres, marker='o', label="PostgreSQL")  # 添加点标记 marker='o'
plt.plot(sizes, accumulo, marker='o', label="Accumulo")  # 添加点标记 marker='o'
plt.xlabel("栅格范围(km²)")
plt.ylabel("读取时间(s)")
plt.legend()

# 显示图形
plt.savefig('fig7.png')
plt.show()