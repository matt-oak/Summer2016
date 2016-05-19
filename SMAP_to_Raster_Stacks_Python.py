#Matthew Oakley, 05/17/2016
#Python script to convert an SMAP file in h5 format into a raster object

###Prerequisites###
#conda install h5py
#conda install gdal=1.11.2
#conda upgrade numpy
#Add a System variable 'GDAL_DATA' w/ path to directory containing helper files (CSV format) for GDAL

import h5py
from osgeo import gdal
from osgeo import gdal_array
from osgeo import osr
import numpy as np

def smap2raster(inputFile, group, dataset):

	#Read in the SMAP file in h5 format
	h5File = h5py.File(inputFile, 'r')
	
	#Get the data from the specific group/dataset
	data = h5File.get(group + '/' + dataset)
	lat = h5File.get('cell_lat')
	lon = h5File.get('cell_lon')
	
	#Convert this data into numpy arrays
	np_data = np.array(data)
	np_lat = np.array(lat)
	np_lon = np.array(lon)
	
	#Get the spatial extents of the data
	num_cols = np_data.shape[1]
	num_rows = np_data.shape[0]
	xmin = np_lon.min()
	xmax = np_lon.max()
	ymin = np_lat.min()
	ymax = np_lat.max()
	xres = (xmax - xmin)/float(num_cols)
	yres = (ymax - ymin)/float(num_rows)
	
	#Set up the transformation necessary to create the raster
	#Format: (Top left x, West/East pixel resolution, Rotation(0 if N is up), Top left y, Rotation(0 if N is up), North/South pixel resolution)
	geotransform = (xmin, xres, 0, ymax, 0, -yres)
	
	#Create the raster object with the proper coordinate encoding and geographic transformation
	output_raster = gdal.GetDriverByName('GTiff').Create(dataset+'Raster.tif', num_cols, num_rows, 1, gdal.GDT_Float32)
	output_raster.SetGeoTransform(geotransform)
	srs = osr.SpatialReference()
	srs.ImportFromEPSG(4326)
	
	#Export and write the data array to the raster
	output_raster.SetProjection( srs.ExportToWkt() )
	output_raster.GetRasterBand(1).WriteArray(np_data)
	

datasets = ['snow_mass', 'snow_depth']
for i in range(0, len(datasets)):
	smap2raster('SMAP_data.h5', 'Geophysical_Data', datasets[i])













