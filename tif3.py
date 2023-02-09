from osgeo import osr, gdal
import numpy as np
from PIL import Image
import time
from skimage import io
from osgeo import gdal
import os
os.environ['PROJ_LIB'] = r'D:\app\anaconda\Lib\site-packages\osgeo\data\proj'


def get_file_names(data_dir, file_type=['tif', 'tiff']):
    result_dir = []
    result_name = []
    for maindir, subdir, file_name_list in os.walk(data_dir):
        for filename in file_name_list:
            apath = maindir + '/' + filename
            ext = apath.split('.')[-1]
            if ext in file_type:
                result_dir.append(apath)
                result_name.append(filename)
            else:
                pass
    return result_dir, result_name


def get_same_img(img_dir, img_name):
    result = {}
    for idx, name in enumerate(img_name):
        temp_name = ''
        for idx2, item in enumerate(name.split('_')[:-4]):
            if idx2 == 0:
                temp_name = temp_name + item
            else:
                temp_name = temp_name + '_' + item

        if temp_name in result:
            result[temp_name].append(img_dir[idx])
        else:
            result[temp_name] = []
            result[temp_name].append(img_dir[idx])
    return result


def assign_spatial_reference_byfile(src_path, dst_path):
    src_ds = gdal.Open(src_path, gdal.GA_ReadOnly)
    sr = osr.SpatialReference()
    sr.ImportFromWkt(src_ds.GetProjectionRef())
    geoTransform = src_ds.GetGeoTransform()
    dst_ds = gdal.Open(dst_path, gdal.GA_Update)
    dst_ds.SetProjection(sr.ExportToWkt())
    dst_ds.SetGeoTransform(geoTransform)
    dst_ds = None
    src_ds = None


def cut(in_dir, out_dir, file_type=['tif', 'tiff'], out_type='png', out_size=256):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    data_dir_list, _ = get_file_names(in_dir, file_type)
    count = 0
    print('Cut begining for ', str(len(data_dir_list)), ' images.....')
    for each_dir in data_dir_list:
        time_start = time.time()
        # image = np.array(io.imread(each_dir))
        image = np.array(Image.open(each_dir))
        print(image.shape)

        cut_factor_row = int(np.ceil(image.shape[0] / out_size))
        cut_factor_clo = int(np.ceil(image.shape[1] / out_size))
        for i in range(cut_factor_row):
            for j in range(cut_factor_clo):

                if i == cut_factor_row - 1:
                    i = image.shape[0] / out_size - 1
                else:
                    pass

                    if j == cut_factor_clo - 1:
                        j = image.shape[1] / out_size - 1
                    else:
                        pass

                start_x = int(np.rint(i * out_size))
                start_y = int(np.rint(j * out_size))
                end_x = int(np.rint((i + 1) * out_size))
                end_y = int(np.rint((j + 1) * out_size))

                temp_image = image[start_x:end_x, start_y:end_y, :]

                print('temp_image:', temp_image.shape)
                out_dir_images = out_dir + '/' + each_dir.split('/')[-1].split('.')[0] \
                                 + '_' + str(start_x) + '_' + str(end_x) + '_' + str(start_y) + '_' + str(
                    end_y) + '.' + out_type

                out_image = Image.fromarray(temp_image)
                out_image.save(out_dir_images)

                src_path = 'D:\JavaConsist\MapData\out1part2.tif'  # 带地理影像
                assign_spatial_reference_byfile(src_path, out_dir_images)

        count += 1
        print('End of ' + str(count) + '/' + str(len(data_dir_list)) + '...')
        time_end = time.time()
        print('Time cost: ', time_end - time_start)
    print('Cut Finsh!')
    return 0

if __name__ == '__main__':
    ##### cut
    data_dir = 'D:\JavaConsist\MapData'
    out_dir = 'D:\JavaConsist\MapData\out'
    file_type = ['tif']
    out_type = 'tif'
    cut_size = 256

    cut(data_dir, out_dir, file_type, out_type, cut_size)