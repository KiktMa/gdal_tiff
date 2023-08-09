import matplotlib.pyplot as plt

# 数据
pointcloud = [0.01, 0.5, 1.7, 5, 10, 30]
hbase = [2734, 35174, 84376, 225347, 383746, 1208314]
accumulo = [456, 13537, 49753, 164070, 294644, 974677]
mysql = [1460, 67359, 211131, 644224, 1244455, 2554430]

# 创建折线图
plt.figure(figsize=(10, 6))
plt.plot(pointcloud, hbase, marker='o', label='HBase')
plt.plot(pointcloud, accumulo, marker='o', label='Accumulo')
plt.plot(pointcloud, mysql, marker='o', label='MySQL')

# 添加标题和标签
plt.title('Comparison of storage time between different databases')
plt.xlabel('PointCloud Size(million)')
plt.ylabel('Time (ms)')

# 添加图例
plt.legend()

# 显示图表
plt.grid(True)

# 保存
plt.savefig('performance_comparison.png')
plt.show()
