import geo
from numpy import *
import numpy as np

with open(r"C:\Users\mj\Code\Obj\merge\new_obj333.obj", 'r') as file:
    vertices = []
    new_vertices = []
    for line in file:
        parts = line.strip().split()

        if not parts:
            continue

        if parts[0] == 'v':
            vertices.append(list(map(float, parts[1:])))

    for vertice in range(len(vertices)):
        arr = geo.ecef_to_enu(vertices[vertice][0], vertices[vertice][1], vertices[vertice][2],
                              25.040609531680197, 121.2533545134789, 0.0)
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
        arr = tuple(arr)
        new_vertices.append(arr)

with open(r"C:\Users\mj\Desktop\output.txt", 'w') as outfile:
    for vertex in new_vertices:
        outfile.write(f"v {' '.join(map(str, vertex))}\n")