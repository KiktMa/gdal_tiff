import re

from osgeo import gdal,osr
import numpy as np

def get_elevation(tif_path, latitude, longitude):
    gdal.UseExceptions()
    dataset = gdal.Open(tif_path)

    band = dataset.GetRasterBand(1)
    elevation = band.ReadAsArray()
    nrows, ncols = elevation.shape

    x0, dx, dxdy, y0, dydx, dy = dataset.GetGeoTransform()

    new_ncols, new_nrows = int((y0 - latitude) / dx), int((longitude - x0) / dx)

    return elevation[new_ncols][new_nrows]

def getSRSPair(dataset):
    '''
    获得给定数据的投影参考系和地理参考系
    :param dataset: GDAL地理数据
    :return: 投影参考系和地理参考系
    '''
    prosrs = osr.SpatialReference()
    prosrs.ImportFromWkt(dataset.GetProjection())
    geosrs = prosrs.CloneGeogCS()
    return prosrs, geosrs

def lonlat2geo(dataset, lon, lat):
    '''
    将经纬度坐标转为投影坐标（具体的投影坐标系由给定数据确定）
    :param dataset: GDAL地理数据
    :param lon: 地理坐标lon经度
    :param lat: 地理坐标lat纬度
    :return: 经纬度坐标(lon, lat)对应的投影坐标
    '''
    prosrs, geosrs = getSRSPair(dataset)
    ct = osr.CoordinateTransformation(geosrs, prosrs)
    coords = ct.TransformPoint(lon, lat)
    return coords[:2]

def lat_lon_to_pixel(raster_dataset,location) :
    # from zacharybears.com/using-python-to-translate-latlor-locations-to-pixels-on-a-geotiff
    ds = raster_dataset
    gt = ds.GetGeoTransform()
    srs = osr.SpatialReference()
    srs.ImportFromWkt(ds.GetProjection())
    prosrs, geosrs = getSRSPair(ds)
    ct = osr.CoordinateTransformation(geosrs, prosrs)
    new_location = ct.TransformPoint(location[0], location[1])
    # print(gt[0]+","+gt[3])
    # print(gt[1]+","+gt[5])
    x = (new_location[0] - gt[0]) / gt[1]
    y = (new_location[1] - gt[3]) / gt[5]
    return (int(x), int(y))

# 经纬度点坐标
# 27°37'53.68"N,91°58'50.67"E
if __name__=='__main__':
    lat, lon = 27.630543805555554, 91.97650486111111
    # h = get_elevation('D:\JavaConsist\MapData\out1part2.tif', latitude, longitude)
    location = [lon, lat]
    gdal.AllRegister()
    dataset = gdal.Open(r"D:\JavaConsist\MapData\newAlgorithmDiagram\object_slope_trafficable_accessment_60_slope\object_slope_trafficable_accessment_60_slope.tif")
    print('数据投影：')
    print(dataset.GetProjection())
    print('数据的大小（行，列）：')
    print('(%s %s)' % (dataset.RasterYSize, dataset.RasterXSize))

    print('经纬度 -> 投影坐标：')
    coords = lonlat2geo(dataset, lon, lat)
    print('(%s, %s)->(%s, %s)' % (lon, lat, coords[0], coords[1]))

    print('经纬度 -> 像素坐标：')
    pixel = lat_lon_to_pixel(dataset, location)
    print(pixel)
    print(int(pixel[0] % 513),int(pixel[1] % 513))
