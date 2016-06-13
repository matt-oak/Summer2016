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
		main("OpenTopoDL.py")

#Shear HTML code (formatted as str) to extract the data's long name
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

#Shear the HTML code (formatted as str) to extract the data's ID number
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

#Create the URL associated with the data's downloadable files
def DL_URL_creator(lidar_raster, requested_id, user_request, lidar_matrix):
	global lidar_private_bit_list
	global raster_private_bit_list

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

	else:
		orig_page_URL = "http://opentopo.sdsc.edu/datasetMetadata?otCollectionID=OT." + requested_id
		if raster_private_bit_list[user_request] == 0:
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
	global raster_name_list
	global raster_private_bit_list

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
				name_shearer(cells_str, lidar_raster)
				ID_shearer(cells_str, lidar_raster)

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

		return int(user_request) - 1

	elif lidar_raster == "Raster":
		raster_url = "http://opentopo.sdsc.edu/lidar?format=sd"
		raster_page = urllib2.urlopen(raster_url)
		raster_soup = BeautifulSoup(raster_page, "lxml")
		table = raster_soup.find("table", class_ = "table table-hover table-condensed table-striped table-nospace")
		for row in table.findAll("tr"):
			cells = row.findAll("td")
			cells_str = str(cells)
			if "small text-right text-muted" in cells_str:
				name_shearer(cells_str, lidar_raster)
				ID_shearer(cells_str, lidar_raster)

		print "\n"
		print "* indicates the dataset is PRIVATE and unavailable for download"
		print "\n"

		for i in range(0, len(raster_name_list)):
			if len(raster_name_list[i]) < non_private_threshold:
				raster_private_bit_list.append(0)
				print str(i + 1) + ":", raster_name_list[i]
			else:
				string = raster_name_list[i]
				string = string[:private_shear]
				raster_name_list[i] = string
				raster_private_bit_list.append(1)
				print str(i + 1) + "*:", raster_name_list[i]

		print "\n"
		user_request = raw_input("Requested dataset's number entry: ")

		return int(user_request) - 1

#Creates a dataframe with the data's associated long name, ID number, and private bit
def lidar_array_maker(lidar_raster, name_list, ID_list, private_bit_list, matrix):
	global lidar_name_list
	global lidar_ID_list
	global lidar_private_bit_list
	global raster_name_list
	global raster_ID_list
	global raster_private_bit_list

	if lidar_raster == "PC_Bulk":
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

	else:
		name_list = raster_name_list
		ID_list = raster_ID_list
		private_bit_list = raster_private_bit_list
		raster_matrix = matrix

		name_array = np.asarray(name_list)
		ID_array = np.asarray(ID_list)
		private_bit_array = np.asarray(private_bit_list)

		data = {	'name': name_array,
					'ID': ID_array,
					'private_bit': private_bit_array}
		raster_matrix = pd.DataFrame(data, columns = ['name', 'ID', 'private_bit'])

		return raster_matrix

def downloader(lidar_raster, short_name):

	if lidar_raster == "PC_Bulk":
		URL = "https://cloud.sdsc.edu/v1/AUTH_opentopography/PC_Bulk/" + short_name + "/"
		page = urllib2.urlopen(URL)
		soup = BeautifulSoup(page, "lxml")
		entries = soup.findAll('tr', class_="item type-application type-octet-stream")

		print "Prepared to download " + str(len(entries)) + " files"
		user_input = raw_input("Would you like to continue? [y]es or [n]o: ")
		print "\n"

		if user_input == "Y" or user_input == "y":
			source_directory = os.getcwd()
			data_directory = source_directory + "/" + short_name
			if os.path.exists(data_directory):
				os.chdir(data_directory)
			else:
				os.makedirs(short_name)
				os.chdir(data_directory)


			for i in range(0, len(entries)):
				file = entries[i].a["href"]
				URL_with_file = URL + file
				print file
				wget.download(URL_with_file)
				print "\n"

			os.chdir(source_directory)
		else:
			del lidar_name_list[:]
			del lidar_ID_list[:]
			del lidar_private_bit_list[:]
			main("OpenTopoDL.py")


	else:
		URL = "https://cloud.sdsc.edu/v1/AUTH_opentopography/Raster/" + short_name + "/"
		dir_recursive_descent(URL, short_name)

def dir_recursive_descent(dir_URL, short_name):
	page = urllib2.urlopen(dir_URL)
	soup = BeautifulSoup(page, "lxml")
	entries = soup.findAll('tr', class_ = "item type-application type-octet-stream")
	sub_dirs = soup.findAll('tr', class_= "item subdir")
	num_sub_dirs = len(sub_dirs)

	source_directory = os.getcwd()
	data_directory = source_directory + "\\" + short_name

	if os.path.exists(data_directory):
		os.chdir(data_directory)
	else:
		os.makedirs(short_name)
		os.chdir(data_directory)

	for i in range(0, len(entries)):
		file = entries[i].a["href"]
		URL_with_file = dir_URL + file
		print URL_with_file
		wget.download(URL_with_file)
		print "\n"

	os.chdir(source_directory)

	for i in range(0, num_sub_dirs):
		sub_dir_name = sub_dirs[i].a["href"]
		sub_dir_URL = dir_URL + sub_dir_name
		os.chdir(data_directory)
		dir_recursive_descent(sub_dir_URL, sub_dir_name)

def main(argv):

	# Globals #
	global lidar_name_list
	global lidar_ID_list
	global lidar_private_bit_list

	# Vars #
	lidar_raster = 0			#Boolean condition to check if user wants lidar or raster data. "PC_Bulk" = lidar. "Raster" = raster
	user_request = 0			#Number corresponding to the dataset the user wants to download
	lidar_matrix = 0			#Dataframe used to store lidar dataset's long name, ID, and private bit

	print "\n"
	print "OpenTopo Downloader - Python script to download data from OpenTopography"
	print "When asked for user input, please enter the corresponding letter/number in the square brackets, []\n"

	if len(argv) > 1:
		if argv[1] == "l":
			lidar_raster == "PC_Bulk"
		elif argv[1] == "r":
			lidar_raster == "Raster"
		user_request == int(argv[2]) - 1
	else:
		lidar_raster = lidar_vs_raster()
		user_request = area_listing(lidar_raster)

	matrix = lidar_array_maker(lidar_raster, lidar_name_list, lidar_ID_list, lidar_private_bit_list, lidar_matrix)

	if lidar_raster == "PC_Bulk":
		requested_id = matrix.loc[user_request][1]
	else:
		requested_id = matrix.loc[user_request][1]
	short_name = DL_URL_creator(lidar_raster, requested_id, user_request, lidar_matrix)
	downloader(lidar_raster, short_name)


if __name__ == "__main__":
	main(sys.argv)