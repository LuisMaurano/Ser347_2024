# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 14:06:43 2020

@author: Luis Maurano
"""


import glob
import numpy as np
from osgeo import gdal
from osgeo import osr
import os
import cv2
import skimage as ski
from skimage import data, img_as_float
from skimage import exposure
from check_dir import check
from skimage import io
import matplotlib.pyplot as plt

print(dir(data))

def saveResult (matriz,path,file_out,dataset,colunas,linhas,nbandas,data_type):
    # criar novo dataset 
    tiff_out = path + file_out
    dtype = gdal.GDT_Float32
    dataset_new = driver.Create(tiff_out,colunas,linhas,nbandas,dtype,options=['COMPRESS=LZW'])
    # copiar informações espaciais da banda já existente
    dataset_new.SetGeoTransform(dataset.GetGeoTransform())
    # set no data
    dataset_new.GetRasterBand(1).SetNoDataValue(0)
    # copiar informações de projeção
    dataset_new.SetProjection(dataset.GetProjectionRef())
    # escrever dados da matriz_contraste na banda
    dataset_new.GetRasterBand(1).WriteArray(matriz)
    # salvar valores
    dataset_new.FlushCache()
    # fechar datasets
    dataset_new = None
    dataset = None

# definir driver da gdal
driver = gdal.GetDriverByName('GTiff')

# define caminho para dados
current_directory = os.getcwd()

#verifica se arq existe
path = check()

dirtifs = path + "MASC_*.TIF"

tiffiles = []
bands = []

# define escala e offset para produtos reflectancia L8/L9
scalefactor = 1 # nao necessario pq a banda ja esta corrigida
offset = 0 # nao necessario pq a banda ja esta corrigida

# array com bandas de interesse (valido para landat 8 e 9)
bandas = ["B2","B3","B4","B5","B6","B7"]

i = 0
nbandas = 1

nb = len(bandas) - 1
    
i = 0
nbandas = 1

# cria lista de nome dos tifs de interesse
for f in glob.glob(dirtifs):  # find all png files
        exc_name = os.path.basename(f)
        
        for banda in bandas:
            if banda in exc_name:
                tiffiles.append(exc_name)

print(tiffiles)
#abre lista de tif de interesse
for tiff in tiffiles:
    file_path = path+tiff
    print('Lendo a imagem GeoTIFF',file_path)
    dataset = gdal.Open(file_path)

    geotransform = dataset.GetGeoTransform()
    linhas = dataset.RasterYSize
    colunas = dataset.RasterXSize
    nbandas = 1
    data_type = dataset.GetRasterBand(1).DataType
    srs = osr.SpatialReference()

    band = dataset.GetRasterBand(1)
    img_src = band.ReadAsArray()

    # Contrast stretching
    v_min, v_max = np.percentile(img_src, (0.2, 98.0))
    better_contrast = exposure.rescale_intensity(img_src, in_range=(v_min, v_max))
    matriz = better_contrast
    file_out = tiff.replace('.TIF','_realce_2p.TIF') 
    saveResult (matriz,path,file_out,dataset,colunas,linhas,nbandas,data_type)
    
    #Equalization
    img_eq = exposure.equalize_hist(img_src)
    matriz = img_eq
    file_out = tiff.replace('.TIF','_eqlz.TIF') 
    saveResult (matriz,path,file_out,dataset,colunas,linhas,nbandas,data_type)
    
    #logaritmo
    #img_cast = np.where(img_src  < -0.0, 0, img_src)
    img_log = exposure.adjust_log(img_src)
    matriz = img_log
    file_out = tiff.replace('.TIF','_log.TIF') 
    saveResult (matriz,path,file_out,dataset,colunas,linhas,nbandas,data_type)
    
    # Adaptive Equalization
    img_adapteq = exposure.equalize_adapthist(img_src, clip_limit=0.03)
    file_out = tiff.replace('.TIF','_eqlz_adp.TIF') 
    matriz = img_adapteq
    saveResult (matriz,path,file_out,dataset,colunas,linhas,nbandas,data_type)

    i += 1
    dataset = None
    



