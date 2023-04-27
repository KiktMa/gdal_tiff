from osgeo import gdal

tif_file = "D:\\JavaConsist\MapData\\newAlgorithmDiagram\\object_slope_trafficable_accessment_60_slope\\object_slope_trafficable_accessment_60_slope.tif"
dataset = gdal.Open(tif_file, gdal.GA_Update)

gt = dataset.GetGeoTransform() # 获取仿射变换参数
x_min = gt[0] # 左上角x坐标
y_max = gt[3] # 左上角y坐标

x_offset = 100 # 填充的x偏移量
y_offset = -100 # 填充的y偏移量

gt_new = list(gt) # 将仿射变换参数转换为列表
gt_new[0] += x_offset * gt[1] # 修改左上角x坐标
gt_new[3] += y_offset * gt[5] # 修改左上角y坐标

dataset.SetGeoTransform(gt_new) # 更新仿射变换参数
dataset.FlushCache() # 刷新缓存

dataset = None
