import numpy as np
import math
import trimesh

def merge_meshes(origin_path,path,outpath):

    vts = []
    # faces = []
    mesh = trimesh.load(path)
    v1all = trimesh.load(origin_path)
    v1 = v1all.vertices
    v2 = mesh.vertices
    max_v2 = np.max(v1, axis=0)
    min_v2 = np.min(v1, axis=0)
    R = 6371068
    lat_max = math.asin(max_v2[2]/R)*180/math.pi - 0.00002
    lon_max = math.acos(max_v2[0]/(math.cos(math.asin(max_v2[2]/R))*R))*180/math.pi
    lat_min = math.asin(min_v2[2] / R) * 180 / math.pi
    lon_min = math.acos(min_v2[0] / (math.cos(math.asin(min_v2[2] / R)) * R)) * 180 / math.pi
    faces = mesh.faces
    flag = []
    for face in range(len(faces)):
        ra = []
        for fa in range(len(faces[face])):
            ra.append(math.sqrt(v2[faces[face][fa]][0]**2+v2[faces[face][fa]][1]**2+v2[faces[face][fa]][2]**2))
        if math.fabs(sum(ra)/len(ra)-ra[0]) < 1:
            continue
        else:
            flag.append(face)
    # normals = mesh.vertex_normals
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

    with open(outpath, 'w') as f:
        f.write("mtllib model.mtl\n"
                "usemtl newtiff\n"
                "o planet_newtiff\n")

        for vertex in v2:
            f.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")

        for vt in vts:
            f.write(f"vt {vt[0]} {vt[1]}\n")

        # for vn in normals:
        #     f.write(f"vn {vn[0]} {vn[1]} {vn[2]}\n")

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
            a = faces[fl]
            f.write(f"v {v2[faces[fl][0]][0]} {v2[faces[fl][0]][1]} {v2[faces[fl][0]][2]}\n")
            f.write(f"v {v2[faces[fl][1]][0]} {v2[faces[fl][1]][1]} {v2[faces[fl][1]][2]}\n")
            f.write(f"v {v2[faces[fl][2]][0]} {v2[faces[fl][2]][1]} {v2[faces[fl][2]][2]}\n")
            # f.write(f"v {v2[faces[fl][3]][0]} {v2[faces[fl][3]][1]} {v2[faces[fl][3]][2]}\n")
            f.write("vt 0.0 0.0\n")
            f.write("vt 0 1.0\n")
            f.write("vt 1.0 0\n")
            f.write(f"f {len(v2)+nnn}/{len(v2)+nnn}/{len(v2)+nnn} "
                    f"{len(v2)+nnn+1}/{len(v2)+nnn+1}/{len(v2)+nnn+1} "
                    f"{len(v2)+nnn+2}/{len(v2)+nnn+2}/{len(v2)+nnn+2}\n")

            nnn += 3
            # if face in flag:
            #     f.write("end\n")

merge_meshes(r"C:\Users\mj\Code\Obj\removeuse\mesh12.obj",r"C:\Users\mj\Desktop\newobj\obj\szf\dantihua\new.obj", r"C:\Users\mj\Desktop\newobj\obj\szf\dantihua\change.obj")