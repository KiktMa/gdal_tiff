import random

import numpy as np
import open3d as o3d
import trimesh
import math
import json, copy
import removeusemtl
import add_texture_in_mergeobj

def wgs_to_metter(x, y):
    x = x * math.pi / 180
    y=y*math.pi/180
    R=6371068
    a=(math.cos(y)*R)*math.cos(x)
    b=(math.cos(y)*R)*math.sin(x)
    c=math.sin(y)*R
    # x=x*math.pi/180
    # y=y*math.pi/180
    # a = math.sqrt((1-(math.sin(y))**2)*((z+6371000)**2)/(1+math.tan(x)))
    # b = a*math.tan(x)
    # c = math.sin(y)*(z+6378137)
    return a,b,c

def wgs_to_metter_height(x, y, z):
    x = x * math.pi / 180
    y=y*math.pi/180
    R=6371068+z
    a=(math.cos(y)*R)*math.cos(x)
    b=(math.cos(y)*R)*math.sin(x)
    c=math.sin(y)*R

    # x=x*math.pi/180
    # y=y*math.pi/180
    # a = math.sqrt((1-(math.sin(y))**2)*((z+6371000)**2)/(1+math.tan(x)))
    # b = a*math.tan(x)
    # c = math.sin(y)*(z+6378137)
    return a,b,c

def geojson_to_obj(geojson_file, obj_file):
    with open(geojson_file, 'r') as f:
        geojson_data = json.load(f)

    vertices = []
    faces = []

    for feature in geojson_data['features']:
        if feature['geometry']['type'] == 'Point':
            coordinates = feature['geometry']['coordinates']
            vertices.append(coordinates)
        elif feature['geometry']['type'] == 'LineString':
            coordinates = feature['geometry']['coordinates']
            vertices.extend(coordinates)
            faces.append(list(range(len(vertices) - len(coordinates), len(vertices))))
        elif feature['geometry']['type'] == 'Polygon':
            coordinates = feature['geometry']['coordinates'][0]  # Assuming only exterior ring
            coordinates_up=copy.deepcopy(coordinates)
            for i in coordinates: # 建筑物屋顶预测图及底面点
                i[0], i[1], z=wgs_to_metter(i[0], i[1])
                # i[0]-=174.064252
                # i[1]-=463.469967
                # z+=360.203842594102
                i.append(z)
                # x,y,z=Xyz2Blh(i[0], i[1], 2696351.106957404)
                # print(x,y,z)
            vertices.extend(coordinates)
            faces.append(list(range(len(vertices) - len(coordinates), len(vertices))))
            hight = random.randint(6, 20)
            for i in coordinates_up: # 顶面
                i[0], i[1], z = wgs_to_metter_height(i[0], i[1], hight)
                # i[0]-=174.064252
                # i[1]-=463.469967#绿色
                # z+=360.203842594102#蓝36.69913
                i.append(z)
            vertices.extend(coordinates_up)
            faces.append(list(range(len(vertices) - len(coordinates), len(vertices))))
            for i in range(len(coordinates) - 1): # 侧面顶点连接
                faces.append("122")
                faces.append([len(vertices) - 2 * len(coordinates) + i, len(vertices) - 2 * len(coordinates) + i + 1,
                              len(vertices) - len(coordinates) + i + 1, len(vertices) - len(coordinates) + i])

        with open(obj_file, 'w') as f:
            for vertex in vertices:
                f.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")

            for face in faces:
                if face=="122":
                    f.write("# cemian\n")
                    continue
                f.write("f " + " ".join(str(v + 1) for v in face) + "\n")

def load_obj(file_path):
    mesh = trimesh.load(file_path)
    return mesh

def load_obj_with_texture(file_path):
    mesh = o3d.io.read_triangle_mesh(file_path)
    return mesh

def merge_meshes(mesh1_v, mesh2):
    # 获取顶点和面信息
    vertices1 = mesh1_v.vertices
    triangles1 = mesh1_v.faces
    vertex_normals1 = mesh1_v.vertex_normals
    # arr = []
    # for vertices in range(len(vertices1)):
    #     tme = []
    #     for ve in range(len(vertices1[vertices])):
    #         arr.append(vertices1[vertices][ve])
    # arr = np.array(arr)
    # vertices2 = np.asarray(mesh1_vt.vertices)
    # triangles1 = np.asarray(mesh1_vt.triangles)
    # triangles2 = mesh1_v.triangles
    # triangle_uvs1 = np.asarray(mesh1_vt.triangle_uvs)
    # vertex_normals1 = np.asarray(mesh1_vt.vertex_normals)

    v2 = mesh2.vertices
    f2 = mesh2.faces
    v2 = np.array(v2)
    f2 = np.array(f2)

    # 合并顶点和面
    f2 = np.array(f2) + np.shape(vertices1)[0]
    v = np.concatenate((vertices1, v2), axis=0)
    f = np.concatenate((triangles1, f2), axis=0)

    if len(vertex_normals1) > 0:
        vertex_normals_combined = np.concatenate((vertex_normals1, np.zeros_like(vertex_normals1)))
    else:
        vertex_normals_combined = np.zeros((0, 3))

    # 创建合并后的Mesh对象
    # mesh_combined = o3d.geometry.TriangleMesh()
    obj = trimesh.Trimesh(vertices=v, faces=f, vertex_normals=vertex_normals_combined)
    # mesh_combined.vertices = o3d.utility.Vector3dVector(v)
    # mesh_combined.vertices = o3d.utility.Vector3dVector(f)
    # mesh_combined.triangle_uvs = o3d.utility.Vector2dVector(triangle_uvs_combined)
    # mesh_combined.vertex_normals = o3d.utility.Vector3dVector(vertex_normals_combined)

    return obj

def main():
    # 建筑物json转obj
    geojson_file = r"C:\Users\mj\Code\Obj\new.json"  # json文件地址
    bulid_obj_file = r"C:\Users\mj\Code\Obj\OBJ\new11.obj"  # 建筑物obj临时文件
    geojson_to_obj(geojson_file, bulid_obj_file)

    # 由于地理obj文件由多个切片构成，首先对其进行合并，使用cloudcompare软件对文件进行合并
    input_file_path = r"C:\Users\mj\Code\Obj\removeuse\Merged mesh.obj"  # 合并后的地理obj文件地址
    output_file_path = r"C:\Users\mj\Code\Obj\removeuse\mesh11.obj"  # 删除合并地理obj文件中的usemtl行（处理后的文件地址）

    # 删除合并地理obj文件中的usemtl行
    removeusemtl.remove_usemtl_lines(input_file_path, output_file_path)

    # 加载处理后的地理obj文件
    mesh_with_v = load_obj(output_file_path)

    # 加载没有纹理信息的OBJ文件（建筑物obj文件地址）
    mesh_without_texture = load_obj(bulid_obj_file)

    # 合并两个Mesh对象（合并两个obj文件，处理后的obj文件中只有v、vn、f信息还需要进行纹理贴图）
    merged_mesh = merge_meshes(mesh_with_v, mesh_without_texture)

    # 对合并后的obj进行纹理贴图，outfile_obj为纹理贴图后的保存地址
    outfile_obj = r"C:\Users\mj\Code\Obj\merge\new_obj111.obj"
    add_texture_in_mergeobj.merge_meshes(merged_mesh, outfile_obj)

if __name__ == "__main__":
    main()