# import numpy as np
# import open3d as o3d
# import trimesh
#
# def load_obj(file_path):
#     mesh = o3d.io.read_triangle_mesh(file_path)
#     return mesh
#
# def load_obj2(file_path):
#     mesh = trimesh.load_mesh(file_path)
#     return mesh
#
# def merge_meshes(mesh1, mesh2):
#     # 获取顶点、面、纹理坐标和颜色信息
#     vertices1 = np.asarray(mesh1.vertices)
#     triangles1 = np.asarray(mesh1.triangles)
#     triangle_uvs1 = np.asarray(mesh1.triangle_uvs)
#     vertex_color1 = np.asarray(mesh1.vertex_normals)
#
#     vertices2 = np.asarray(mesh2.vertices)
#     triangles2 = np.asarray(mesh2.triangles)
#     vertex_color2 = np.asarray(mesh2.vertex_normals)
#     triangle_uvs2 = np.asarray(mesh2.triangle_uvs)
#
#     # 合并顶点、面、纹理坐标和颜色
#     vertices_combined = np.vstack((vertices1, vertices2 + np.max(vertices1, axis=0)))
#     triangles_combined = np.vstack((triangles1, triangles2 + len(vertices1)))
#
#     # 确保纹理坐标和颜色信息对齐
#     if len(triangle_uvs1) > 0 and len(triangle_uvs2) > 0:
#         triangle_uvs_combined = np.vstack((triangle_uvs1, triangle_uvs2))
#     else:
#         triangle_uvs_combined = []
#
#     if len(vertex_color1) > 0 and len(vertex_color2) > 0:
#         vertex_color_combined = np.vstack((vertex_color1, vertex_color2))
#     else:
#         vertex_color_combined = []
#
#     # 创建合并后的Mesh对象
#     mesh_combined = o3d.geometry.TriangleMesh()
#     mesh_combined.vertices = o3d.utility.Vector3dVector(vertices_combined)
#     mesh_combined.triangles = o3d.utility.Vector3iVector(triangles_combined)
#
#     if len(triangle_uvs_combined) > 0:
#         mesh_combined.triangle_uvs = o3d.utility.Vector2dVector(triangle_uvs_combined)
#
#     if len(vertex_color_combined) > 0:
#         mesh_combined.vertex_colors = o3d.utility.Vector3dVector(vertex_color_combined)
#
#     return mesh_combined
#
# def main():
#     # 加载带有纹理信息的OBJ文件
#     mesh_with_texture = load_obj(r"C:\Users\mj\Code\Obj\OBJ\3143415262517261-20-962\model.obj")
#
#     # 加载没有纹理信息的OBJ文件
#     mesh_without_texture = load_obj2(r"C:\Users\mj\Code\Obj\OBJ\new.obj")
#
#     # 合并两个Mesh对象
#     merged_mesh = merge_meshes(mesh_with_texture, mesh_without_texture)
#
#     # 保存合并后的OBJ文件
#     o3d.io.write_triangle_mesh(r"C:\Users\mj\Code\Obj\merged_output.obj", merged_mesh)
#
# if __name__ == "__main__":
#     main()

