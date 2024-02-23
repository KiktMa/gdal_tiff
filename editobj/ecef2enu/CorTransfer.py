import geo
from numpy import *
import numpy as np

# class Change2ENU:
#     def coor2ENU(self, path):
# 输入需要改坐标系的obj文件绝对路径
with open(r"D:\BaiduNetdiskDownload\3143415262515062-20-962\model.obj", 'r') as file:
    vertices = []
    new_vertices = []
    for line in file:
        parts = line.strip().split()

        if not parts:
            continue

        if parts[0] == 'v':
            vertices.append(list(map(float, parts[1:])))

    # 25.040609531680197, 121.2533545134789
    # 24.980294521860554 121.24806089167481
    # 24.980427736593345 121.2537309245741
    # R = 6371068
    # index = int(len(vertices) / 2)
    # lat = math.asin(vertices[index][2] / R) * 180 / math.pi
    # lon = math.acos(vertices[index][0] / (math.cos(math.asin(vertices[index][2] / R)) * R)) * 180 / math.pi
    # print(lat, lon)  #62: 24.979906279659247 121.25023833819394; 63: 24.979567434028905 121.25580597429797
    # 这里采用所有obj都使用同一个ENU坐标系，在obj转3dtiles后的合并才能没有缝隙
    for vertice in range(len(vertices)):
        arr = geo.ecef_to_enu(vertices[vertice][0], vertices[vertice][1], vertices[vertice][2],
                              24.979906279659247, 121.25023833819394, 0.0)
        arr = list(arr)
        arr[0], arr[2] = arr[2], arr[0]
        arr[0], arr[1] = arr[1], arr[0]

        # 绕y轴逆时针旋转90度
        angle_radians = np.radians(90)
        rotation_matrix = np.array([
            [np.cos(angle_radians), 0, np.sin(angle_radians)],
            [0, 1, 0],
            [-np.sin(angle_radians), 0, np.cos(angle_radians)]
        ])
        rotated_point = np.dot(rotation_matrix, arr)

        # arr[0], arr[2] = arr[2], arr[0]
        arr = tuple(rotated_point)
        new_vertices.append(arr)

# 输入需要改坐标系的obj文件绝对路径
with open(r"D:\BaiduNetdiskDownload\3143415262515062-20-962\model.obj", 'r') as infile:
    lines = infile.readlines()

# 输入输出修改obj后的路径
with open(r"D:\BaiduNetdiskDownload\3143415262515062-20-962\model_m.obj", 'w') as outfile:
    # for vertex in new_vertices:
    #     outfile.write(f"v {' '.join(map(str, vertex))}\n")
    start = 0
    for i, line in enumerate(lines):
        if line.startswith("v "):
            vertex = new_vertices[start]
            start += 1
            outfile.write(f"v {' '.join(map(str, vertex))}\n")
        else:
            outfile.write(line)