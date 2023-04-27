from osgeo import gdal

# 指定tif文件路径
tif_file = "D:\\JavaConsist\MapData\\newAlgorithmDiagram\\object_slope_trafficable_accessment_60_slope\\object_slope_trafficable_accessment_60_slope.tif"

# 打开tif文件
dataset = gdal.Open(tif_file)

# 获取第一个波段
band = dataset.GetRasterBand(1)

# 获取nodata值
nodata = band.GetNoDataValue()
print("nodata value:", nodata)
