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
import os
import re

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
#
#desc:		Return a string variable corresponding to whether the user wants Lidar or
#			Raster data
#========================================================================================
def lidar_vs_raster():
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
#Function: short_name_creator 															
#																						
#input:		lidar_raster - String to determine whether the user wants Lidar or 			
#							Raster data 												
#			requested_id - ID number associated with the data the user wants 			
#			user_request - Listing number associated with the data the user wants 	
# 																						
#desc:		Find the 'short name' associated the requested data 						
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
		exit()

#========================================================================================
#Function: private_bits 																
#    																					
#input:		lidar_raster - String to determine whether to work with Lidar or Raster data
#																						
#desc: 		Create a list of bits (0 for public, 1 for private) to determine whether	
#			the dataset is public or private on OpenTopography's website 				
#========================================================================================
def private_bits(lidar_raster):
	# Globals #
	global lidar_name_list
	global lidar_private_bit_list
	global raster_name_list
	global raster_private_bit_list

	name_list = []
	private_bit_list = []

	#Determine which lists to use
	if lidar_raster == "PC_Bulk":
		name_list = lidar_name_list
		private_bit_list = lidar_private_bit_list
	elif lidar_raster == "Raster":
		name_list = raster_name_list
		private_bit_list = raster_private_bit_list

	#Construct the private_bit_list for the specified data format
	for i in range(0, len(name_list)):
		if name_list[i] == " PRIVATE DATASET":
			private_bit_list.append(1)
		else:
			private_bit_list.append(0)

#========================================================================================
#Function: URL_creator
#
#input:		lidar_raster - String to determine whether to work with Lidar or Raster data
#
#desc:		Create the proper URL string and href regex in addition to assigning
#			the proper global name and ID lists
#========================================================================================
def URL_creator(lidar_raster):
	global lidar_name_list
	global lidar_ID_list
	global raster_name_list
	global raster_ID_list

	if lidar_raster == "PC_Bulk":
		URL = "http://opentopo.sdsc.edu/lidar"
		name_list = lidar_name_list
		ID_list = lidar_ID_list
		href = '^/lidarDataset*'
		return URL, name_list, ID_list, href
	elif lidar_raster == "Raster":
		URL = "http://opentopo.sdsc.edu/lidar?format=sd"
		name_list = raster_name_list
		ID_list = raster_ID_list
		href = '^/raster*'
		return URL, name_list, ID_list, href
	else:
		raise Exception('Invalid dataset type')

#========================================================================================
#Function: list_creator
#
#input:		cells - HTML 'a' tags
#			lidar_raster - String to determine whether to work with Lidar or Raster data
#			name_list - List of dataset long names
#			ID_list - List of dataset ID numbers
#
#desc:		Create lists of long names and ID numbers from the acquired HTML
#========================================================================================
def list_creator(cells, lidar_raster, name_list, ID_list):
	for i in range(0, len(cells)):
		long_name = cells[i].string
		if long_name == None:
			name_list.append(" PRIVATE DATASET")
		else:
			name_list.append(long_name)

		if lidar_raster == "PC_Bulk":
			ID = str(cells[i]['href'])[31:]
		elif lidar_raster == "Raster":
			ID = str(cells[i]['href'])[26:]
		ID_list.append(ID)

#========================================================================================
#Function: area_listing																	
#																						
#input:		lidar_raster - String to determing whether to list Lidar or Raster data     
#																						
#desc:		List the available Lidar or Raster datasets on OpenTopography's website and
#			create lists of data's long names, ID numbers, and private bits   
#========================================================================================
def area_listing(lidar_raster, cmd_line):
	# Globals #
	global lidar_name_list
	global raster_name_list
	global lidar_ID_list
	global raster_ID_list

	#Obtain the proper URL, name_list, ID_list, and href regex depending on what data format the user wants
	URL, name_list, ID_list, href = URL_creator(lidar_raster)

	#Find all the datasets listed on OpenTopography's website
	page = urllib2.urlopen(URL)
	soup = BeautifulSoup(page, "lxml")
	table = soup.find("table", class_= "table table-hover table-condensed table-striped table-nospace")
	for row in table.findAll("tr"):
		cells = row.findAll('a', href = re.compile(href))
		list_creator(cells, lidar_raster, name_list, ID_list)

	#Determine whether the dataset is public or private
	private_bits(lidar_raster)

	if cmd_line == 0:
		#Print to the user the available datasets
		print "\n"
		for i in range(0, len(name_list)):
			print str(i + 1) + ":" + name_list[i]

		#Obtain and return the user's requested dataset's number
		print "\n"
		user_request = raw_input("Requested dataset's number entry: ")

		return int(user_request) - 1

#========================================================================================
#Function: downloader 																	
#																						
#input:		lidar_raster - String to determine whether to DL Lidar or Raster data       
#			URL - URL to the HTTP directory storing files/sub-directories 				
#			short_name - Short name corresponding to specific data files on  			
#							OpenTopography 												
#																						
#desc:		Download all files immediately present and within subdirectories on 		
#			OpenTopography's servers to the local machine with an identical file 		
#			and subdirectory hierarchy 													
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

	#Check and see if the local directory currently exists or not
	if os.path.exists(data_directory):
		os.chdir(data_directory)
	else:
		os.makedirs(short_name)
		os.chdir(data_directory)

	#Download all available files
	for i in range(0, len(entries)):
		file = entries[i].a["href"]
		URL_with_file = URL + file
		if file != "log":
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

	lidar_raster = 0			#Boolean condition to check if user wants lidar or raster data. "PC_Bulk" = lidar. "Raster" = raster
	user_request = 0			#Number corresponding to the dataset the user wants to download
	cmd_line = 0				#Boolean corresponding to whether or not the user wants to run the script with 1 command

	#Logic/functions if the user wants to run the script directly from the command line with no user input
	if len(argv) > 1:
		cmd_line = 1
		if argv[1] == "l":
			lidar_raster = "PC_Bulk"
		elif argv[1] == "r":
			lidar_raster = "Raster"
		else:
			print "Invalid input"
		user_request = int(argv[2]) - 1
		area_listing(lidar_raster, cmd_line)

	#Logic/functions if the user does not want to run the script from the command line and wants to have user input
	else:
		print "\n"
		print "OpenTopo Downloader - Python script to download data from OpenTopography"
		print "When asked for user input, please enter the corresponding letter/number in the square brackets, []\n"
		lidar_raster = lidar_vs_raster()
		user_request = area_listing(lidar_raster, cmd_line)

	if lidar_raster == "PC_Bulk":
		requested_id = lidar_ID_list[user_request]
	else:
		requested_id = raster_ID_list[user_request]

	short_name = short_name_creator(lidar_raster, requested_id, user_request)
	downloader(lidar_raster, 0, short_name)


if __name__ == "__main__":
	main(sys.argv)