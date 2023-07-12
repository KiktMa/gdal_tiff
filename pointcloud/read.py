# import laspy
# import numpy as np
#
#
# def las_3d_slicing(input_file, output_files_prefix, interval):
#     # 打开LAS文件
#     inFile = laspy.open(input_file, mode="r")
#
#     # 获取点云数据
#     points = np.vstack((inFile.points["X"], inFile.points["Y"], inFile.points["Z"])).transpose()
#
#     # 计算切割的范围
#     min_bounds = np.min(points, axis=0)
#     max_bounds = np.max(points, axis=0)
#
#     # 计算切割的数量
#     num_slices = np.ceil((max_bounds - min_bounds) / interval).astype(int)
#
#     # 进行切割
#     for i in range(num_slices[0]):
#         for j in range(num_slices[1]):
#             for k in range(num_slices[2]):
#                 # 计算切割的边界
#                 slice_min = min_bounds + [i, j, k] * interval
#                 slice_max = slice_min + interval
#
#                 # 筛选在切割范围内的点云
#                 mask = np.all((points >= slice_min) & (points < slice_max), axis=1)
#                 sliced_points = points[mask]
#
#                 # 创建新的LAS文件并保存切割后的点云数据
#                 header = inFile.header.copy()
#                 header.min = slice_min
#                 header.max = slice_max
#
#                 outFile = laspy.open(f"{output_files_prefix}_{i}_{j}_{k}.las", mode="w", header=header)
#                 outFile.points = len(sliced_points)
#                 outFile.x = sliced_points[:, 0]
#                 outFile.y = sliced_points[:, 1]
#                 outFile.z = sliced_points[:, 2]
#                 outFile.close()
#
#     # 关闭输入LAS文件
#     inFile.close()
#
#
# # 调用函数进行切割
# las_3d_slicing("D:\\JavaConsist\MapData\\180m_pointcloud\\corrected-LJYY-Cloud-1-0-9.las", "output_slice", interval=[10, 10, 10])


import laspy
import numpy as np

def cut_las_file(las_path, output_folder, num_cuts):
    # 加载LAS文件
    inFile = laspy.read(las_path)

    # 获取点云的坐标数据
    points = np.vstack((inFile.x, inFile.y, inFile.z)).transpose()

    # 计算每个切割层的高度范围
    min_z = np.min(points[:, 2])
    max_z = np.max(points[:, 2])
    height_range = max_z - min_z
    cut_height = height_range / num_cuts

    # 在XYZ方向上进行切割
    for i in range(num_cuts):
        # 定义切割高度范围
        cut_min_z = min_z + (i * cut_height)
        cut_max_z = min_z + ((i + 1) * cut_height)

        # 获取位于切割高度范围内的点云
        cut_points = points[(points[:, 2] >= cut_min_z) & (points[:, 2] < cut_max_z)]

        # 创建新的LAS文件
        new_las = laspy.file.File(f"{output_folder}/cut_{i}.las", mode="w", header=inFile.header)
        new_las.points = cut_points
        new_las.close()

    # 关闭原始LAS文件
    inFile.close()

def read_las_metadata(file_path):

    in_file = laspy.read(file_path)

    # 访问文件的元数据
    header = in_file.header

    # 输出元数据信息
    print("header:", header)
    print("文件版本:", header.version)
    print("点数:", header.point_count)
    print("x偏移量:", header.x_offset)
    print("y偏移量:", header.y_offset)
    print("z偏移量:", header.z_offset)
    print("x缩放因子:", header.x_scale)
    print("y缩放因子:", header.y_scale)
    print("z缩放因子:", header.z_scale)

# 使用示例
las_file_path = "D:\\JavaConsist\MapData\\180m_pointcloud\\corrected-LJYY-Cloud-1-0-9.las"
# output_folder = "D:\\JavaConsist\\MapData\\180m_pointcloud\\new"
# num_cuts = 5  # 切割层数量

# cut_las_file(las_file_path, output_folder, num_cuts)

read_las_metadata(las_file_path)
