import bs4
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen as uReq
import time
import datetime
from datetime import datetime as datetime2
import pandas as pd
from collections import defaultdict
import sqlite3
import lxml
from twilio.rest import Client


account_sid = "AC07b84eb974bf10833f1f9e430585aa82"
auth_token  = "a4f6b1978fdea11ab88e6395fc17799e"
client = Client(account_sid, auth_token)


# This function retrieves the wave height
def wave_height_finder():
	#list of URLs to scrape from
	my_url = ['https://www.ndbc.noaa.gov/station_page.php?station=44013']

	for url in my_url:
	#initiating python's ability to parse URL
		uClient = uReq(url)
	# this will offload our content in'to a variable
		page_html = uClient.read()
	# closes our client
		uClient.close()
		page_soup = BeautifulSoup(page_html, "html.parser")	
	# Fetching/Defining data to variables
		wave_height = page_soup.find('td', string='Wave Height (WVHT):').find_next_sibling().get_text().strip()
		wave_interval = page_soup.find('td', string='Dominant Wave Period (DPD):').find_next_sibling().get_text().strip()
		wind_direction = page_soup.find('td', string='Wind Direction (WDIR):').find_next_sibling().get_text().strip()
		wind_speed = page_soup.find('td', string='Wind Speed (WSPD):').find_next_sibling().get_text().strip()
		air_temp = page_soup.find('td', string='Air Temperature (ATMP):').find_next_sibling().get_text().strip()
		water_temp = page_soup.find('td', string='Water Temperature (WTMP):').find_next_sibling().get_text().strip()

		#Wind Direction Splicing
		wind_direction_abbreviated = wind_direction[:4]

		#Wind Speed Splicing
		wind_speed_abbreviated = wind_speed.split('.')
		# print(wind_speed_abbreviated)
		wind_speed_sliced = wind_speed_abbreviated[0]
		wind_speed_abbreviated_int = int(wind_speed_sliced)


		current_date = datetime2.today().strftime("%m/%d/%Y")
		msg_header = "------ New England Surf Summary " + current_date + "------" + "\n"

		surf_info_msg = "Current Wave Height:" + " " + wave_height + "\n" + "Current Wave Interval:" + " " + wave_interval + "\n" + "Current Wind Direction:" + " " + wind_direction + "\n" + "Current Wind Speed:" + " " + wind_speed + "\n" + "Current Air Temp:" + " " + air_temp + "\n" + "Current Water Temp:" + " " + water_temp + "\n" 


		# Logic begins for determining if surf conditions are good or not
		# Creating lists of WaveHeights, Wave Intervals, Wind Directions to check against in our logic 
		# for determining good surf conditions
		wave_height_list = ['0.1 ft','0.2 ft','0.3 ft','0.4 ft','0.5 ft','0.6 ft','0.7 ft','0.8 ft','0.9 ft',
								'1.1 ft', '1.2 ft', '1.3 ft', '1.4 ft', '1.5 ft', '1.6 ft', '1.7 ft', '1.8 ft','1.9 ft',
								'2.0 ft','2.3 ft','2.4 ft','2.5 ft','2.6 ft','2.7 ft','2.8 ft','2.9 ft']

		wave_interval_list = ['1 sec', '2 sec', '3 sec', '4 sec', '5 sec', '6 sec', '7 sec']


		wind_direction_list = ["SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]


		wind_speed_abbreviated = wind_speed.split('.')
		wind_speed_sliced = wind_speed_abbreviated[0]


###################################### Tide Info ######################################
	# Using Pandas to parse through the html table found in the URL containing Tide Data
	# current_date = datetime2.today().strftime('%Y-%m-%d')
	# print('')
	# print("------ Boston Tide Info ", current_date, "------")
	# print('')

	tide_urls = [
	#Boston [0]
	'https://www.tide-forecast.com/locations/Castle-Island-Boston-Harbor-Massachusetts/tides/latest',
	#North Carolina [1]
	'https://www.tide-forecast.com/locations/Morehead-City-North-Carolina/tides/latest',
	#Maine [2]
	'https://www.tide-forecast.com/locations/Portland-Maine/tides/latest',
	#Rhode Island [3]
	'https://www.tide-forecast.com/locations/Newport-Rhode-Island/tides/latest']

	#Initial Master Lists of Tide + Time Info from All URLs
	time_list_initial = []
	tide_list_initial = []

	#Boston Specific Lists
	boston_time_list = []
	boston_tide_list = []



  #	LISTS within a LIST
  # 1 & 2: Boston Tide List + Boston Time List
	boston_master_tides_list = []
	boston_master_tides_list.append(boston_tide_list)
	boston_master_tides_list.append(boston_time_list)


	#MASTER LIST
		#Currently Contains 2 lists (Boston [0] + NC[1])
			# Boston List[0] is comprised of 2 lists: Boston Tide List[0] + Boston Time List [1]
	master_all_list = []
	master_all_list.append(boston_master_tides_list)

	# Iterating for our Initial Lists Containing All URL data
	for url in tide_urls:


		tide_table = pd.read_html(url)[0]


		tide_ = tide_table['Tide'].values.tolist()

		# 11/9/2019 -- Changed to Time (EST)& Date
			# Previously Time (EDT)& Date
		# Tide Website changes value of this table's column from time to time
		# Observed at least twice now.
		time_date = tide_table['Time (EDT)& Date'].values.tolist()

		time_list_initial.append(time_date)
		tide_list_initial.append(tide_)

	#Boston: Iterating through our initial lists
	for (t, i) in zip(tide_list_initial[0], time_list_initial[0]):
		time_date_sliced = i.split('(')
		time_ = time_date_sliced[0]
		date_ = time_date_sliced[1]

		#change the variable name so it makes it clear what we're printing :)
		tide_ = t

		boston_time_list.append(time_)
		boston_tide_list.append(tide_)

	for x in master_all_list:
		tide_times_list = []
		tide_values_list = []

		for tide_times,values in zip(x[0], x[1]):

			tide_time = tide_times.replace("e", "e:")

			tide_times_list.append(tide_time)
			tide_values_list.append(values)

		if len(tide_times_list) == 4:
			tide_info_msg = "----- New England Tide Info -----" + "\n" + tide_times_list[0] + " " + tide_values_list[0] + "\n" + tide_times_list[1] + " " + tide_values_list[1] + "\n" +  tide_times_list[2] + " " + tide_values_list[2] + "\n" +  tide_times_list[3] + " " + tide_values_list[3]
		else:
			tide_info_msg = "----- New England Tide Info -----" + "\n" + tide_times_list[0] + " " + tide_values_list[0] + "\n" + tide_times_list[1] + " " + tide_values_list[1] + "\n" +  tide_times_list[2] + " " + tide_values_list[2]
		print("\n")


	# Here is the logic used to determine if current conditions are generating good waves
	if wave_height not in wave_height_list and wave_interval not in wave_interval_list and wind_direction in wind_direction_list and wind_speed_abbreviated_int < 17:
		print("\n")
		message = client.messages \
			.create(
				 body=wave_height,
				 from_="+12058758672",
				 to='+17812648275'
			 )
		print("----- Summary -----")
		print("Good Waves Right Now in New England! Go out ;& Surf!")
		print("\n")
		print("SMS For Good Conditions Message Sent!")
		print("\n")
		print("End.")
		print("\n")
	else:
		print("\n")
		sms_msg = msg_header + surf_info_msg + tide_info_msg
		print(sms_msg)
		message = client.messages \
			.create(
				 body=sms_msg,
				 from_="+12058758672",
				 to='+17812648275'
			 )
		print("----- Summary -----")
		print("Unfortunately, surf conditions in New England are not good right now.")
		print("\n")
		print("SMS For Bad Conditions Message Sent!")
		print("\n")
		print("End.")
		print("\n")

wave_height_finder()		

