import numpy as np
import trimesh
import math

def load_obj(file_path):
    mesh = trimesh.load(file_path)
    return mesh

def process_obj(input_path, output_path):
    with open(input_path, 'r') as infile:
        lines = infile.readlines()

    # 寻找第一次出现 "usemtl cemian_rgb" 的行
    usemtl_line_index = -1
    for i, line in enumerate(lines):
        if line.startswith("usemtl cemian_rgb"):
            usemtl_line_index = i
            break

    if usemtl_line_index == -1:
        # 如果没有找到 "usemtl cemian_rgb" 行，不进行处理
        with open(output_path, 'w') as outfile:
            outfile.writelines(lines)
        return

    # 找到 "usemtl cemian_rgb" 行后，将其下的所有 "f" 行移动到该行的前面
    f_lines = []
    i = usemtl_line_index + 1
    while i < len(lines) and not lines[i].startswith("usemtl"):
        if lines[i].startswith("f"):
            f_lines.append(lines.pop(i))
        else:
            i += 1

    # 将 "f" 行插入到 "usemtl cemian_rgb" 行的前面
    lines[usemtl_line_index + 1:usemtl_line_index + 1] = f_lines

    # 将处理后的结果写入输出文件
    with open(output_path, 'w') as outfile:
        outfile.writelines(lines)

def merge_meshes(mesh2,path):

    vts = []
    # faces = []
    v2 = mesh2.vertices
    max_v2 = np.max(v2,axis=0)
    min_v2 = np.min(v2,axis=0)
    R = 6371068
    lat_max = math.asin(max_v2[2]/R)*180/math.pi - 0.00002
    lon_max = math.acos(max_v2[0]/(math.cos(math.asin(max_v2[2]/R))*R))*180/math.pi
    lat_min = math.asin(min_v2[2] / R) * 180 / math.pi
    lon_min = math.acos(min_v2[0] / (math.cos(math.asin(min_v2[2] / R)) * R)) * 180 / math.pi
    faces = mesh2.faces
    flag = []
    for face in range(len(faces)):
        a = math.sqrt(v2[faces[face][0]][0]**2+v2[faces[face][0]][1]**2+v2[faces[face][0]][2]**2)
        b = math.sqrt(v2[faces[face][1]][0] ** 2 + v2[faces[face][1]][1] ** 2 + v2[faces[face][1]][2] ** 2)
        c = math.sqrt(v2[faces[face][2]][0] ** 2 + v2[faces[face][2]][1] ** 2 + v2[faces[face][2]][2] ** 2)
        if math.fabs(a-b)<5 and math.fabs(a-c)<5 and math.fabs(b-c)<5:
            continue
        else:
            flag.append(face)
    normals = mesh2.vertex_normals
    for i in v2:
        vt = []
        # if math.sqrt(i[0]**2+i[1]**2+i[2]**2)>6371090:
        #     R = 6371100
        # else:
        #     R = 6371070
        R = math.sqrt(i[0]**2+i[1]**2+i[2]**2)
        # -2994562.87901422
        # 4934768.3642328875 - 2994600.8305515703
        # 4934764.232818925
        lat = math.asin(i[2]/R)*180/math.pi
        lon = math.acos(i[0]/(math.cos(math.asin(i[2]/R))*R))*180/math.pi
        vt1 = 1-((lon-lon_min)/(lon_max-lon_min))
        # if vt1 < 0: vt1 = 0
        # if vt1 > 1: vt1 = 1
        vt.append(vt1)
        vt2 = (lat - lat_min) / (lat_max - lat_min)
        # if vt2 < 0: vt2 = 0
        # if vt2 > 1: vt2 = 1
        vt.append(vt2)
        vts.append(vt)

    with open(path, 'w') as f:
        f.write("mtllib model.mtl\n"
                "usemtl newtiff\n"
                "o planet_newtiff\n")

        for vertex in v2:
            f.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")

        for vt in vts:
            f.write(f"vt {vt[0]} {vt[1]}\n")

        for vn in normals:
            f.write(f"vn {vn[0]} {vn[1]} {vn[2]}\n")

        for face in range(len(faces)):
            if face in flag:
                continue
                # f.write("usemtl cemian_rgb\n")
                # f.write(f"f {faces[face][0]+1}/{faces[face][0]+1}/{faces[face][0]+1} {faces[face][1]+1}/{faces[face][1]+1}/{faces[face][1]+1} {faces[face][2]+1}/{faces[face][2]+1}/{faces[face][2]+1}\n")
            else:
                f.write(f"f {faces[face][0]+1}/{faces[face][0]+1}/{faces[face][0]+1} {faces[face][1]+1}/{faces[face][1]+1}/{faces[face][1]+1} {faces[face][2]+1}/{faces[face][2]+1}/{faces[face][2]+1}\n")

        nnn = 1
        for fl in flag:
            f.write("usemtl cemian_rgb\n")
            f.write(f"v {v2[faces[fl][0]][0]} {v2[faces[fl][0]][1]} {v2[faces[fl][0]][2]}\n")
            f.write(f"v {v2[faces[fl][1]][0]} {v2[faces[fl][1]][1]} {v2[faces[fl][1]][2]}\n")
            f.write(f"v {v2[faces[fl][2]][0]} {v2[faces[fl][2]][1]} {v2[faces[fl][2]][2]}\n")
            f.write("vt 0.0 0.0\n")
            f.write("vt 0 1.0\n")
            f.write("vt 1.0 0\n")
            f.write(f"f {len(v2)+nnn}/{len(v2)+nnn}/{len(v2)+nnn} "
                    f"{len(v2)+nnn+1}/{len(v2)+nnn+1}/{len(v2)+nnn+1} "
                    f"{len(v2)+nnn+2}/{len(v2)+nnn+2}/{len(v2)+nnn+2}\n")
            nnn += 3
            # if face in flag:
            #     f.write("end\n")

    f2 = mesh2.faces
    v2 = np.array(v2)
    f2 = np.array(f2)