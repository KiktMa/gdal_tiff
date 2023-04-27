import laspy
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 读取LAS数据
las_file = laspy.read("D:\\JavaConsist\\MapData\\180m_pointcloud\\corrected-LJYY-Cloud-1-0-9.las")
# las_file = laspy.read("D:\\JavaConsist\\MapData\\180m_pointcloud\\corrected-LJYY-Cloud-1-0-9.las")

# 获取点云数据
point_cloud = np.vstack((las_file.x, las_file.y, las_file.z)).transpose()

# 绘制三维散点图
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(point_cloud[:, 0], point_cloud[:, 1], point_cloud[:, 2], s=0.1)

# 设置坐标轴范围
x_min, x_max = np.min(point_cloud[:, 0]), np.max(point_cloud[:, 0])
y_min, y_max = np.min(point_cloud[:, 1]), np.max(point_cloud[:, 1])
z_min, z_max = np.min(point_cloud[:, 2]), np.max(point_cloud[:, 2])
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_zlim(z_min, z_max)

# 设置坐标轴标签和图像标题
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Point Cloud')

# 显示图像
plt.show()