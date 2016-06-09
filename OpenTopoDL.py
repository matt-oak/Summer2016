#OpenTopo Downloader
#Python script to download data from OpenTopography (http://opentopo.sdsc.edu/)
#
#Author: Matt Oakley
#Date of Creation: 06/08/2016

# Imports #
from bs4 import BeautifulSoup
import urllib2
import sys
import wget
import re
import numpy as np
import pandas as pd

lidar_name_list = []
lidar_ID_list = []
lidar_private_bit_list = []
lidar_matrix = []

def lidar_vs_raster():
	lidar_raster = 0

	user_input = raw_input("Download [L]idar Point Cloud or [R]aster data: ")
	if user_input == "L" or user_input == "l":
		lidar_raster = "PC_Bulk"
		return lidar_raster
	elif user_input == "R" or user_input == "r":
		lidar_raster = "Raster"
		return lidar_raster
	else:
		print "Invalid input."
		lidar_vs_raster()

def name_shearer(original_str):
	global lidar_name_list
	stopper = True
	iterr = 0
	while stopper == True:
		if iterr == 8:
			sheared_string = original_str[:-17]
			lidar_name_list.append(sheared_string)
			stopper = False
		else:
			index = original_str.index('>')
			shorter_str = original_str[index+1:]
			iterr = iterr + 1
			original_str = shorter_str

def ID_shearer(original_str):
	global lidar_ID_list
	stopper = True
	iterr = 0
	while stopper == True:
		if iterr == 7:
			sheared_string = original_str[original_str.find('open'):original_str.find('>') - 1]
			lidar_ID_list.append(sheared_string)
			stopper = False
		else:
			index = original_str.index('>')
			shorter_str = original_str[index + 1:]
			iterr = iterr + 1
			original_str = shorter_str


def area_listing(lidar_raster):
	global lidar_name_list
	global lidar_private_bit_list
	global lidar_matrix

	non_private_threshold = 200
	private_shear = -348

	if lidar_raster == "PC_Bulk":
		lidar_url = "http://opentopo.sdsc.edu/lidar"
		lidar_page = urllib2.urlopen(lidar_url)
		lidar_soup = BeautifulSoup(lidar_page, "lxml")
		table = lidar_soup.find("table", class_= "table table-hover table-condensed table-striped table-nospace")
		for row in table.findAll("tr"):
			cells = row.findAll("td")
			cells_str = str(cells)
			if "small text-right text-muted" in cells_str:
				name_shearer(cells_str)
				ID_shearer(cells_str)
		for i in range(0, len(lidar_name_list)):
			if len(lidar_name_list[i]) < non_private_threshold:
				#print str(i + 1) + ":", lidar_name_list[i]
				lidar_private_bit_list.append(0)
				#print str(i + 1) + ":", lidar_ID_list[i]
			else:
				string = lidar_name_list[i]
				string = string[:private_shear]
				lidar_name_list[i] = string
				#print str(i + 1) + ":", string[:private_shear], " ****** [PRIVATE] - Unavailable for Download"
				lidar_private_bit_list.append(1)
				#print str(i + 1) + ":", lidar_ID_list[i]


def lidar_array_maker(name_list, ID_list, private_bit_list):
	global lidar_name_list
	global lidar_ID_list
	global lidar_private_bit_list
	global lidar_matrix

	name_list = lidar_name_list
	ID_list = lidar_ID_list
	private_bit_list = lidar_private_bit_list

	name_array = np.asarray(name_list)
	ID_array = np.asarray(ID_list)
	private_bit_array = np.asarray(private_bit_list)

	data = { 	'name': name_array,
				'ID': ID_array,
				'private_bit': private_bit_array}
	lidar_matrix = pd.DataFrame(data, columns = ['name', 'ID', 'private_bit'])

	print lidar_matrix

def main(argv):
	# Globals #
	global lidar_name_list
	global lidar_ID_list
	global lidar_private_bit_list
	global lidar_matrix

	# Vars #
	lidar_raster = 0			#Boolean condition to check if user wants lidar or raster data. "PC_Bulk" = lidar. "Raster" = raster

	print "\n"
	print "OpenTopo Downloader - Python script to download data from OpenTopography"
	print "When asked for user input, please enter the corresponding letter/number in the square brackets, []\n"

	lidar_raster = lidar_vs_raster()
	area_listing(lidar_raster)
	lidar_array_maker(lidar_name_list, lidar_ID_list, lidar_private_bit_list)


if __name__ == "__main__":
	main(sys.argv)