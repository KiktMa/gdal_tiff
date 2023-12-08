import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# 设置中文字体
plt.rcParams["font.sans-serif"] = ["SimHei"]

# 数据
pointcloud = [0.01, 0.5, 1.7, 5, 10, 30]
hbase = [2734, 35174, 84376, 225347, 383746, 1208314]
accumulo = [456, 13537, 49753, 164070, 294644, 974677]
mysql = [1460, 67359, 211131, 644224, 1244455, 2554430]

# 创建图表
fig = plt.figure(figsize=(10, 8))
gs = GridSpec(2, 1, height_ratios=[20, 1])  # 2 行，1 列的网格，高度比例为 4:1

# 上半部分：折线图
ax1 = fig.add_subplot(gs[0])
ax1.plot(pointcloud, hbase, marker='o', label='HBase')
ax1.plot(pointcloud, accumulo, marker='o', label='Accumulo')
ax1.plot(pointcloud, mysql, marker='o', label='MySQL')
ax1.set_title('不同存储模型对点云数据进行存储时间对比')
ax1.set_xlabel('点云数据量 (百万)')
ax1.set_ylabel('存储耗时(ms)')
ax1.legend()
ax1.grid(True)

# 下半部分：表格
ax2 = fig.add_subplot(gs[1])
ax2.axis('off')  # 关闭下半部分的坐标轴
table_data = [hbase, accumulo, mysql]
row_labels = ['HBase(ms)', 'Accumulo(ms)', 'MySQL(ms)']
col_labels = ['0.01', '0.5', '1', '5', '10', '30']
ax2.table(cellText=table_data, rowLabels=row_labels, colLabels=col_labels, cellLoc='center', loc='center')

# 调整图表布局，以便表格和折线图之间有间隔
plt.subplots_adjust(hspace=0.25)

# 保存
plt.savefig('performance_comparison.png')
plt.show()
