import subprocess

from osgeo import gdal
from osgeo.gdalconst import GA_ReadOnly
import numpy as np


def read_tif(path):
    ds = gdal.Open(path, GA_ReadOnly)
    cols = ds.RasterXSize
    rows = ds.RasterYSize
    counts = ds.RasterCount
    Driver = ds.GetDriver()
    geo = ds.GetGeoTransform()
    proj = ds.GetProjection()
    return ds, cols, rows, counts, Driver, geo, proj


def GetCornerCoordinates(path):
    #返回tif图像角点坐标
    src = gdal.Open(path)
    x0, xres, xrot, y0, yrot, yres  = src.GetGeoTransform()
    w= src.RasterXSize
    h= src.RasterYSize
    # 构造旋转矩阵
    rot = np.array([xres, xrot, yrot, yres]).reshape((2,2))
    # 构造矩阵输入四个角点的像素坐标
    input = np.array([0, 0, w, w, 0, h, 0, h]).reshape((2,4))
    # 构造矩阵输入左上角点的地理坐标
    offset = np.array([x0, y0]).reshape((2,1))
    # 使用矩阵乘法开始转换
    output = np.dot(rot, input) + offset
    # print(output)
    # print('upper left x坐标是{:.3f} y坐标是{:.3f}'.format(output[0,0],output[1,0]))
    # print('upper right x坐标是{:.3f} y坐标是{:.3f}'.format(output[0,2],output[1,2]))
    # print('lower left x坐标是{:.3f} y坐标是{:.3f}'.format(output[0,1],output[1,1]))
    # print('lower right x坐标是{:.3f} y坐标是{:.3f}'.format(output[0,3],output[1,3]))
    return output