import geo
from numpy import *
import numpy as np

with open(r"C:\Users\mj\Desktop\obj\test\Merged mesh.obj", 'r') as file:
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
    R = 6371068
    index = int(len(vertices) / 2)
    lat = math.asin(vertices[index][2] / R) * 180 / math.pi
    lon = math.acos(vertices[index][0] / (math.cos(math.asin(vertices[index][2] / R)) * R)) * 180 / math.pi
    print(lat, lon)
    for vertice in range(len(vertices)):
        arr = geo.ecef_to_enu(vertices[vertice][0], vertices[vertice][1], vertices[vertice][2],
                              lat, lon, 0.0)
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

with open(r"C:\Users\mj\Desktop\obj\test\Merged mesh.obj", 'r') as infile:
    lines = infile.readlines()

with open(r"C:\Users\mj\Desktop\obj\test\Merged mesh.obj", 'w') as outfile:
    # for vertex in new_vertices:
    #     outfile.write(f"v {' '.join(map(str, vertex))}\n")
    v_len = len(new_vertices)
    for i, line in enumerate(lines):
        if line.startswith("v "):
            vertex = new_vertices[(i-2) // 1]  # 每行三个顶点，减2是因为new_vertices索引开始时为2，因为obj中前两行为cloudcompare合并时锁产生的注释
            outfile.write(f"v {' '.join(map(str, vertex))}\n")
        else:
            outfile.write(line)