# import numpy as np
# import open3d as o3d
# import trimesh
#
# def load_obj(file_path):
#     mesh = o3d.io.read_triangle_mesh(file_path)
#     return mesh
#
# def load_obj2(file_path):
#     mesh = trimesh.load(file_path)
#     return mesh
#
# def merge_meshes(mesh1, mesh2):
#     # 获取顶点和面信息
#     vertices1 = np.asarray(mesh1.vertices)
#     triangles1 = np.asarray(mesh1.triangles)
#     triangle_uvs1 = np.asarray(mesh1.triangle_uvs)
#     vertex_color1 = np.asarray(mesh1.vertex_normals)
#
#     v2 = mesh2.vertices  # 这样得到的v,f格式是trimesh 内置的格式，不能直接用于其它计算，需要转换为numpy
#     f2 = mesh2.faces
#     v2 = np.array(v2)
#     f2 = np.array(f2)
#     # vertices2 = np.asarray(mesh2.vertices)
#     # triangles2 = np.asarray(mesh2.triangles)
#     # triangle_uvs2 = np.asarray(mesh2.triangle_uvs)
#     # vertex_color2 = np.asarray(mesh2.vertex_colors)
#
#     # 合并顶点和面
#     vertices_combined = np.vstack((vertices1, v2 + np.max(vertices1, axis=0)))
#     triangles_combined = np.vstack((triangles1, f2 + len(vertices1)))
#     triangle_uvs_combined = np.vstack((triangle_uvs1, []))
#     vertex_color_combined = np.vstack((vertex_color1, []))
#
#     # 创建合并后的Mesh对象
#     mesh_combined = o3d.geometry.TriangleMesh()
#     mesh_combined.vertices = o3d.utility.Vector3dVector(vertices_combined)
#     mesh_combined.triangles = o3d.utility.Vector3iVector(triangles_combined)
#     mesh_combined.triangle_uvs = o3d.utility.Vector3dVector(triangle_uvs_combined)
#     mesh_combined.vertex_colors = o3d.utility.Vector3dVector(vertex_color_combined)
#
#     return mesh_combined
#
# def main():
#     # 加载带有纹理信息的OBJ文件
#     mesh_with_texture = load_obj(r"C:\Users\mj\Code\Obj\OBJ\3143415262517261-20-962\model.obj")
#
#     # 加载没有纹理信息的OBJ文件
#     mesh_without_texture = load_obj2(r"C:\Users\mj\Code\Obj\OBJ\new.obj")
#
#     # 合并两个Mesh对象
#     merged_mesh = merge_meshes(mesh_with_texture, mesh_without_texture)
#
#     # 保存合并后的OBJ文件
#     o3d.io.write_triangle_mesh(r"C:\Users\mj\Code\Obj\merged_output.obj", merged_mesh)
#
# if __name__ == "__main__":
#     main()

# import numpy as np
# import open3d as o3d
# import trimesh
#
# def load_obj(file_path):
#     mesh = o3d.io.read_triangle_mesh(file_path)
#     return mesh
#
# def load_obj2(file_path):
#     mesh = trimesh.load(file_path)
#     return mesh
#
# def merge_meshes(mesh1, mesh2):
#     # 获取顶点和面信息
#     vertices1 = np.asarray(mesh1.vertices)
#     triangles1 = np.asarray(mesh1.triangles)
#     triangle_uvs1 = np.asarray(mesh1.triangle_uvs)
#     vertex_normals1 = np.asarray(mesh1.vertex_normals)
#
#     v2 = mesh2.vertices
#     f2 = mesh2.faces
#     v2 = np.array(v2)
#     f2 = np.array(f2)
#
#     # 合并顶点和面
#     vertices_combined = np.vstack((vertices1, v2 + np.max(vertices1, axis=0)))
#     triangles_combined = np.vstack((triangles1, f2 + len(vertices1)))
#
#     # 处理纹理坐标和法线信息
#     if len(triangle_uvs1) > 0:
#         triangle_uvs_combined = np.vstack((triangle_uvs1, np.zeros_like(triangle_uvs1)))
#     else:
#         triangle_uvs_combined = np.zeros((0, 2))
#
#     if len(vertex_normals1) > 0:
#         vertex_normals_combined = np.vstack((vertex_normals1, np.zeros_like(vertex_normals1)))
#     else:
#         vertex_normals_combined = np.zeros((0, 3))
#
#     # 创建合并后的Mesh对象
#     mesh_combined = o3d.geometry.TriangleMesh()
#     mesh_combined.vertices = o3d.utility.Vector3dVector(vertices_combined)
#     mesh_combined.triangles = o3d.utility.Vector3iVector(triangles_combined)
#     mesh_combined.triangle_uvs = o3d.utility.Vector2dVector(triangle_uvs_combined)
#     mesh_combined.vertex_normals = o3d.utility.Vector3dVector(vertex_normals_combined)
#
#     return mesh_combined
#
# def main():
#     # 加载带有纹理信息的OBJ文件
#     mesh_with_texture = load_obj(r"C:\Users\mj\Code\Obj\OBJ\3143415262517261-20-962\model.obj")
#
#     # 加载没有纹理信息的OBJ文件
#     mesh_without_texture = load_obj2(r"C:\Users\mj\Code\Obj\OBJ\new.obj")
#
#     # 合并两个Mesh对象
#     merged_mesh = merge_meshes(mesh_with_texture, mesh_without_texture)
#
#     # 保存合并后的OBJ文件
#     o3d.io.write_triangle_mesh(r"C:\Users\mj\Code\Obj\merged_output.obj", merged_mesh)
#
# if __name__ == "__main__":
#     main()

