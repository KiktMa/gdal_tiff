from osgeo import gdal
import numpy as np
import pyproj

gdal.AllRegister()
filePath = r'D:\JavaConsist\MapData\out1part2.tif'
dataset = gdal.Open(filePath)

adfGeoTransform = dataset.GetGeoTransform()
adfGeoTransform = list(adfGeoTransform)
adfGeoTransform[0], adfGeoTransform[3] = 398946.8066990252, 3058340.462749814
proj = dataset.GetProjection()

# 左上角地理坐标
print(adfGeoTransform[0])
print(adfGeoTransform[3])

nXSize = dataset.RasterXSize #列数
nYSize = dataset.RasterYSize #行数

arrSlope = [] # 用于存储每个像素的（X，Y）坐标
for i in range(nYSize):
    row = []
    for j in range(nXSize):
        px = adfGeoTransform[0] + i * adfGeoTransform[1] + j * adfGeoTransform[2]
        py = adfGeoTransform[3] + i * adfGeoTransform[4] + j * adfGeoTransform[5]
        col = [px, py]
        row.append(col)
    arrSlope.append(row)

print(len(arrSlope))
a = np.array(arrSlope)


# 地理坐标和投影坐标之间的转换
'''
utm_proj=pyproj.Proj('+proj=utm +zone=31 +ellps=WGS84')
utm_proj=pyproj.Proj(proj='utm',zone=31,ellps='WGS84')
# '''
# utm_proj=pyproj.Proj(init='epsg:32631')
# x,y=utm_proj(2.294694,48.858093)
# print(x,y)
# a,b=utm_proj(x,y,inverse=True)
# print(a,b)
CGCS_proj = pyproj.Proj(init='epsg:4490')
# CGCS_proj=pyproj.Proj(init='epsg:4326')
# CGCS_proj=pyproj.Proj(init='epsg:4540')
x, y = CGCS_proj(27.63178308333333, 91.97961677777778, inverse=True)
print(x, y)

res = np.zeros((len(a), len(a[0]), len(a[0, 0])))
for i in range(len(a)):
    for j in range(len(a[0])):
        x, y = CGCS_proj(a[i, j, 0], a[i, j, 1], inverse=True)
        # res[i, j, 0], res[i, j, 1] = x + 0.00000025*(i+1), y + 0.00000025*(j+1)
        res[i, j, 0], res[i, j, 1] = x, y

res1 = res.transpose(2, 0, 1)
print(len(np.unique(res1)))
print(len(a) + len(a[0]))

print(res1[0, 0, 0], res1[1, 0, 0])
print(res1[0, -1, -1], res1[1, -1, -1])

# 保存文件
np.savetxt(r'D:lon.txt', res1[0, :, 0], fmt='%.08f')
np.savetxt(r'D:lat.txt', res1[1, 0, :], fmt='%.08f')

# #第二种转换方法，支持对投影坐标以及投影坐标之间的互相转换
# wgs84=pyproj.Proj('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs ')
# proj1=pyproj.Proj('+proj=utm +zone=31 +ellps=WGS84')
# x1,y1=pyproj.transform(proj1,wgs84,580744.32,4504695.26)
# print(x1,y1)
# x2,y2=utm_proj(580744.32,4504695.26,inverse=True)
# print(x2,y2)
