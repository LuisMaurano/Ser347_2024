"""
Created on Thu Oct 22 14:06:43 2020

@author: Ricardo Cartaxo M Souza
"""

from osgeo import gdal,osr
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import os,sys
from check_dir import check

def cluster_image(image, n_clusters):
# Convertendo a imagem em um array unidimensional
	X = image.reshape((-1, 1))

# Aplicando o algoritmo KMeans para encontrar os clusters
	kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(X)
	labels = kmeans.labels_

# Convertendo os clusters de volta para a forma da imagem
	clustered_image = labels.reshape(image.shape)

	return clustered_image

def cluster_imageg(image, n_clusters):
# Convertendo a imagem em um array unidimensional
	X = image.reshape((-1, 1))

# Aplicando o algoritmo KMeans para encontrar os clusters
	print('cluster_image',image.shape,'->',X.shape)
	flat_pixels_subsets = np.array_split(X, 10)
	results = []
	count = 0
	for subset in flat_pixels_subsets:
		print('count',count,subset.shape)
		result_subset = KMeans(n_clusters=n_clusters, random_state=0).fit(subset)
		results.append(result_subset.labels_)
		count += 1
	labels = np.concatenate(results)
	#labels = kmeans.labels_

	# Convertendo os clusters de volta para a forma da imagem
	clustered_image = labels.reshape(image.shape)

	return clustered_image

def calculate_cluster_values(image, clustered_image):
	cluster_values = []

# Iterar sobre os clusters únicos
	for cluster_id in np.unique(clustered_image):
# Filtrar a região correspondente ao cluster atual
		region = image[clustered_image == cluster_id]

# Calcular os valores mínimo e máximo para o cluster atual
		min_value = np.min(region)
		max_value = np.max(region)
		mean_value = np.mean(region)
		std_value = np.std(region)

		cluster_values.append((cluster_id, min_value, max_value, mean_value, std_value))

	return cluster_values

# define caminho para dados
current_directory = os.getcwd()

#verifica se arq existe
path = check()

file_path = path + "LC09_L2SP_226068_20230821_20230823_02_T1_SR_NDVI_AI_N.TIF"

# Número de clusters desejados
n_clusters = 5 #int(sys.argv[2])

# Lendo a imagem GeoTIFF
print('Lendo a imagem GeoTIFF',file_path)
dataset = gdal.Open(file_path)
geotransform = dataset.GetGeoTransform()
srs = osr.SpatialReference()
srs.ImportFromWkt(dataset.GetProjection())

band = dataset.GetRasterBand(1)
image = band.ReadAsArray()

# Aplicando a clusterização
print('Aplicando a clusterização')
clustered_image = cluster_image(image, n_clusters)

# Salvando a imagem cluster
driver = gdal.GetDriverByName('GTiff')
clufilename = file_path.replace('.TIF','_{}_CLUSTER.TIF'.format(n_clusters))
cludataset = driver.Create( clufilename, dataset.RasterXSize, dataset.RasterYSize, 1, gdal.GDT_Byte,  options = [ 'COMPRESS=DEFLATE' ] )
# Set the geo-transform and srs to the cludataset
cludataset.SetGeoTransform( geotransform )
cludataset.GetRasterBand(1).SetNoDataValue(255)
cludataset.SetProjection ( srs.ExportToWkt() )
cludataset.GetRasterBand(1).WriteArray( clustered_image )
cludataset = None

# Contando o número de clusters distintos na imagem
unique_clusters = np.unique(clustered_image)
num_clusters = len(unique_clusters)

print(f"Número de clusters na imagem: {num_clusters}")

# Calculando os valores de cinza mínimo e máximo para cada cluster
cluster_values = calculate_cluster_values(image, clustered_image)

# Exibindo os valores de cinza mínimo e máximo para cada cluster
for cluster_id, min_value, max_value, mean_value, std_value in cluster_values:
	print(f"Cluster {cluster_id}: Mínimo = {min_value}, Máximo = {max_value}, Média = {mean_value}, Variância = {std_value}")
