import numpy as np
import trimesh
import math

def load_obj(file_path):
    mesh = trimesh.load(file_path)
    return mesh

def merge_meshes(mesh2,path):

    vts = []
    # faces = []
    v2 = mesh2.vertices
    max_v2 = np.max(v2,axis=0)
    min_v2 = np.min(v2,axis=0)
    R = 6371070
    lat_max = math.asin(max_v2[2]/R)*180/math.pi - 0.0001
    lon_max = math.acos(max_v2[0]/(math.cos(math.asin(max_v2[2]/R))*R))*180/math.pi
    lat_min = math.asin(min_v2[2] / R) * 180 / math.pi
    lon_min = math.acos(min_v2[0] / (math.cos(math.asin(min_v2[2] / R)) * R)) * 180 / math.pi
    faces = mesh2.faces
    normals = mesh2.vertex_normals
    for i in v2:
        vt = []
        if math.sqrt(i[0]**2+i[1]**2+i[2]**2)>6371090:
            R = 6371100
        else:
            R = 6371070
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

        for face in faces:
            f.write(f"f {face[0]+1}/{face[0]+1}/{face[0]+1} {face[1]+1}/{face[1]+1}/{face[1]+1} {face[2]+1}/{face[2]+1}/{face[2]+1}\n")

    f2 = mesh2.faces
    v2 = np.array(v2)
    f2 = np.array(f2)

def main():
    # 加载没有纹理信息的OBJ文件
    mesh_without_texture = load_obj(r"C:\Users\mj\Code\Obj\merge1.obj")
    outfile_obj = r"C:\Users\mj\Code\Obj\new_obj2.obj"
    # 合并两个Mesh对象
    merge_meshes(mesh_without_texture,outfile_obj)

if __name__ == "__main__":
    main()