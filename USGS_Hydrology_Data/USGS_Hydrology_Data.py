#USGS_Hydro_Viewer [Refined]
#Python script to view real-time hydrology data from USGS
#
#Author: Matt Oakley
#Date of Creation: 07/06/2016

#TODO: Adjust formatting for different data types

# Imports #
from bs4 import BeautifulSoup
import urllib2
import sys
import wget
import os
import codecs

def choose_state():
	states = [
			    ('ak', 'Alaska'),
			    ('al', 'Alabama'),
			    ('az', 'Arizona'),
			    ('ar', 'Arkansas'),
			    ('ca', 'California'),
			    ('co', 'Colorado'),
			    ('ct', 'Connecticut'),
			    ('de', 'Delaware'),
			    ('fl', 'Florida'),
			    ('ga', 'Georgia'),
			    ('hi', 'Hawaii'),
			    ('id', 'Idaho'),
			    ('il', 'Illinois'),
			    ('in', 'Indiana'),
			    ('ia', 'Iowa'),
			    ('ks', 'Kansas'),
			    ('ky', 'Kentucky'),
			    ('la', 'Louisiana'),
			    ('me', 'Maine'),
			    ('md', 'Maryland'),
			    ('ma', 'Massachusetts'),
			    ('mi', 'Michigan'),
			    ('mn', 'Minnesota'),
			    ('ms', 'Mississippi'),
			    ('mo', 'Missouri'),
			    ('mt', 'Montana'),
			    ('ne', 'Nebraska'),
			    ('nv', 'Nevada'),
			    ('nh', 'New Hampshire'),
			    ('nj', 'New Jersey'),
			    ('nm', 'New Mexico'),
			    ('ny', 'New York'),
			    ('nc', 'North Carolina'),
			    ('nd', 'North Dakota'),
			    ('oh', 'Ohio'),
			    ('ok', 'Oklahoma'),
			    ('or', 'Oregon'),
			    ('pa', 'Pennsylvania'),
			    ('ri', 'Rhode Island'),
			    ('sc', 'South Carolina'),
			    ('sd', 'South Dakota'),
			    ('tn', 'Tennessee'),
			    ('tx', 'Texas'),
			    ('ut', 'Utah'),
			    ('vt', 'Vermont'),
			    ('va', 'Virginia'),
			    ('wa', 'Washington'),
			    ('wv', 'West Virginia'),
			    ('wi', 'Wisconsin'),
			    ('wy', 'Wyoming')
	]

	for i in range(0, len(states)):
		print str(i + 1) + ": " + states[i][1]
	
	state_num = int(raw_input("Enter the number of the state you'd like to DL: "))
	state_choice = states[state_num - 1][0]

	return state_choice

def choose_data_type():
	data_types = [
					("flow", "Streamflow Data"),
					("lake", "Lake and Reservoir Data"),
					("precip", "Precipitation Data"),
					("gw", "Groundwater Data"),
					("quality", "Water Quality Data")]

	print "--------------------------------------"
	for i in range(0, len(data_types)):
		print str(i + 1) + ": " + data_types[i][1]

	data_type_num = int(raw_input("Enter the number of the data type you'd like to DL: "))
	data_type_choice = data_types[data_type_num - 1][0]

	return data_type_choice

def create_URL(state_abbrev, data_type):
	URL = "http://waterdata.usgs.gov/" + state_abbrev + "/nwis/current/?type=" + data_type + "&group_key=NONE"
	return URL

def get_HTML(URL):
	page = urllib2.urlopen(URL)
	soup = BeautifulSoup(page, "lxml")
	table = soup.find("table", border = "0", align = "left", cellspacing = "1")
	header = table.find("thead")
	header = header.find("tr")
	column_headers = []
	stripped_column_headers = []
	num_columns = 0
	new_line_shear = 5

	for cols in header.findAll("th"):
		num_columns += 1
		num_words = len(cols.contents)
		column_header = cols.text
		column_header = column_header.encode('utf-8')
		column_header = column_header[new_line_shear - 1:-new_line_shear]
		column_headers.append(column_header)

	for i in range(0, len(column_headers)):
		stripped_header = column_headers[i].strip()
		stripped_column_headers.append(stripped_header)

	element_lists = [[] for _ in range(num_columns)]

	output = open("output.txt", "w")
	list_iterator = 0
	list_iterator2 = -1
	for row in table.findAll("tr"):
		for elements in row.findAll("td"):
			num_list = list_iterator % num_columns
			element_lists[num_list].append(elements.text)
			item = element_lists[num_list][list_iterator2].encode('utf-8')
			header = stripped_column_headers[num_list]
			output.write(header + ": " + item + "\n")
			list_iterator += 1
			if list_iterator % num_columns == 0:
				list_iterator2 += 1
		output.write("--------------------------------------\n")


state_abbrev = choose_state()
data_type = choose_data_type()
URL = create_URL(state_abbrev, data_type)
table_entries = get_HTML(URL)