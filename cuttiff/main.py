# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from osgeo import gdal
import os
import numpy as np

os.environ['PROJ_LIB'] = r'D:\app\anaconda\Lib\site-packages\osgeo\data\proj'

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def read_tif(file_path):
    dataset = gdal.Open(file_path)

    im_width = dataset.RasterXSize  # 栅格矩阵的列数
    im_height = dataset.RasterYSize  # 栅格矩阵的行数

    im_geotrans = dataset.GetGeoTransform()  # 仿射矩阵
    im_proj = dataset.GetProjection()  # 地图投影信息
    im_data = dataset.ReadAsArray(0, 0, im_width, im_height)  # 将数据写成数组，对应栅格矩阵

    del dataset
    return im_geotrans,im_proj,im_data
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    dataset = gdal.Open(r"D:\test_tif\tif5\test113.tif")
    minx, xres, xskew, maxy, yskew, yres = dataset.GetGeoTransform()
    geotrans,pproj,data = read_tif(r"D:\test_tif\tif5\test113.tif")

    print(geotrans)
    print(pproj)
    print("---------------------------------")
    dataset1 = gdal.Open(r"D:\JavaConsist\MapData\newAlgorithmDiagram\threat_area.tif")
    minx1, xres1, xskew1, maxy1, yskew1, yres1 = dataset1.GetGeoTransform()
    geotrans1, pproj1, data1 = read_tif(r"D:\JavaConsist\MapData\newAlgorithmDiagram\threat_area.tif")
    print(geotrans1)
    print(pproj1)
    print(geotrans1)
    print(data.shape)
    # print(0.49897450980406854*1540,0.4989745098040664*1797)
# ROJCS["CGCS2000 / 3-degree Gauss-Kruger CM 93E",GEOGCS["China Geodetic Coordinate System 2000",DATUM["China_2000",
# SPHEROID["GRS 1980",6378137,298.257222101004,AUTHORITY["EPSG","7019"]],AUTHORITY["EPSG","1043"]],
# PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4490"]],
# PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",93],
# PARAMETER["scale_factor",1],PARAMETER["false_easting",500000],PARAMETER["false_northing",0],UNIT["metre",1,
# AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],AXIS["Northing",NORTH],AUTHORITY["EPSG","4540"]]


# PROJCS["CGCS2000 / 3-degree Gauss-Kruger CM 93E",GEOGCS["China Geodetic Coordinate System 2000",DATUM["China_2000",
# SPHEROID["CGCS2000",6378137,298.257222101],AUTHORITY["EPSG","1043"]],PRIMEM["Greenwich",0],UNIT["Degree",0.0174532925199433]],
# PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",93],
# PARAMETER["scale_factor",1],PARAMETER["false_easting",500000],PARAMETER["false_northing",0],UNIT["metre",1,
# AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],AXIS["Northing",NORTH]]


# "POINT(398946.8066990252 3058340.462749814)"
# "POINT(399202.7806225547 3058340.462749814)"
# "POINT(399714.72846961365 3057572.5409792257)"