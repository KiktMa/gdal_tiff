import laspy

# 打开LAS文件
inFile = laspy.read("D:\\JavaConsist\\MapData\\180m_pointcloud\\corrected-LJYY-Cloud-1-0-9.las")

# 获取文件头元数据信息
header = inFile.header
points = inFile.points

print("文件版本号:", header.version)
print("项目ID:", header.point_format)
print("系统标识:", header.system_identifier)
print("生成软件:", header.generating_software)

# 打印点云属性
print("X坐标:", points["X"])
print("Y坐标:", points["Y"])
print("Z坐标:", points["Z"])
print("强度值:", points["intensity"])
print("回波值:", points["return_num"])
print("总回波数:", points["num_returns"])
