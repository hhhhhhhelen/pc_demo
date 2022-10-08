import os
from glob import glob
from tqdm import tqdm
from base import read_tif
from osgeo import gdal

def new_lbl(i, lbl, outdir_lbl):
    basename = os.path.basen(lbl)
    save_path = os.path.join(outdir_lbl, basename.replace('.tif', str(i)+'.tif'))
    if i == 0:
        start_x = 0
        start_y = 0        
    elif i == 1:
        start_x = 0
        start_y = 512
    elif i == 2:
        start_x = 512
        start_y = 0
    elif i == 3:
        start_x = 512
        start_y = 512
    return start_x, start_y, save_path

def new_img(i, lbl, outdir_img):
    basename = os.path.basen(lbl)
    save_path = os.path.join(outdir_img, basename.replace('.tif', str(i)+'.tif'))
    if i == 0:
        start_x = 0
        start_y = 0        
    elif i == 1:
        start_x = 0
        start_y = 4096
    elif i == 2:
        start_x = 4096
        start_y = 0
    elif i == 3:
        start_x = 4096
        start_y = 4096
    return start_x, start_y, save_path

def run():
    size = 512
    inlbl = glob('./datasets/labels/*.tif')
    outdir_img = './datasets/images512'
    outdir_lbl = './datasets/labels512'

    for lbl in tqdm(inlbl):
        ds_lbl, _, _, counts_lbl, Driver_lbl, geo_lbl, _ = read_tif(lbl)
        ds_img, _, _, counts_img, Driver_img, geo_img, _ = read_tif(lbl.replace('labels','images'))           
        
        for i in range(4):
            # new labels
            start_x, start_y, save_path = new_lbl(i, lbl, outdir_lbl)        
            data_lbl_patch = ds_lbl.ReadAsArray(start_x, start_y, size, size)
            ds_out_lbl = Driver_lbl.Create(save_path, size, size, counts_lbl, gdal.GDT_Byte)
            ds_out_lbl.SetGeoTransform(geo_lbl)                
            band_out_lbl = ds_out_lbl.GetRasterBand(1)       
            band_out_lbl.WriteArray(data_lbl_patch)
            # new images
            start_x, start_y, save_path = new_img(i, lbl, outdir_img)
            data_img_patch = ds_img.ReadAsArray(start_x, start_y, size, size)
            ds_out_img = Driver_img.Create(save_path, size*8, size*8, counts_img, gdal.GDT_Byte)
            ds_out_img.SetGeoTransform(geo_img)
            for bandid in range(counts_img):
                band_out_img = ds_out_img.GetRasterBand(bandid+1)
                band_out_img.WriteArray(data_img_patch[bandid])
        

if __name__ == '__main__':
    run()