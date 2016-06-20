#Script to compute slope and aspect from DEM data

from __future__ import division
from osgeo import gdal
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib import colors
from matplotlib import ticker
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
	
def calculate_aspect(data_array):
	num_rows = data_array.shape[0]
	num_cols = data_array.shape[1]
	aspect_array = np.zeros((num_rows, num_cols), dtype = int)
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
				y_deriv = (g + (2 * h) + q - a - (2 * b) - c) / 8
				
				aspect = DEGREE_CONVERSION * math.atan2(y_deriv, (-1 * x_deriv))
				
				if aspect < 0:
					aspect_array[i][j] = 90 - aspect
				elif aspect > 90:
					aspect_array[i][j] = 360 - aspect + 90
				else:
					aspect_array[i][j] = 90 - aspect
			
			else:
				aspect_array[i][j] = 0
	
	return aspect_array
		
def visualize_slope(slope_array, filename):
	color_map = ListedColormap(['white', 'green', 'limegreen', 'lime', 
		'greenyellow', 'yellow', 'gold', 'orange', 'orangered', 'red'])
	color_bounds = [0, 1, 10, 20, 30, 40, 50, 60, 70, 80, 90]
	color_norm = colors.BoundaryNorm(color_bounds, color_map.N)
	
	img = plt.imshow(slope_array, interpolation = 'nearest', origin = 'lower', 
		cmap = color_map, norm = color_norm)
	cbar = plt.colorbar(img, cmap = color_map, norm = color_norm, boundaries = color_bounds, 
		ticks = color_bounds)
		
	plt.axis('off')
	plt.title(filename + " Slope")
	plt.savefig(filename + '_slope.png')
	plt.close()
	
def visualize_aspect(aspect_array, filename):
	color_map = ListedColormap(['white', 'red', 'orange', 'yellow', 'lime', 'cyan', 'cornflowerblue', 
		'blue', 'magenta', 'red'])
	color_bounds = [-1, 0, 22.5, 67.5, 112.5, 157.5, 202.5, 247.5, 292.5, 337.5, 360]
	color_norm = colors.BoundaryNorm(color_bounds, color_map.N)
	
	img = plt.imshow(aspect_array, interpolation = 'nearest', origin = 'lower', 
		cmap = color_map, norm = color_norm)
	cbar = plt.colorbar(img, cmap = color_map, boundaries = color_bounds, ticks = color_bounds)
	cbar.ax.tick_params(length = 0, pad = 5)
	cbar.ax.set_yticklabels(['Flat', 'N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N'])
	
	plt.axis('off')
	plt.title(filename + " Aspect")
	plt.savefig(filename + '_aspect.png')
	plt.close()
		
def main(argv):
	filename = argv[1]
	data = gdal.Open(filename)
	data_array = np.array(data.GetRasterBand(1).ReadAsArray())
	slope_array = calculate_slope(data_array)
	aspect_array = calculate_aspect(data_array)
	visualize_slope(slope_array, filename[:-4])
	visualize_aspect(aspect_array, filename[:-4])

if __name__ == "__main__":
	main(sys.argv)
