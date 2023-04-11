import os
from osgeo import gdal

# 定义要切分的影像文件和切分后的影像尺寸
input_file = "D:\\test_tif\\GeoSOT_Standard\\caijian_zhuanhuan.tif"
size = 512

# 打开影像文件
ds = gdal.Open(input_file)

# 获取影像的宽度和高度
width = ds.RasterXSize
height = ds.RasterYSize

# 定义切分后影像的存储路径
output_dir = "D:\\test_tif\\18level"
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# 遍历影像，进行切分
for i in range(width // size):
    for j in range(height // size):
        # 定义切分后影像的文件名
        tile_filename = os.path.join(output_dir, f"{i}_{j}.tif")

        # 切分影像
        gdal.Translate(tile_filename, ds, format="GTiff", srcWin=[i, j, size, size])


print("切割完成")