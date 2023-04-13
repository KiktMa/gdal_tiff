import laspy
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 读取LAS数据
las_file = laspy.read("D:\\JavaConsist\\MapData\\180m_pointcloud\\corrected-LJYY-Cloud-1-0-9.las")
# las_file = laspy.read("D:\\JavaConsist\\MapData\\180m_pointcloud\\corrected-LJYY-Cloud-1-0-9.las")

# 获取X、Y、Z坐标和强度数据
x = las_file.X
y = las_file.Y
z = las_file.Z
intensity = las_file.intensity

# 绘制三维散点图
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, c=intensity, cmap='jet', alpha=0.5)

# 设置坐标轴标签
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# 显示图像
plt.show()