# import math
#
# def make_rotate(rx, ry, rz):
#     sinX = np.sin(rx)
#     sinY = np.sin(ry)
#     sinZ = np.sin(rz)
#
#     cosX = np.cos(rx)
#     cosY = np.cos(ry)
#     cosZ = np.cos(rz)
#
#     Rx = np.zeros((3, 3))
#     Rx[0, 0] = 1.0
#     Rx[1, 1] = cosX
#     Rx[1, 2] = -sinX
#     Rx[2, 1] = sinX
#     Rx[2, 2] = cosX
#
#     Ry = np.zeros((3, 3))
#     Ry[0, 0] = cosY
#     Ry[0, 2] = sinY
#     Ry[1, 1] = 1.0
#     Ry[2, 0] = -sinY
#     Ry[2, 2] = cosY
#
#     Rz = np.zeros((3, 3))
#     Rz[0, 0] = cosZ
#     Rz[0, 1] = -sinZ
#     Rz[1, 0] = sinZ
#     Rz[1, 1] = cosZ
#     Rz[2, 2] = 1.0
#
#     R = np.matmul(np.matmul(Rz, Ry), Rx)
#     return R

import numpy as np
import open3d as o3d
import trimesh

def load_obj(file_path):
    mesh = trimesh.load(file_path)
    return mesh

def load_obj_with_texture(file_path):
    mesh = o3d.io.read_triangle_mesh(file_path)
    return mesh

def map_vertices_to_texture_coordinates(vertices, triangle_uvs1):
    mapped_texture_coordinates = vertices + triangle_uvs1
    return np.array(mapped_texture_coordinates)

def merge_meshes(mesh1, mesh2):
    # 获取顶点和面信息
    vertices1 = np.asarray(mesh1.vertices)
    triangles1 = np.asarray(mesh1.triangles)
    triangle_uvs1 = np.asarray(mesh1.triangle_uvs)
    vertex_normals1 = np.asarray(mesh1.vertex_normals)

    v2 = mesh2.vertices
    f2 = mesh2.faces
    v2 = np.array(v2)
    f2 = np.array(f2)

    # 映射new.obj的顶点到model.obj的纹理坐标
    # mapped_texture_coordinates = map_vertices_to_texture_coordinates(v2, triangle_uvs1)

    # 合并顶点和面
    f2 = np.array(f2) + np.shape(vertices1)[0]
    v = np.concatenate((vertices1, v2), axis=0)
    f = np.concatenate((triangles1, f2), axis=0)

    # 合并纹理坐标
    # if len(triangle_uvs1) > 0:
    #     triangle_uvs_combined = np.hstack((triangle_uvs1, mapped_texture_coordinates))
    # else:
    #     triangle_uvs_combined = np.zeros_like(mapped_texture_coordinates)

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
    # 加载带有纹理信息的OBJ文件
    mesh_with_texture = load_obj_with_texture(r"C:\Users\mj\Code\Obj\OBJ\3143415262517261-20-962\model.obj")

    # 加载没有纹理信息的OBJ文件
    mesh_without_texture = load_obj(r"C:\Users\mj\Code\Obj\OBJ\new.obj")

    # 合并两个Mesh对象
    merged_mesh = merge_meshes(mesh_with_texture, mesh_without_texture)

    # 保存合并后的OBJ文件
    # o3d.io.write_triangle_mesh(r"C:\Users\mj\Code\Obj\merged_output.obj", merged_mesh)
    merged_mesh.export(r"C:\Users\mj\Code\Obj\merge1.obj")

if __name__ == "__main__":
    main()
