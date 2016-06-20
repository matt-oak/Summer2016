#Script to compute slope and aspect from DEM data

from __future__ import division
from osgeo import gdal
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib import colors
import math

MISSING_VAL = -32767
DEGREE_CONVERSION = 57.29578

def calculate_slope(data_array):
	num_rows = data_array.shape[0]
	num_cols = data_array.shape[1]
	slope_array = np.zeros((num_rows, num_cols), dtype = int)
	for i in range(1, num_rows - 1):
		for j in range(1, num_cols - 1):
			a = data_array[i - 1][j - 1]
			b = data_array[i - 1][j]
			c = data_array[i - 1][j + 1]
			d = data_array[i][j - 1]
			e = data_array[i][j]
			f = data_array[i][j + 1]
			g = data_array[i + 1][j - 1]
			h = data_array[i + 1][j]
			q = data_array[i + 1][j + 1]
			
			if (a != MISSING_VAL and b != MISSING_VAL and c != MISSING_VAL and 
			d != MISSING_VAL and e != MISSING_VAL and f != MISSING_VAL and 
			g != MISSING_VAL and h != MISSING_VAL and q != MISSING_VAL):
				
				x_deriv = (c + (2 * f) + q - a - (2 * d) - g) / 8
				x_deriv_squared = math.pow(x_deriv, 2)
				y_deriv = (g + (2 * h) + q - a - (2 * b) - c) / 8
				y_deriv_squared = math.pow(y_deriv, 2)
				
				rise_run = math.sqrt(x_deriv_squared + y_deriv_squared)
				slope_degrees = math.atan(rise_run) * DEGREE_CONVERSION
				
				slope_array[i][j] = slope_degrees
			
			else:
				
				slope_array[i][j] = 0
	
	return slope_array
		
def visualize_slope(slope_array, filename):
	color_map = ListedColormap(['white', 'green', 'limegreen', 'lime', 
		'greenyellow', 'yellow', 'gold', 'orange', 'orangered', 'red'])
	color_bounds = [0, 1, 10, 20, 30, 40, 50, 60, 70, 80, 90]
	color_norm = colors.BoundaryNorm(color_bounds, color_map.N)
	
	img = plt.imshow(slope_array, interpolation = 'nearest', origin = 'lower', 
		cmap = color_map, norm = color_norm)
	plt.colorbar(img, cmap = color_map, norm = color_norm, boundaries = color_bounds, 
		ticks = color_bounds)
	plt.axis('off')
	plt.savefig(filename + '_slope.png')
	
		
def main(argv):
	filename = argv[1]
	data = gdal.Open(filename)
	data_array = np.array(data.GetRasterBand(1).ReadAsArray())
	slope_array = calculate_slope(data_array)
	visualize_slope(slope_array, filename[:-4])

if __name__ == "__main__":
	main(sys.argv)
