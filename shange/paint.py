import matplotlib.pyplot as plt


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
plt.xlabel('raster data size(GB)')
plt.ylabel('Build pyramid and put it into storage(min)')

# 显示图形
plt.show()