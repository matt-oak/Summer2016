#USGS_Hydro_Viewer
#Python script to view real-time hydrology data from USGS
#
#Author: Matt Oakley
#Date of Creation: 07/06/2016

# Imports #
from bs4 import BeautifulSoup
import urllib2
import sys
import wget
import os

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
	
	state_num = int(raw_input("Enter the number of the state you'd like to view: "))
	state_choice = states[state_num - 1][0]

	return state_choice

def get_stations(URL):
	non_blank_entries = []

	page = urllib2.urlopen(URL)
	soup = BeautifulSoup(page, "lxml")
	entries = soup.findAll('area')

	for i in range(0, len(entries)):
		if "hollowdot" in str(entries[i]):
			continue
		else:
			non_blank_entries.append(str(entries[i]))

	print "------------------------------------------------------"
	for i in range(0, len(non_blank_entries)):
		HTML_str = non_blank_entries[i]
		start_index = HTML_str.find('/a&gt;') + 7
		end_index = HTML_str.find('&lt;/caption')
		print str(i + 1) + ": " + HTML_str[start_index:end_index]

	station_num = int(raw_input("Enter the number of the station you'd like to view: ")) - 1
	return non_blank_entries, station_num

def list_station_attributes(entries, station):
	text_file = open("output.txt", "w")
	print "------------------------------------------------------"

	for i in range(0, len(entries)):
		station_str = entries[i]

		start_index = station_str.find('/a&gt;') + 7
		end_index = station_str.find('&lt;/caption')
		station_name = station_str[start_index:end_index]
		if len(station_name) > 70:
			if i == station:
				print "Station Name: NONE"
			text_file.write("Station Name: NONE\n")
		else:
			if i == station:
				print "Station Name: " + station_name
			text_file.write("Station Name: %s\n" % station_name)

		start_index = station_str.find('Drainage area') + 35
		end_index = station_str.find('&lt;sup')
		drainage_area = station_str[start_index:end_index]
		if len(drainage_area) > 30:
			if i == station:
				print "Drainage Area: NONE"
			text_file.write("Drainage Area: NONE\n")
		else:
			if i == station:
				print "Drainage Area: " + drainage_area + "^2"
			text_file.write("Drainage Area: %s^2\n" % drainage_area)

		start_index = station_str.find('Discharge') + 31
		end_index = station_str.find('cfs')
		discharge = station_str[start_index:end_index]
		if len(discharge) > 30:
			if i == station:
				print "Discharge: NONE"
			text_file.write("Discharge: NONE\n")
		else:
			if i == station:
				print "Discharge: " + discharge + "cfs"
			text_file.write("Discharge: %scfs\n" % discharge)

		start_index = station_str.find('Stage') + 27
		end_index = station_str.find('ft')
		stage = station_str[start_index:end_index]
		if len(stage) > 30:
			if i == station:
				print "Stage: NONE"
			text_file.write("Stage: NONE\n")
		else:
			if i == station:
				print "Stage: " + stage + "ft"
			text_file.write("Stage: %sft\n" % stage)

		station_str = station_str[start_index + 10:]

		start_index = station_str.find('Flood stage') + 33
		end_index = station_str.find('ft&lt;')
		flood_stage = station_str[start_index:end_index]
		if len(flood_stage) > 30:
			if i == station:
				print "Flood Stage: NONE"
			text_file.write("Flood Stage: NONE\n")
		else:
			if i == station:
				print "Flood Stage: " + flood_stage + "ft"
			text_file.write("Flood Stage: %sft\n" % flood_stage)

		start_index = station_str.find('Date') + 26
		end_index = start_index + 19
		date = station_str[start_index:end_index]
		if len(date) > 30:
			if i == station:
				print "Date: NONE"
			text_file.write("Date: NONE\n")
		else:
			if i == station:
				print "Date: " + date
			text_file.write("Date: %s\n" % date)

		start_index = station_str.find('Percentile') + 32
		end_index = station_str.find('%&lt;/')
		percentile = station_str[start_index:end_index]
		if len(percentile) > 30:
			if i == station:
				print "Percentile: NONE"
			text_file.write("Percentile: NONE\n")
		else:
			if i == station:
				print "Percentile: " + percentile + "%"
			text_file.write("Percentile: %s %% \n" % percentile)

		if "real02dot" in station_str:
			if i == station:
				print "Class Symbol: BROWN"
			text_file.write("Class Symbol: BROWN\n")
		elif "real03dot" in station_str:
			if i == station:
				print "Class Symbol: RED"
			text_file.write("Class Symbol: RED\n")
		elif "real04dot" in station_str:
			if i == station:
				print "Class Symbol: ORANGE"
			text_file.write("Class Symbol: ORANGE\n")
		elif "real05dot" in station_str:
			if i == station:
				print "Class Symbol: GREEN"
			text_file.write("Class Symbol: GREEN\n")
		elif "real06dot" in station_str:
			if i == station:
				print "Class Symbol: LIGHT BLUE"
			text_file.write("Class Symbol: LIGHT BLUE\n")
		elif "real07dot" in station_str:
			if i == station:
				print "Class Symbol: DARK BLUE"
			text_file.write("Class Symbol: DARK BLUE\n")
		elif "real08dot" in station_str:
			if i == station:
				print "Class Symbol: BLACK"
			text_file.write("Class Symbol: BLACK\n")

		station_str = station_str[start_index + 40:]

		start_index = station_str.find('median') + 29
		end_index = station_str.find('%&lt;/')
		median = station_str[start_index:end_index]
		if len(percentile) > 30:
			if i == station:
				print "Normal (median): NONE"
			text_file.write("Normal (median): NONE\n")
		else:
			if i == station:
				print "Normal (median): " + median + "%"
			text_file.write("Normal (median): %s %% \n" % median)

		station_str = station_str[start_index + 40:]

		start_index = station_str.find('mean') + 27
		end_index = station_str.find('%&lt;/')
		mean = station_str[start_index:end_index]
		if len(percentile) > 30:
			if i == station:
				print "Normal (mean): NONE"
			text_file.write("Normal (mean): NONE\n")
		else:
			if i == station:
				print "Normal (mean): " + mean + "%"
			text_file.write("Normal (mean): %s %% \n" % mean)

		text_file.write("------------------------------------------\n")

state_abbrev = choose_state()
URL = "http://waterwatch.usgs.gov/?m=real&r=" + state_abbrev
entries, station = get_stations(URL)
list_station_attributes(entries, station)
