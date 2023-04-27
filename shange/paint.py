import matplotlib.pyplot as plt


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 定义数据
data = {
    'PostGre+PostGis': [3, 7, 16, 35, 58],
    'ArcGis+FileSystem': [2, 9, 23, 49, 70],
    'Geotrellis': [5, 13, 23, 66, 89],
    'Geotrellis+GeoSOT': [2.9, 5, 9, 29, 45]
}
x = [0.1, 0.5, 1, 3.7, 5.5]

# 绘制折线图
for label, values in data.items():
    plt.plot(x, values, label=label)

# 添加图例、标题、轴标签等
plt.legend()
plt.xlabel('影像大小(GB)')
plt.ylabel('构建金字塔并入库(min)')

# 显示图形
plt.show()