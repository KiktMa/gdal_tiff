import removeusemtl
def many_geometry_merge2one(input_paths, output_path):
    # 存储所有集合体的顶点、法线、纹理坐标和面
    all_vertices = []
    all_normals = []
    all_tex_coords = []
    all_faces = []

    for input_path in input_paths:
        with open(input_path, 'r') as file:
            vertices = []
            normals = []
            tex_coords = []
            faces = []

            for line in file:
                parts = line.strip().split()

                if not parts:
                    continue

                if parts[0] == 'v':
                    vertices.append(list(map(float, parts[1:])))
                elif parts[0] == 'vn':
                    normals.append(list(map(float, parts[1:])))
                elif parts[0] == 'vt':
                    tex_coords.append(list(map(float, parts[1:])))
                elif parts[0] == 'f':
                    faces.append([list(map(int, v.split('/'))) for v in parts[1:]])

            all_vertices.extend(vertices)
            all_normals.extend(normals)
            all_tex_coords.extend(tex_coords)
            all_faces.extend(faces)

    # 写入新的OBJ文件
    with open(output_path, 'w') as outfile:
        for vertex in all_vertices:
            outfile.write(f"v {' '.join(map(str, vertex))}\n")
        for normal in all_normals:
            outfile.write(f"vn {' '.join(map(str, normal))}\n")
        for tex_coord in all_tex_coords:
            outfile.write(f"vt {' '.join(map(str, tex_coord))}\n")
        for face in all_faces:
            outfile.write(f"f {' '.join(['/'.join(map(str, v)) for v in face])}\n")

    # 删除合并几何体后的obj中的usemtl行
    removeusemtl.remove_usemtl_lines(output_path, output_path)
# if __name__ == "__main__":
#     input_paths = [r"C:\Users\mj\Code\Obj\OBJ\3143415262517261-20-962\model.obj"]  # 需要合并的OBJ文件路径
#     output_path = r"C:\Users\mj\Code\Obj\OBJ\3143415262517261-20-962\merged_obj.obj"  # 输出OBJ文件路径
#
#     many_geometry_merge2one(input_paths, output_path)
