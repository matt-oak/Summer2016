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

lidar_list = []

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

def shearer(original_str):
	global lidar_list
	stopper = True
	iterr = 0
	while stopper == True:
		if iterr == 8:
			sheared_string = original_str[:-17]
			lidar_list.append(sheared_string)
			stopper = False
		else:
			index = original_str.index('>')
			shorter_str = original_str[index+1:]
			iterr = iterr + 1
			original_str = shorter_str

def area_listing(lidar_raster):
	if lidar_raster == "PC_Bulk":
		lidar_url = "http://opentopo.sdsc.edu/lidar"
		lidar_page = urllib2.urlopen(lidar_url)
		lidar_soup = BeautifulSoup(lidar_page, "lxml")
		table = lidar_soup.find("table", class_= "table table-hover table-condensed table-striped table-nospace")
		for row in table.findAll("tr"):
			cells = row.findAll("td")
			cells_str = str(cells)
			if "small text-right text-muted" in cells_str:
				shearer(cells_str)
		for i in range(0, len(lidar_list)):
			if len(lidar_list[i]) < 200:
				print str(i + 1) + ":", lidar_list[i]
			else:
				string = lidar_list[i]
				print str(i + 1) + ":", string[:-348], " ****** [PRIVATE] - Unavailable for Download"
				


	elif lidar_raster == "Raster":
		print "asdf"

def main(argv):
	# Vars #
	lidar_raster = 0			#Boolean condition to check if user wants lidar or raster data. "PC_Bulk" = lidar. "Raster" = raster

	print "\n"
	print "OpenTopo Downloader - Python script to download data from OpenTopography"
	print "When asked for user input, please enter the corresponding letter/number in the square brackets, []\n"

	lidar_raster = lidar_vs_raster()
	area_listing(lidar_raster)


if __name__ == "__main__":
	main(sys.argv)