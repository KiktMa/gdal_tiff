# -*- coding: utf-8 -*-
import numpy
from osgeo import gdal
import os
os.environ['PROJ_LIB'] = r'D:\app\anaconda\Lib\site-packages\osgeo\data\proj'

# "# 可以切片，但好像也不能根据指定位置进行切"
class GRID:
    # 读图像文件
    def read_img(self, filename):
        dataset = gdal.Open(filename)  # 打开文件
        print("dataset: ", dataset)  # 添加这行进行调试

        im_width = dataset.RasterXSize  # 栅格矩阵的列数
        im_height = dataset.RasterYSize  # 栅格矩阵的行数

        im_geotrans = dataset.GetGeoTransform()  # 仿射矩阵
        im_proj = dataset.GetProjection()  # 地图投影信息
        im_data = dataset.ReadAsArray(0, 0, im_width, im_height)  # 将数据写成数组，对应栅格矩阵
        # band = dataset.GetRasterBand()

        del dataset
        return im_proj, im_geotrans, im_data

    # 写文件，以写成tif为例
    def write_img(self, filename, im_proj, origin_x, origin_y, pixel_width, pixel_height, im_data):
        # gdal数据类型包括
        # gdal.GDT_Byte,
        # gdal .GDT_UInt16, gdal.GDT_Int16, gdal.GDT_UInt32, gdal.GDT_Int32,
        # gdal.GDT_Float32, gdal.GDT_Float64

        # 判断栅格数据的数据类型
        if 'int8' in im_data.dtype.name:
            datatype = gdal.GDT_Byte
        elif 'int16' in im_data.dtype.name:
            datatype = gdal.GDT_UInt16
        else:
            datatype = gdal.GDT_Float32

        # 判读数组维数
        if len(im_data.shape) == 3:
            im_bands, im_height, im_width = im_data.shape
        else:
            im_bands, (im_height, im_width) = 1, im_data.shape

            # 创建文件
        driver = gdal.GetDriverByName("GTiff")  # 数据类型必须有，因为要计算需要多大内存空间
        dataset = driver.Create(filename, im_width, im_height, im_bands, datatype)

        dataset.SetGeoTransform((origin_x, pixel_width, 0, origin_y, 0, pixel_height))  # 写入仿射变换参数
        dataset.SetProjection(im_proj)  # 写入投影

        if im_bands == 1:
            dataset.GetRasterBand(1).WriteArray(im_data)  # 写入数组数据
        else:
            for i in range(im_bands):
                dataset.GetRasterBand(i + 1).WriteArray(im_data[i])

        del dataset

if __name__ == "__main__":
    # os.chdir(r'E:/data')  # 切换路径到待处理图像所在文件夹
    file_name = r"C:\Users\mj\Code\tifdata\taiwan.tif"
    dataset = gdal.Open(file_name)
    minx, xres, xskew, maxy, yskew, yres = dataset.GetGeoTransform()
    proj, geotrans, data= GRID().read_img(file_name)  # 读数据
    # print(proj)
    # print(geotrans)
    # print(data.shape)
    tmp, width, height = data.shape
    size = 1024
    for i in range(height // size):  # 切割成512*512小图
        for j in range(width // size):
            if(j == height//size):
                cur_image = data[:,i * size:(i + 1) * size, j * size:(j + 1) * size]
                lon = minx + xres * size * j
                lat = maxy + yres * (i * size)
                GRID().write_img(r'C:\Users\mj\Code\tifdata\taiwancut/{}_{}.tif'.format(i, j), proj,
                                 lon, lat, xres, yres, cur_image)  # 写数据
            else:
                cur_image = data[:,i*size:(i + 1) * size, j * size:(j + 1) * size]
                lon=minx+xres*size*j
                lat=maxy+yres*(i*size)
                GRID().write_img(r'C:\Users\mj\Code\tifdata\taiwancut/{}_{}.tif'.format(i, j), proj,
                                 lon, lat, xres, yres, cur_image)  # 写数据
    print("批量切割完成")