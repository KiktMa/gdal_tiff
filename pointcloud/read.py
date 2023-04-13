import open3d as o3d

# 读取点云数据
point_cloud = o3d.io.read_point_cloud("D:\\JavaConsist\\MapData\\180m点云\\corrected-LJYY-Cloud-1-0-9.las")

# 可视化点云
o3d.visualization.draw_geometries([point_cloud])

# 查看点云信息
print(point_cloud)