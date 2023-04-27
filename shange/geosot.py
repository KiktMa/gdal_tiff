from math import floor


# 将经纬度转换成度分秒格式 D° M' S"
def decimal_degree_to_dms(decimal_degree):
    degree = int(decimal_degree)
    minute = int((decimal_degree - degree) * 60)
    second = round(((decimal_degree - degree) * 60 - minute) * 60, 2)
    return degree, minute, second


# 将度分秒格式的经纬度转换为 GeoSOT编码值
def dms_to_geosot(d, m, s):
    geosot = (d * 64 * 64 + m * 64 + s) * 2048
    return geosot


# 计算 GeoSOT 剖分在层级 level 的单元面片大小 Cellsize
def calculate_cellsize(level):
    cellsize = 360 / (2 ** level)
    return cellsize


# 将 LGeoSOT/Cellsize 和 BGeoSOT/Cellsize 转成二进制
def geosot_to_binary(geosot, cellsize, level):
    binary = format(floor(geosot / cellsize), '0{}b'.format(level - 1))
    return binary


# 将二进制转换为四进制一维编码 PGeoSOT4
def binary_to_pgeosot(binary):
    pgeosot = ''
    for i in range(0, len(binary), 2):
        if i == len(binary) - 1:
            pgeosot += str(int(binary[i], 2))
        else:
            pgeosot += str(int(binary[i:i + 2], 2))
    return pgeosot


# 将经纬度转换为最终结果
def geocode_to_final_result(l, b, level):
    # 转换经纬度为度分秒格式
    l_degree, l_minute, l_second = decimal_degree_to_dms(l)
    b_degree, b_minute, b_second = decimal_degree_to_dms(b)

    # 计算 LGeoSOT 和 BGeoSOT 的值
    l_geosot = dms_to_geosot(l_degree, l_minute, l_second)
    b_geosot = dms_to_geosot(b_degree, b_minute, b_second)

    # 计算单元面片大小 Cellsize
    cellsize = calculate_cellsize(level)

    # 将 LGeoSOT/Cellsize 和 BGeoSOT/Cellsize 转成二进制
    l_binary = geosot_to_binary(l_geosot, cellsize, level)
    b_binary = geosot_to_binary(b_geosot, cellsize, level)

    # 将二进制转换为四进制一维编码 PGeoSOT4
    pgeosot = binary_to_pgeosot(l_binary + b_binary)

    # 返回最终结果
    return 'G' + pgeosot


# 示例
l = 116.407413
b = 39.904214
level = 15
result = geocode_to_final_result(l, b, level)
print(result)
