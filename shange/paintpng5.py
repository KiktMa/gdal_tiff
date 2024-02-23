import matplotlib.pyplot as plt
import pandas as pd

# 设置中文字体
plt.rcParams["font.sans-serif"] = ["SimHei"]

# 数据
data = {
    'PostGresql+PostGis': [3, 7, 16, 35, 56.4],
    'ArcGis+FileSystem': [2, 9, 23, 49, 79.8],
    'Geotrellis': [5, 13, 23, 66, 87.9],
    'Geotrellis+GeoSOT': [2.9, 5, 9, 29, 43.5]
}
x = [0.1, 0.5, 1, 3.7, 5.3]

# 为折线图和表格创建一个图形和两个子图形
fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [20, 1]}, figsize=(8, 6))

# 用点标记绘制折线图
for label, values in data.items():
    ax1.plot(x, values, marker='o', label=label)  # 为点标记添加标记=“0”

ax1.legend()
ax1.set_xlabel('栅格影像大小(GB)')
ax1.set_ylabel('构建金字塔并入库(min)')

# 为表创建DataFrame
# table_data = pd.DataFrame(data, index=[str(val) + 'GB' for val in x])
#
# # 绘制表格
# table = ax2.table(cellText=table_data.values, colLabels=table_data.columns, rowLabels=table_data.index,
#                   cellLoc='center', rowLoc='center', loc='center')

# 隐藏表格的轴
ax2.axis('off')

plt.subplots_adjust(hspace=0.15)  # 调整子地块之间的间距
plt.savefig('fig5.png')
plt.show()