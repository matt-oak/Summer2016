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
import numpy as np
import pandas as pd
import os

# Globals #
lidar_name_list = []
lidar_ID_list = []
lidar_private_bit_list = []

raster_name_list = []
raster_ID_list = []
raster_private_bit_list = []

#========================================================================================
#Function: lidar_vs_raster
#
#input:		None
#desc:		Return a string variable corresponding to whether the user wants Lidar or
#			Raster data
#========================================================================================
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
		main("OpenTopoDL.py")

#========================================================================================
#Function: name_shearer 																#
#																						#
#input:		original_str - HTML code in string format									#
#			lidar_raster - String to determine whether to use Lidar or Raster data 		#
#																						#
#desc: 		Create a list with all the long names associated with the data 				#
#========================================================================================
def name_shearer(original_str, lidar_raster):
	global lidar_name_list
	global raster_name_list

	stopper = True
	iterr = 0

	while stopper == True:
		if iterr == 8:
			sheared_string = original_str[:-17]
			if lidar_raster == "PC_Bulk":
				lidar_name_list.append(sheared_string)
			else:
				raster_name_list.append(sheared_string)
			stopper = False
		else:
			index = original_str.index('>')
			shorter_str = original_str[index + 1:]
			iterr = iterr + 1
			original_str = shorter_str

#========================================================================================
#Function: ID_shearer 																	#
#																						#
#input:		original_str - HTML code in string format 									#
#			lidar_raster - String to determine whether to use Lidar or Raster data 		#
#																						#
#desc:		Create a list with all of the ID numbers associated with the data 			#
#========================================================================================
def ID_shearer(original_str, lidar_raster):
	global lidar_ID_list
	global raster_ID_list

	stopper = True
	iterr = 0
	while stopper == True:
		if iterr == 7:
			if lidar_raster == "PC_Bulk":
				sheared_string = original_str[original_str.find('AS.') + 3:original_str.find('>') - 1]
				lidar_ID_list.append(sheared_string)
			else:
				sheared_string = original_str[original_str.find('EM.') + 3:original_str.find('>') - 1]
				raster_ID_list.append(sheared_string)
			stopper = False
		else:
			index = original_str.index('>')
			shorter_str = original_str[index + 1:]
			iterr = iterr + 1
			original_str = shorter_str

#========================================================================================
#Function: short_name_creator 															#
#																						#
#input:		lidar_raster - String to determine whether the user wants Lidar or 			#
#							Raster data 												#
#			requested_id - ID number associated with the data the user wants 			#
#			user_request - Listing number associated with the data the user wants 		#
# 																						#
#desc:		Find the 'short name' associated the requested data 						#
#========================================================================================
def short_name_creator(lidar_raster, requested_id, user_request):
	global lidar_private_bit_list
	global raster_private_bit_list

	short_name_line = 9
	short_name_shear = 29

	if lidar_raster == "PC_Bulk":
		private_bit_list = lidar_private_bit_list
	elif lidar_raster == "Raster":
		private_bit_list = raster_private_bit_list

	URL = "http://opentopo.sdsc.edu/datasetMetadata?otCollectionID=OT." + requested_id
	if private_bit_list[user_request] == 0:
		page = urllib2.urlopen(URL)
		soup = BeautifulSoup(page, "lxml")
		div = str(soup.find('div', class_ = 'well'))
		log = open("log.txt", "w")
		log.write(div)
		log.close()
		f = open("log.txt")
		lines = f.readlines()
		line = lines[short_name_line]
		short_name = line[short_name_shear:]
		f.close()
		os.remove("log.txt")
		short_name = short_name.rstrip()
		return short_name
	else:
		print "Dataset is private and unavailable for download"

#========================================================================================
#Function: private_bits 																#
#    																					#
#input:		lidar_raster - String to determine whether to work with Lidar or Raster data#
#																						#
#desc: 		Create a list of bits (0 for public, 1 for private) to determine whether	#
#			the dataset is public or private on OpenTopography's website 				#
#========================================================================================
def private_bits(lidar_raster):
	global lidar_name_list
	global lidar_private_bit_list
	global raster_name_list
	global raster_private_bit_list

	non_private_threshold = 200

	if lidar_raster == "PC_Bulk":
		for i in range(0, len(lidar_name_list)):
			if len(lidar_name_list[i]) < non_private_threshold:
				lidar_private_bit_list.append(0)
			else:
				lidar_private_bit_list.append(1)
	else:
		for i in range(0, len(raster_name_list)):
			if len(raster_name_list[i]) < non_private_threshold:
				raster_private_bit_list.append(0)
			else:
				raster_private_bit_list.append(1)

