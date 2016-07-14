#Characterizing raster data around buffered spatial points
#Author: Matt Oakley

from osgeo import gdal
import numpy as np

def get_buffer_points(raster, coords, radius):
	buffer_list = []
	lower_x = coords[0] - radius
	upper_x = coords[0] + radius
	lower_y = coords[1] - radius
	upper_y = coords[1] + radius
	
	for row in range(lower_x, upper_x + 1):
		for col in range(lower_y, upper_y + 1):
			val = raster[row][col]
			buffer_list.append(val)
			
	buffer_array = np.asarray(buffer_list)
	
	return buffer_array

filename = "front_range.dem"
data = gdal.Open(filename)
data_array = np.array(data.GetRasterBand(1).ReadAsArray())
num_rows = data_array.shape[0]
num_cols = data_array.shape[1]

#See coordinates
#print num_rows
#print num_cols

coords = (100, 200)
radius = 2

buffer_array = get_buffer_points(data_array, coords, radius)
mean = np.mean(buffer_array)
std = np.std(buffer_array)
variance = np.var(buffer_array)

print "Mean: ", mean
print "Standard Deviation: ", std
print "Variance: ", variance





