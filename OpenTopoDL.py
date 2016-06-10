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
import urllib
import cookielib
import os

# Globals #
lidar_name_list = []
lidar_ID_list = []
lidar_private_bit_list = []
lidar_DL_URL_list = []

#Determine whether the user wants to download Lidar Point Cloud data or Raster Data
#lidar_raster == "PC_Bulk" --> Lidar Point Cloud data
#lidar_raster == "Raster" --> Raster data
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

#Shear HTML code (formatted as str) to extract the data's long name
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

#Shear the HTML code (formatted as str) to extract the data's ID number
def ID_shearer(original_str):
	global lidar_ID_list

	stopper = True
	iterr = 0
	while stopper == True:
		if iterr == 7:
			sheared_string = original_str[original_str.find('AS.') + 3:original_str.find('>') - 1]
			lidar_ID_list.append(sheared_string)
			stopper = False
		else:
			index = original_str.index('>')
			shorter_str = original_str[index + 1:]
			iterr = iterr + 1
			original_str = shorter_str

#Create the URL associated with the data's downloadable files
def DL_URL_creator(lidar_raster, requested_id, user_request, lidar_matrix):
	global lidar_DL_URL_list
	global lidar_private_bit_list
	global lidar_ID_list

	short_name_line = 9
	short_name_shear = 29

	if lidar_raster == "PC_Bulk":
		orig_page_URL = "http://opentopo.sdsc.edu/datasetMetadata?otCollectionID=OT." + requested_id
		if lidar_private_bit_list[user_request] == 0:
			orig_page = urllib2.urlopen(orig_page_URL)
			orig_soup = BeautifulSoup(orig_page, "lxml")
			div = str(orig_soup.find('div', class_ = 'well'))
			log = open("log.txt", "w")
			log.write(div)
			log.close()
			f = open('log.txt')
			lines = f.readlines()
			line = lines[short_name_line]
			short_name = line[short_name_shear:]
			f.close()
			os.remove('log.txt')
			short_name = short_name.rstrip()
			return short_name
		else:
			print "Dataset is private and unavailable for download"

#Format long names and list the data available on OpenTopography
#Additionally, add a bit associated with the data to see if it is private or not
def area_listing(lidar_raster):
	global lidar_name_list
	global lidar_private_bit_list

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

		print "\n"
		print "* indicates the dataset is PRIVATE and unavailable for download"
		print "\n"

		for i in range(0, len(lidar_name_list)):
			if len(lidar_name_list[i]) < non_private_threshold:
				lidar_private_bit_list.append(0)
				print str(i + 1) + ":", lidar_name_list[i]
			else:
				string = lidar_name_list[i]
				string = string[:private_shear]
				lidar_name_list[i] = string
				lidar_private_bit_list.append(1)
				print str(i + 1) + "*:", lidar_name_list[i]

		print "\n"
		user_request = raw_input("Requested dataset's number entry: ")
		print "\n"

		return int(user_request) - 1



#Creates a dataframe with the data's associated long name, ID number, and private bit
def lidar_array_maker(name_list, ID_list, private_bit_list, matrix):
	global lidar_name_list
	global lidar_ID_list
	global lidar_private_bit_list

	name_list = lidar_name_list
	ID_list = lidar_ID_list
	private_bit_list = lidar_private_bit_list
	lidar_matrix = matrix

	name_array = np.asarray(name_list)
	ID_array = np.asarray(ID_list)
	private_bit_array = np.asarray(private_bit_list)

	data = { 	'name': name_array,
				'ID': ID_array,
				'private_bit': private_bit_array}
	lidar_matrix = pd.DataFrame(data, columns = ['name', 'ID', 'private_bit'])

	return lidar_matrix

def downloader(lidar_raster, short_name):

	if lidar_raster == "PC_Bulk":
		URL = "https://cloud.sdsc.edu/v1/AUTH_opentopography/PC_Bulk/" + short_name + "/"
		page = urllib2.urlopen(URL)
		soup = BeautifulSoup(page, "lxml")
		entries = soup.findAll('tr', class_="item type-application type-octet-stream")

		print "Downloading " + str(len(entries)) + " files"
		print "\n"

		for i in range(0, len(entries)):
			file = entries[i].a["href"]
			URL_with_file = URL + file
			print file
			wget.download(URL_with_file)
			print "\n"


def main(argv):
	# Globals #
	global lidar_name_list
	global lidar_ID_list
	global lidar_private_bit_list

	# Vars #
	lidar_raster = 0			#Boolean condition to check if user wants lidar or raster data. "PC_Bulk" = lidar. "Raster" = raster
	user_request = 0			#Number corresponding to the dataset the user wants to download
	lidar_matrix = 0			#Dataframe used to store dataset's long name, ID, and private bit

	print "\n"
	print "OpenTopo Downloader - Python script to download data from OpenTopography"
	print "When asked for user input, please enter the corresponding letter/number in the square brackets, []\n"

	lidar_raster = lidar_vs_raster()
	user_request = area_listing(lidar_raster)
	lidar_matrix = lidar_array_maker(lidar_name_list, lidar_ID_list, lidar_private_bit_list, lidar_matrix)
	requested_id = lidar_matrix.loc[user_request][1]
	short_name = DL_URL_creator(lidar_raster, requested_id, user_request, lidar_matrix)
	downloader(lidar_raster, short_name)


if __name__ == "__main__":
	main(sys.argv)