#========================================================================================
#Function: area_listing																	#
#																						#
#input:		lidar_raster - String to determing whether to list Lidar or Raster data     #
#																						#
#desc:		List the available Lidar or Raster datasets on OpenTopography's website     #
#========================================================================================
def area_listing(lidar_raster):
	# Globals #
	global lidar_name_list
	global raster_name_list

	# Vars for extracting the proper information from HTML code
	non_private_threshold = 200
	private_shear = -348

	#Obtain the proper URL and name_list depending on whether the user wants Lidar or Raster data
	if lidar_raster == "PC_Bulk":
		URL = "http://opentopo.sdsc.edu/lidar"
		name_list = lidar_name_list
	elif lidar_raster == "Raster":
		URL = "http://opentopo.sdsc.edu/lidar?format=sd"
		name_list = raster_name_list

	#Find all the datasets listed on OpenTopography's website
	page = urllib2.urlopen(URL)
	soup = BeautifulSoup(page, "lxml")
	table = soup.find("table", class_= "table table-hover table-condensed table-striped table-nospace")
	for row in table.findAll("tr"):
		cells = row.findAll("td")
		cells_str = str(cells)
		if "small text-right text-muted" in cells_str:

			#Extract the proper name and ID from the HTML code
			name_shearer(cells_str, lidar_raster)
			ID_shearer(cells_str, lidar_raster)

	#Determine whether the dataset is public or private
	private_bits(lidar_raster)

	#Print to the user the available datasets
	print "\n"
	print "* indicates the dataset is PRIVATE and unavailable for download"
	print "\n"

	for i in range(0, len(name_list)):
		if len(name_list[i]) < non_private_threshold:
			print str(i + 1) + ":", name_list[i]
		else:
			string = name_list[i]
			string = string[:private_shear]
			name_list[i] = string
			print str(i + 1) + "*:", name_list[i]

	#Obtain and return the user's requested dataset's number
	print "\n"
	user_request = raw_input("Requested dataset's number entry: ")

	return int(user_request) - 1

#========================================================================================
#Function: downloader 																	#
#																						#
#input:		lidar_raster - String to determine whether to DL Lidar or Raster data       #
#			URL - URL to the HTTP directory storing files/sub-directories 				#
#			short_name - Short name corresponding to specific data files on  			#
#							OpenTopography 												#
#																						#
#desc:		Download all files immediately present and within subdirectories on 		#
#			OpenTopography's servers to the local machine with an identical file 		#
#			and subdirectory hierarchy 													#
#========================================================================================
def downloader(lidar_raster, URL, short_name):

	#Obtain the proper, initial URL
	if lidar_raster == "PC_Bulk" and URL == 0:
		URL = "https://cloud.sdsc.edu/v1/AUTH_opentopography/PC_Bulk/" + short_name + "/"
	elif lidar_raster == "Raster" and URL == 0:
		URL = "https://cloud.sdsc.edu/v1/AUTH_opentopography/Raster/" + short_name + "/"

	#Find all files and sub-directories within the HTML of the page
	page = urllib2.urlopen(URL)
	soup = BeautifulSoup(page, "lxml")
	entries = soup.findAll('tr', class_ = "item type-application type-octet-stream")
	sub_dirs = soup.findAll('tr', class_= "item subdir")
	num_sub_dirs = len(sub_dirs)

	#Obtain/create local directories to save files to
	source_directory = os.getcwd()
	data_directory = source_directory + "\\" + short_name

	if os.path.exists(data_directory):
		os.chdir(data_directory)
	else:
		os.makedirs(short_name)
		os.chdir(data_directory)

	#Download all available files
	for i in range(0, len(entries)):
		file = entries[i].a["href"]
		URL_with_file = URL + file
		print URL_with_file
		wget.download(URL_with_file)
		print "\n"

	os.chdir(source_directory)

	#If sub-directories are present, recurse into them
	for i in range(0, num_sub_dirs):
		sub_dir_name = sub_dirs[i].a["href"]
		sub_dir_URL = URL + sub_dir_name
		os.chdir(data_directory)
		downloader(lidar_raster, sub_dir_URL, sub_dir_name)

def main(argv):

	# Globals #
	global lidar_name_list
	global lidar_ID_list
	global lidar_private_bit_list
	global raster_name_list
	global raster_ID_list
	global raster_private_bit_list

	# Vars #
	lidar_raster = 0			#Boolean condition to check if user wants lidar or raster data. "PC_Bulk" = lidar. "Raster" = raster
	user_request = 0			#Number corresponding to the dataset the user wants to download
	lidar_matrix = 0			#Dataframe used to store lidar dataset's long name, ID, and private bit

	print "\n"
	print "OpenTopo Downloader - Python script to download data from OpenTopography"
	print "When asked for user input, please enter the corresponding letter/number in the square brackets, []\n"

	if len(argv) > 1:
		if argv[1] == "l":
			lidar_raster = "PC_Bulk"
		elif argv[1] == "r":
			lidar_raster = "Raster"
		user_request = int(argv[2]) - 1
	else:
		lidar_raster = lidar_vs_raster()
		user_request = area_listing(lidar_raster)

	if lidar_raster == "PC_Bulk":
		requested_id = lidar_ID_list[user_request]
	else:
		requested_id = raster_ID_list[user_request]
	short_name = short_name_creator(lidar_raster, requested_id, user_request)
	downloader(lidar_raster, 0, short_name)


if __name__ == "__main__":
	main(sys.argv)