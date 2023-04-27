import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

# 数据
sizes = ["0.5x0.5", "2x2", "5x5", "7x7"]
postgres = [2, 10, 94, 153]
accumulo = [8, 15, 22, 41]

# 绘图
plt.plot(sizes, postgres, label="PostgreSQL")
plt.plot(sizes, accumulo, label="Accumulo")
plt.xlabel("范围(km²)")
plt.ylabel("读取时间(s)")
plt.legend()

# 显示图形
plt.show()