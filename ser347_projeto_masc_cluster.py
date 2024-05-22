# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 14:06:43 2020

@authors: Luis Maurano, Ana Júlia Dias, Andrés Velastegui-Montoya, Camila Totti, Marina Galdez
"""


import glob
import numpy as np
from osgeo import gdal
import os
from check_dir import check

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

dirtifs = path + "LC09*SR*_AI_N*.TIF"

tiffiles = []
bands = []

# array com bandas de interesse (valido para landat 8 e 9)
bandas = ["B2","B3","B4","B5","B6","B7", "CLUSTER"]
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
    
# recupera matrix das bandas espectrais e indices
B2 = bands[0].astype(float) # banda 2 blue

B3 = bands[1].astype(float) # banda 3 green

B4 = bands[2].astype(float) # banda 4 red

B5 = bands[3].astype(float) # banda 5 nir

B6 = bands[4].astype(float) # banda 6 swir1

B7 = bands[5].astype(float) # banda 7 swir2

CLUSTER = bands[6].astype(float) # banda cluster


# define min max ndvi por classe e filtra matriz

# Cluster 1 e 4 floresta
floresta_cluster_min = 1
floresta_cluster_max = 4
floresta_cluster_boleana1  = 1 * (CLUSTER == floresta_cluster_min)
floresta_cluster_boleana4  = 1 * (CLUSTER == floresta_cluster_max)
floresta_cluster_boleana = floresta_cluster_boleana1 + floresta_cluster_boleana4 

# Cluster 3 agua
agua_cluster_min =  3
agua_cluster_max = 3
agua_cluster_boleana  = 1 * (CLUSTER == agua_cluster_min)

# Cluster 0 area agricola 
usoagricola_cluster_min = 0
usoagricola_cluster_max = 0
usoagricola_cluster_boleana  = 1 * (CLUSTER == usoagricola_cluster_min)

# Cluster 2 area degradacao
degradacao_cluster_min = 2
degradacao_cluster_max = 2
degradacao_cluster_boleana  = 1 * (CLUSTER == degradacao_cluster_min)


i = 0
for i in range(len(bandas) - 1):
    floresta = bands[i] * floresta_cluster_boleana    
    # salva banda
    file_out = "MASC_NDVI_Floresta_" + bandas[i] + ".TIF"
    matriz =  floresta
    saveResult (matriz,path,file_out,dataset,colunas,linhas,nbandas,data_type)
     
    agua = bands[i] * agua_cluster_boleana
    # salva banda
    file_out = "MASC_NDVI_Agua_" + bandas[i] + ".TIF"
    matriz =  agua
    saveResult (matriz,path,file_out,dataset,colunas,linhas,nbandas,data_type)
    
    usoagricola = bands[i] * usoagricola_cluster_boleana
    # salva banda
    file_out = "MASC_NDVI_UsoAgricola_" + bandas[i] + ".TIF"
    matriz =  usoagricola
    saveResult (matriz,path,file_out,dataset,colunas,linhas,nbandas,data_type)
    
    degradacao = bands[i] * degradacao_cluster_boleana
    # salva banda
    file_out = "MASC_NDVI_Degradacao_" + bandas[i] + ".TIF"
    matriz =  degradacao
    saveResult (matriz,path,file_out,dataset,colunas,linhas,nbandas,data_type)
    

