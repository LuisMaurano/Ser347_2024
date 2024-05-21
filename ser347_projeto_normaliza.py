# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 14:06:43 2020

@author: Luis Maurano
"""

import glob
import numpy as np
from osgeo import gdal
import os

# salva tiff processado no disco
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
    
# Filtra bandas baseados em limiares min max
def filtra_reflectancia(banda, min, max):
    banda = np.where(banda < min, min, banda)
    banda = np.where(banda > max, max, banda)
    return banda
    
# definir driver da gdal
driver = gdal.GetDriverByName('GTiff')

# define caminho para dados
current_directory = os.getcwd()

#verifica se arq existe
if os.path.isfile(current_directory + "/set_path_dir.txt"):
   infile = open(current_directory + "/set_path_dir.txt", "r")
   path = infile.readline().strip() + "/"
   infile.close()
else:
    print("set_path_dir.txt nao existe em ", current_directory)
    exit()

#verifica se diretorio existe
if os.path.isdir(path) is False:
    print("nao encontrou diretorio em ", path)
    exit()

dirtifs = path + "LC09*SR*B*.TIF"

tiffiles = []
bands = []

# define escala e offset para produtos refectancia L8/L9
scalefactor = 0.0000275
offset = 0.2

# array com bandas de interesse (valido para landat 8 e 9)
bandas = ["B2","B3","B4","B5","B6","B7"]
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
    print("Fazendo....:",tiff)

    dataset = gdal.Open(path + tiff, gdal.GA_ReadOnly)
    # obter metadados da imagem original
    linhas = dataset.RasterYSize
    colunas = dataset.RasterXSize
    nbandas = 1
    #recupera banda como array do tipo inteiro
    data_type = dataset.GetRasterBand(1).DataType
    aux = dataset.GetRasterBand(1)
    #adiciona banda no array de bandas
    bands.append(aux)  
    bands[i]  = aux.ReadAsArray()
    bands[i]  = bands[i].astype(float)
    
    i += 1
   # dataset = None
    
# recupera matrix das bandas espectrais
min = 0.0
max = 1.0

matriz_blue = bands[0].astype(float) * scalefactor + offset # banda 2
file_out = tiff.replace('B7_AI.TIF','B2_AI_N.TIF') #LC09_L2SP_226068_20230821_20230823_02_T1_SR_B7.TIF
banda = matriz_blue
matriz = filtra_reflectancia(banda, min, max)
saveResult (matriz,path,file_out,dataset,colunas,linhas,nbandas,data_type)

matriz_green = bands[1].astype(float) * scalefactor + offset # banda 3
file_out = tiff.replace('B7_AI.TIF','B3_AI_N.TIF') 
banda = matriz_green
matriz = filtra_reflectancia(banda, min, max)
saveResult (matriz,path,file_out,dataset,colunas,linhas,nbandas,data_type)

matriz_red = bands[2].astype(float) * scalefactor + offset # banda 4
file_out = tiff.replace('B7_AI.TIF','B4_AI_N.TIF') 
banda = matriz_red
matriz = filtra_reflectancia(banda, min, max)
saveResult (matriz,path,file_out,dataset,colunas,linhas,nbandas,data_type)

matriz_nir = bands[3].astype(float) * scalefactor + offset # banda 5
file_out = tiff.replace('B7_AI.TIF','B5_AI_N.TIF') 
banda = matriz_nir
matriz = filtra_reflectancia(banda, min, max)
saveResult (matriz,path,file_out,dataset,colunas,linhas,nbandas,data_type)

matriz_swir1 = bands[4].astype(float) * scalefactor + offset # banda 6
file_out = tiff.replace('B7_AI.TIF','B6_AI_N.TIF') 
banda = matriz_swir1
matriz = filtra_reflectancia(banda, min, max)
saveResult (matriz,path,file_out,dataset,colunas,linhas,nbandas,data_type)

matriz_swir2 = bands[5].astype(float) * scalefactor + offset # banda 7
file_out = tiff.replace('B7_AI.TIF','B7_AI_N.TIF') 
banda = matriz_swir2
matriz = filtra_reflectancia(banda, min, max)
saveResult (matriz,path,file_out,dataset,colunas,linhas,nbandas,data_type)



