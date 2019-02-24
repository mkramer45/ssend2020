from lxml import html
import requests
import sqlite3
import bs4
from bs4 import BeautifulSoup
import sqlite3
#from urllib.request import urlopen as uReq
from urllib2 import urlopen as uReq
import re
import sys



def my_function():
	my_url = ['https://magicseaweed.com/Narragansett-Beach-Surf-Report/1103/',
	'https://magicseaweed.com/2nd-Beach-Sachuest-Beach-Surf-Report/846/',
	'https://magicseaweed.com/Nahant-Surf-Report/1091/',
	'https://magicseaweed.com/Nantasket-Beach-Surf-Report/371/',
	'https://magicseaweed.com/Scituate-Surf-Report/372/',
	'https://magicseaweed.com/Cape-Cod-Surf-Report/373/',
	'https://magicseaweed.com/The-Wall-Surf-Report/369/',
	'https://magicseaweed.com/Green-Harbor-Surf-Report/864/',
	'https://magicseaweed.com/Cape-Ann-Surf-Report/370/',
	'https://magicseaweed.com/27th-Ave-North-Myrtle-Surf-Report/2152/',
	'https://magicseaweed.com/Cocoa-Beach-Surf-Report/350/',
	'https://magicseaweed.com/Devereux-Surf-Report/4792/',
	'https://magicseaweed.com/Salisbury-Surf-Report/1130/',
	'https://magicseaweed.com/Seabrook-Beach-Surf-Report/2078/',
	'https://magicseaweed.com/Rye-Rocks-Surf-Report/368/',
	'https://magicseaweed.com/Hampton-Beach-Surf-Report/2074/',
	'https://magicseaweed.com/Plymouth-Beach-Surf-Report/4525/',
	'https://magicseaweed.com/Baileys-Beach-Surf-Report/2096/',
	'https://magicseaweed.com/Ruggles-Surf-Report/374/'
	]

	for url in my_url:

		page = requests.get(url)
		tree = html.fromstring(page.content)


		#This will create master list containing SwellSize, SwellInterval, & Airtemp
		intervals = tree.xpath('//*[@class="nomargin font-sans-serif heavy"]/text()')
		#Navigating through master list, breaking down 3 data categories into variables
		swellsizeft = intervals[0::5]
		swellintervalsec = intervals[2::5]
		airtempdegrees = intervals[4::5]

		# Next we will need to iterate through our per category lists, and add to DB!

		# ['A', 'B', 'C', 'D']
		# ['Swell Size', 'Junk', 'SwellInterval', 'Junk', 'Airtemp']
		# ['  2', '  ', '  11', '  ', '38', ]

		conn = sqlite3.connect('SurfSend.db')
		cursor = conn.cursor()
		cursor.execute('CREATE TABLE IF NOT EXISTS SurfReport(ID INTEGER PRIMARY KEY, SwellSizeFt INT, SwellIntervalSec INT, AirTemp INT )')

		for x, y, z in zip(swellsizeft, swellintervalsec, airtempdegrees):
				conn = sqlite3.connect('SurfSend.db')
				cursor = conn.cursor()
				# cursor.execute("INSERT INTO SurfReport VALUES (?,?,?)", (x,y,z))
				cursor.execute("INSERT INTO SurfReport (SwellSizeFt, SwellIntervalSec, AirTemp) VALUES (?,?,?)", (x,y,z,))
				conn.commit()
				cursor.close()
				conn.close()


def my_function2():
	#list of URLs to scrape from
	my_url = ['https://magicseaweed.com/Narragansett-Beach-Surf-Report/1103/',
	'https://magicseaweed.com/2nd-Beach-Sachuest-Beach-Surf-Report/846/',
	'https://magicseaweed.com/Nahant-Surf-Report/1091/',
	'https://magicseaweed.com/Nantasket-Beach-Surf-Report/371/',
	'https://magicseaweed.com/Scituate-Surf-Report/372/',
	'https://magicseaweed.com/Cape-Cod-Surf-Report/373/',
	'https://magicseaweed.com/The-Wall-Surf-Report/369/',
	'https://magicseaweed.com/Green-Harbor-Surf-Report/864/',
	'https://magicseaweed.com/Cape-Ann-Surf-Report/370/',
	'https://magicseaweed.com/27th-Ave-North-Myrtle-Surf-Report/2152/',
	'https://magicseaweed.com/Cocoa-Beach-Surf-Report/350/',
	'https://magicseaweed.com/Devereux-Surf-Report/4792/',
	'https://magicseaweed.com/Salisbury-Surf-Report/1130/',
	'https://magicseaweed.com/Seabrook-Beach-Surf-Report/2078/',
	'https://magicseaweed.com/Rye-Rocks-Surf-Report/368/',
	'https://magicseaweed.com/Hampton-Beach-Surf-Report/2074/',
	'https://magicseaweed.com/Plymouth-Beach-Surf-Report/4525/',
	'https://magicseaweed.com/Baileys-Beach-Surf-Report/2096/',
	'https://magicseaweed.com/Ruggles-Surf-Report/374/']
	# opening up connecting, grabbing the page

	conn = sqlite3.connect('SurfSend.db')
	cursor = conn.cursor()
	cursor.execute('CREATE TABLE IF NOT EXISTS WindInfo(ID INTEGER PRIMARY KEY, WindMPH INT)')

	#iterate over list of URLS
	for url in my_url:
		#initiating python's ability to parse URL
		uClient = uReq(url)
	# this will offload our content in'to a variable
		page_html = uClient.read()
	# closes our client
		uClient.close()

	# html parsing
		#beautifulsoup magic
		page_soup = BeautifulSoup(page_html, "html.parser")
		#variable for soon to be parsed page
		wind = page_soup.findAll('td', class_=re.compile("text-center table-forecast-wind td-nowrap"))
		#prints the list of URLs we scraped from

	# iterates over parsed HTML
		for w in wind:
			#wavesize
			wi = w.find('span', class_='stacked-text text-right')
			winb = wi.text.strip()

			conn = sqlite3.connect('SurfSend.db')
			cursor = conn.cursor()
			# cursor.execute("INSERT INTO WindInfo VALUES (?)", (winb,))
			cursor.execute("INSERT INTO WindInfo (WindMPH) VALUES (?)", (winb,))
			conn.commit()
			cursor.close()
			conn.close()

def my_function3():
	my_url = ['https://magicseaweed.com/Narragansett-Beach-Surf-Report/1103/',
	'https://magicseaweed.com/2nd-Beach-Sachuest-Beach-Surf-Report/846/',
	'https://magicseaweed.com/Nahant-Surf-Report/1091/',
	'https://magicseaweed.com/Nantasket-Beach-Surf-Report/371/',
	'https://magicseaweed.com/Scituate-Surf-Report/372/',
	'https://magicseaweed.com/Cape-Cod-Surf-Report/373/',
	'https://magicseaweed.com/The-Wall-Surf-Report/369/',
	'https://magicseaweed.com/Green-Harbor-Surf-Report/864/',
	'https://magicseaweed.com/Cape-Ann-Surf-Report/370/',
	'https://magicseaweed.com/27th-Ave-North-Myrtle-Surf-Report/2152/',
	'https://magicseaweed.com/Cocoa-Beach-Surf-Report/350/',
	'https://magicseaweed.com/Devereux-Surf-Report/4792/',
	'https://magicseaweed.com/Salisbury-Surf-Report/1130/',
	'https://magicseaweed.com/Seabrook-Beach-Surf-Report/2078/',
	'https://magicseaweed.com/Rye-Rocks-Surf-Report/368/',
	'https://magicseaweed.com/Hampton-Beach-Surf-Report/2074/',
	'https://magicseaweed.com/Plymouth-Beach-Surf-Report/4525/',
	'https://magicseaweed.com/Baileys-Beach-Surf-Report/2096/',
	'https://magicseaweed.com/Ruggles-Surf-Report/374/']

	for url in my_url:

		r = requests.get(url)

		html = r.text

		soup = BeautifulSoup(html, 'lxml')

		# wind_directions = soup.find_all('td', {"class":"text-center last msw-js-tooltip td-square background-success"})

		wind_dir = soup.find_all(class_=re.compile('^text-center last msw-js-tooltip td-square background-'))

		conn = sqlite3.connect('SurfSend.db')
		cursor = conn.cursor()
		cursor.execute('CREATE TABLE IF NOT EXISTS WindDirection(ID INTEGER PRIMARY KEY, WindDescription TEXT)')

		for w in wind_dir:

			windd = w['title']
			print(w['title'])


			conn = sqlite3.connect('SurfSend.db')
			cursor = conn.cursor()
			# cursor.execute("INSERT INTO WindInfo VALUES (?)", (winb,))
			cursor.execute("INSERT INTO WindDirection (WindDescription) VALUES (?)", (windd,))
			conn.commit()
			cursor.close()
			conn.close()


def my_function4():

	url = 'https://magicseaweed.com/Narragansett-Beach-Surf-Report/1103/'

	conn = sqlite3.connect('SurfSend.db')
	cursor = conn.cursor()
	cursor.execute('CREATE TABLE IF NOT EXISTS IDGrab(ID INTEGER PRIMARY KEY, WindDescription TEXT)')

	r = requests.get(url)

	html = r.text

	soup = BeautifulSoup(html, 'lxml')

	# wind_directions = soup.find_all('td', {"class":"text-center last msw-js-tooltip td-square background-success"})

	wind_dir = soup.find_all(class_=re.compile('^text-center last msw-js-tooltip td-square background-'))

	for w in wind_dir:

		windd = w['title']
		print(w['title'])


		conn = sqlite3.connect('SurfSend.db')
		cursor = conn.cursor()
		# cursor.execute("INSERT INTO WindInfo VALUES (?)", (winb,))
		cursor.execute("INSERT INTO IDGrab (WindDescription) VALUES (?)", (windd,))
		conn.commit()
		cursor.close()
		conn.close()


def my_function5():

	conn = sqlite3.connect('SurfSend.db')
	cursor = conn.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS SurfMaster2 AS select SurfReport.ID, SurfReport.SwellSizeFt, SurfReport.SwellIntervalSec, WindInfo.WindMPH, WindDirection.WindDescription, SurfReport.AirTemp from SurfReport inner join WindInfo on SurfReport.ID = WindInfo.ID inner join WindDirection on WindInfo.ID = WindDirection.ID")
	cursor.execute("ALTER TABLE SurfMaster2 ADD beach_name TEXT")
	# 1.1 --Beach Naming Begin--
	cursor.execute("UPDATE SurfMaster2 SET beach_name = 'Narragansett' WHERE ID BETWEEN 1 AND 56")
	cursor.execute("UPDATE SurfMaster2 SET beach_name = '2nd Beach' WHERE ID BETWEEN 57 AND 112;")
	cursor.execute("UPDATE SurfMaster2 SET beach_name = 'Nahant' WHERE ID BETWEEN 113 AND 168")
	cursor.execute("UPDATE SurfMaster2 SET beach_name = 'Nantasket' WHERE ID BETWEEN 169 AND 224")
	cursor.execute("UPDATE SurfMaster2 SET beach_name = 'Scituate' WHERE ID BETWEEN 225 AND 280")
	cursor.execute("UPDATE SurfMaster2 SET beach_name = 'Cape Cod' WHERE ID BETWEEN 281 AND 336")
	cursor.execute("UPDATE SurfMaster2 SET beach_name = 'NH Seacoast' WHERE ID BETWEEN 337 AND 392")
	cursor.execute("UPDATE SurfMaster2 SET beach_name = 'Green Harbor' WHERE ID BETWEEN 393 AND 448")
	cursor.execute("UPDATE SurfMaster2 SET beach_name = 'Cape Ann' WHERE ID BETWEEN 449 AND 504")
	cursor.execute("UPDATE SurfMaster2 SET beach_name = 'Myrtle Beach' WHERE ID BETWEEN 505 AND 560")
	cursor.execute("UPDATE SurfMaster2 SET beach_name = 'Cocoa Beach' WHERE ID BETWEEN 561 AND 616")
	cursor.execute("UPDATE SurfMaster2 SET beach_name = 'Devereux Beach' WHERE ID BETWEEN 617 AND 672")
	cursor.execute("UPDATE SurfMaster2 SET beach_name = 'Salisbury' WHERE ID BETWEEN 673 AND 728")
	cursor.execute("UPDATE SurfMaster2 SET beach_name = 'Seabrook' WHERE ID BETWEEN 729 AND 784")
	cursor.execute("UPDATE SurfMaster2 SET beach_name = 'Rye' WHERE ID BETWEEN 785 AND 840")
	cursor.execute("UPDATE SurfMaster2 SET beach_name = 'Hampton' WHERE ID BETWEEN 841 AND 896")
	cursor.execute("UPDATE SurfMaster2 SET beach_name = 'Plymouth' WHERE ID BETWEEN 897 AND 952")
	cursor.execute("UPDATE SurfMaster2 SET beach_name = 'Baileys Beach' WHERE ID BETWEEN 953 AND 1008")
	cursor.execute("UPDATE SurfMaster2 SET beach_name = 'Ruggles' WHERE ID BETWEEN 1009 AND 1064")
	# 1.1 --Beach Naming End--

	# 1.2 --TimeID Begin--
	cursor.execute("ALTER TABLE SurfMaster2 ADD Time_ID TEXT")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =1 where id in (1,57,113,169,225,281,337,393,449,505,561,617,673,729,785,841,897,953,1009);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =2 where id in (2,58,114,170,226,282,338,394,450,506,562,618,674,730,786,842,898,954,1010);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =3 where id in (3,59,115,171,227,283,339,395,451,507,563,619,675,731,787,843,899,955,1011);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =4 where id in (4,60,116,172,228,284,340,396,452,508,564,620,676,732,788,844,900,956,1012);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =5 where id in (5,61,117,173,229,285,341,397,453,509,565,621,677,733,789,845,901,957,1013);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =6 where id in (6,62,118,174,230,286,342,398,454,510,566,622,678,734,790,846,902,958,1014);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =7 where id in (7,63,119,175,231,287,343,399,455,511,567,623,679,735,791,847,903,959,1015);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =8 where id in (8,64,120,176,232,288,344,400,456,512,568,624,680,736,792,848,904,960,1016);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =9 where id in (9,65,121,177,233,289,345,401,457,513,569,625,681,737,793,849,905,961,1017);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =10 where id in (10,66,122,178,234,290,346,402,458,514,570,626,682,738,794,850,906,962,1018);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =11 where id in (11,67,123,179,235,291,347,403,459,515,571,627,683,739,795,851,907,963,1019);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =12 where id in (12,68,124,180,236,292,348,404,460,516,572,628,684,740,796,852,908,964,1020);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =13 where id in (13,69,125,181,237,293,349,405,461,517,573,629,685,741,797,853,909,965,1021);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =14 where id in (14,70,126,182,238,294,350,406,462,518,574,630,686,742,798,854,910,966,1022);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =15 where id in (15,71,127,183,239,295,351,407,463,519,575,631,687,743,799,855,911,967,1023);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =16 where id in (16,72,128,184,240,296,352,408,464,520,576,632,688,744,800,856,912,968,1024);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =17 where id in (17,73,129,185,241,297,353,409,465,521,577,633,689,745,801,857,913,969,1025);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =18 where id in (18,74,130,186,242,298,354,410,466,522,578,634,690,746,802,858,914,970,1026);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =19 where id in (19,75,131,187,243,299,355,411,467,523,579,635,691,747,803,859,915,971,1027);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =20 where id in (20,76,132,188,244,300,356,412,468,524,580,636,692,748,804,860,916,972,1028);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =21 where id in (21,77,133,189,245,301,357,413,469,525,581,637,693,749,805,861,917,973,1029);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =22 where id in (22,78,134,190,246,302,358,414,470,526,582,638,694,750,806,862,918,974,1030);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =23 where id in (23,79,135,191,247,303,359,415,471,527,583,639,695,751,807,863,919,975,1031);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =24 where id in (24,80,136,192,248,304,360,416,472,528,584,640,696,752,808,864,920,976,1032);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =25 where id in (25,81,137,193,249,305,361,417,473,529,585,641,697,753,809,865,921,977,1033);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =26 where id in (26,82,138,194,250,306,362,418,474,530,586,642,698,754,810,866,922,978,1034);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =27 where id in (27,83,139,195,251,307,363,419,475,531,587,643,699,755,811,867,923,979,1035);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =28 where id in (28,84,140,196,252,308,364,420,476,532,588,644,700,756,812,868,924,980,1036);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =29 where id in (29,85,141,197,253,309,365,421,477,533,589,645,701,757,813,869,925,981,1037);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =30 where id in (30,86,142,198,254,310,366,422,478,534,590,646,702,758,814,870,926,982,1038);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =31 where id in (31,87,143,199,255,311,367,423,479,535,591,647,703,759,815,871,927,983,1039);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =32 where id in (32,88,144,200,256,312,368,424,480,536,592,648,704,760,816,872,928,984,1040);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =33 where id in (33,89,145,201,257,313,369,425,481,537,593,649,705,761,817,873,929,985,1041);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =34 where id in (34,90,146,202,258,314,370,426,482,538,594,650,706,762,818,874,930,986,1042);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =35 where id in (35,91,147,203,259,315,371,427,483,539,595,651,707,763,819,875,931,987,1043);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =36 where id in (36,92,148,204,260,316,372,428,484,540,596,652,708,764,820,876,932,988,1044);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =37 where id in (37,93,149,205,261,317,373,429,485,541,597,653,709,765,821,877,933,989,1045);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =38 where id in (38,94,150,206,262,318,374,430,486,542,598,654,710,766,822,878,934,990,1046);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =39 where id in (39,95,151,207,263,319,375,431,487,543,599,655,711,767,823,879,935,991,1047);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =40 where id in (40,96,152,208,264,320,376,432,488,544,600,656,712,768,824,880,936,992,1048);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =41 where id in (41,97,153,209,265,321,377,433,489,545,601,657,713,769,825,881,937,993,1049);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =42 where id in (42,98,154,210,266,322,378,434,490,546,602,658,714,770,826,882,938,994,1050);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =43 where id in (43,99,155,211,267,323,379,435,491,547,603,659,715,771,827,883,939,995,1051);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =44 where id in (44,100,156,212,268,324,380,436,492,548,604,660,716,772,828,884,940,996,1052);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =45 where id in (45,101,157,213,269,325,381,437,493,549,605,661,717,773,829,885,941,997,1053);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =46 where id in (46,102,158,214,270,326,382,438,494,550,606,662,718,774,830,886,942,998,1054);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =47 where id in (47,103,159,215,271,327,383,439,495,551,607,663,719,775,831,887,943,999,1055);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =48 where id in (48,104,160,216,272,328,384,440,496,552,608,664,720,776,832,888,944,1000,1056);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =49 where id in (49,105,161,217,273,329,385,441,497,553,609,665,721,777,833,889,945,1001,1057);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =50 where id in (50,106,162,218,274,330,386,442,498,554,610,666,722,778,834,890,946,1002,1058);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =51 where id in (51,107,163,219,275,331,387,443,499,555,611,667,723,779,835,891,947,1003,1059);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =52 where id in (52,108,164,220,276,332,388,444,500,556,612,668,724,780,836,892,948,1004,1060);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =53 where id in (53,109,165,221,277,333,389,445,501,557,613,669,725,781,837,893,949,1005,1061);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =54 where id in (54,110,166,222,278,334,390,446,502,558,614,670,726,782,838,894,950,1006,1062);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =55 where id in (55,111,167,223,279,335,391,447,503,559,615,671,727,783,839,895,951,1007,1063);")
	cursor.execute("UPDATE SurfMaster2 set Time_ID =56 where id in (56,112,168,224,280,336,392,448,504,560,616,672,728,784,840,896,952,1008,1064);")
	# 1.2 --TimeID End--

	# Date Add
	cursor.execute("ALTER TABLE SurfMaster2 ADD date_ TEXT")
	cursor.execute("UPDATE SurfMaster2 SET date_ = date('now') WHERE Time_ID in (1,2,3,4,5,6,7,8)")
	cursor.execute("UPDATE SurfMaster2 SET date_ = date('now','+1 day') WHERE Time_ID in (9,10,11,12,13,14,15,16)")
	cursor.execute("UPDATE SurfMaster2 SET date_ = date('now','+2 day') WHERE Time_ID in (17,18,19,20,21,22,23,24)")
	cursor.execute("UPDATE SurfMaster2 SET date_ = date('now','+3 day') WHERE Time_ID in (25,26,27,28,29,30,31,32)")
	cursor.execute("UPDATE SurfMaster2 SET date_ = date('now','+4 day') WHERE Time_ID in (33,34,35,36,37,38,39,40)")
	cursor.execute("UPDATE SurfMaster2 SET date_ = date('now','+5 day') WHERE Time_ID in (41,42,43,44,45,46,47,48)")
	cursor.execute("UPDATE SurfMaster2 SET date_ = date('now','+6 day') WHERE Time_ID in (49,50,51,52,53,54,55,56)")
	cursor.execute("ALTER TABLE SurfMaster2 ADD time_ TEXT")
	cursor.execute("UPDATE SurfMaster2 SET time_ = '12am' WHERE Time_ID in (1,9,17,25,33,41,49)")
	cursor.execute("UPDATE SurfMaster2 SET time_ = '3am' WHERE Time_ID in (2,10,18,26,34,42,50)")
	cursor.execute("UPDATE SurfMaster2 SET time_ = '6am' WHERE Time_ID in (3,11,19,27,35,43,51)")
	cursor.execute("UPDATE SurfMaster2 SET time_ = '9am' WHERE Time_ID in (4,12,20,28,36,44,52)")
	cursor.execute("UPDATE SurfMaster2 SET time_ = '12pm' WHERE Time_ID in (5,13,21,29,37,45,53)")
	cursor.execute("UPDATE SurfMaster2 SET time_ = '3pm' WHERE Time_ID in (6,14,22,30,38,46,54)")
	cursor.execute("UPDATE SurfMaster2 SET time_ = '6pm' WHERE Time_ID in (7,15,23,31,39,47,55)")
	cursor.execute("UPDATE SurfMaster2 SET time_ = '9pm' WHERE Time_ID in (8,16,24,32,40,48,56)")

	# State Add
	cursor.execute("ALTER TABLE SurfMaster2 ADD state TEXT")
	cursor.execute("UPDATE SurfMaster2 SET state = 'Rhode Island' WHERE ID BETWEEN 1 AND 56")
	cursor.execute("UPDATE SurfMaster2 SET state = 'Rhode Island' WHERE ID BETWEEN 57 AND 112;")
	cursor.execute("UPDATE SurfMaster2 SET state = 'Massachusetts' WHERE ID BETWEEN 113 AND 168")
	cursor.execute("UPDATE SurfMaster2 SET state = 'Massachusetts' WHERE ID BETWEEN 169 AND 224")
	cursor.execute("UPDATE SurfMaster2 SET state = 'Massachusetts' WHERE ID BETWEEN 225 AND 280")
	cursor.execute("UPDATE SurfMaster2 SET state = 'Massachusetts' WHERE ID BETWEEN 281 AND 336")
	cursor.execute("UPDATE SurfMaster2 SET state = 'New Hampshire' WHERE ID BETWEEN 337 AND 392")
	cursor.execute("UPDATE SurfMaster2 SET state = 'Massachusetts' WHERE ID BETWEEN 393 AND 448")
	cursor.execute("UPDATE SurfMaster2 SET state = 'Massachusetts' WHERE ID BETWEEN 449 AND 504")
	cursor.execute("UPDATE SurfMaster2 SET state = 'South Carolina' WHERE ID BETWEEN 505 AND 560")
	cursor.execute("UPDATE SurfMaster2 SET state = 'Florida' WHERE ID BETWEEN 561 AND 616")
	cursor.execute("UPDATE SurfMaster2 SET state = 'Massachusetts' WHERE ID BETWEEN 617 AND 672")
	cursor.execute("UPDATE SurfMaster2 SET state = 'Massachusetts' WHERE ID BETWEEN 673 AND 728")
	cursor.execute("UPDATE SurfMaster2 SET state = 'New Hampshire' WHERE ID BETWEEN 729 AND 784")
	cursor.execute("UPDATE SurfMaster2 SET state = 'New Hampshire' WHERE ID BETWEEN 785 AND 840")
	cursor.execute("UPDATE SurfMaster2 SET state = 'New Hampshire' WHERE ID BETWEEN 841 AND 896")
	cursor.execute("UPDATE SurfMaster2 SET state = 'Massachusetts' WHERE ID BETWEEN 897 AND 952")
	cursor.execute("UPDATE SurfMaster2 SET state = 'Rhode Island' WHERE ID BETWEEN 953 AND 1008")
	cursor.execute("UPDATE SurfMaster2 SET state = 'Rhode Island' WHERE ID BETWEEN 1009 AND 1064")

	#------------------------Per Day Swell Size AVGs for graphs--------------------------

	cursor.execute("ALTER TABLE SurfMaster2 ADD Avg_Day TEXT")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Narragansett' and date_ = date('now')) where beach_name = 'Narragansett' and date_ = date('now')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Narragansett' and date_ = date('now','+1 day')) where beach_name = 'Narragansett' and date_ = date('now','+1 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Narragansett' and date_ = date('now','+2 day')) where beach_name = 'Narragansett' and date_ = date('now','+2 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Narragansett' and date_ = date('now','+3 day')) where beach_name = 'Narragansett' and date_ = date('now','+3 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Narragansett' and date_ = date('now','+4 day')) where beach_name = 'Narragansett' and date_ = date('now','+4 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Narragansett' and date_ = date('now','+5 day')) where beach_name = 'Narragansett' and date_ = date('now','+5 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Narragansett' and date_ = date('now','+6 day')) where beach_name = 'Narragansett' and date_ = date('now','+6 day')")

	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = '2nd Beach' and date_ = date('now')) where beach_name = '2nd Beach' and date_ = date('now')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = '2nd Beach' and date_ = date('now','+1 day')) where beach_name = '2nd Beach' and date_ = date('now','+1 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = '2nd Beach' and date_ = date('now','+2 day')) where beach_name = '2nd Beach' and date_ = date('now','+2 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = '2nd Beach' and date_ = date('now','+3 day')) where beach_name = '2nd Beach' and date_ = date('now','+3 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = '2nd Beach' and date_ = date('now','+4 day')) where beach_name = '2nd Beach' and date_ = date('now','+4 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = '2nd Beach' and date_ = date('now','+5 day')) where beach_name = '2nd Beach' and date_ = date('now','+5 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = '2nd Beach' and date_ = date('now','+6 day')) where beach_name = '2nd Beach' and date_ = date('now','+6 day')")

	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Ruggles' and date_ = date('now')) where beach_name = 'Ruggles' and date_ = date('now')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Ruggles' and date_ = date('now','+1 day')) where beach_name = 'Ruggles' and date_ = date('now','+1 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Ruggles' and date_ = date('now','+2 day')) where beach_name = 'Ruggles' and date_ = date('now','+2 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Ruggles' and date_ = date('now','+3 day')) where beach_name = 'Ruggles' and date_ = date('now','+3 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Ruggles' and date_ = date('now','+4 day')) where beach_name = 'Ruggles' and date_ = date('now','+4 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Ruggles' and date_ = date('now','+5 day')) where beach_name = 'Ruggles' and date_ = date('now','+5 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Ruggles' and date_ = date('now','+6 day')) where beach_name = 'Ruggles' and date_ = date('now','+6 day')")

	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Nahant' and date_ = date('now')) where beach_name = 'Nahant' and date_ = date('now')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Nahant' and date_ = date('now','+1 day')) where beach_name = 'Nahant' and date_ = date('now','+1 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Nahant' and date_ = date('now','+2 day')) where beach_name = 'Nahant' and date_ = date('now','+2 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Nahant' and date_ = date('now','+3 day')) where beach_name = 'Nahant' and date_ = date('now','+3 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Nahant' and date_ = date('now','+4 day')) where beach_name = 'Nahant' and date_ = date('now','+4 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Nahant' and date_ = date('now','+5 day')) where beach_name = 'Nahant' and date_ = date('now','+5 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Nahant' and date_ = date('now','+6 day')) where beach_name = 'Nahant' and date_ = date('now','+6 day')")

	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Nantasket' and date_ = date('now')) where beach_name = 'Nantasket' and date_ = date('now')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Nantasket' and date_ = date('now','+1 day')) where beach_name = 'Nantasket' and date_ = date('now','+1 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Nantasket' and date_ = date('now','+2 day')) where beach_name = 'Nantasket' and date_ = date('now','+2 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Nantasket' and date_ = date('now','+3 day')) where beach_name = 'Nantasket' and date_ = date('now','+3 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Nantasket' and date_ = date('now','+4 day')) where beach_name = 'Nantasket' and date_ = date('now','+4 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Nantasket' and date_ = date('now','+5 day')) where beach_name = 'Nantasket' and date_ = date('now','+5 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Nantasket' and date_ = date('now','+6 day')) where beach_name = 'Nantasket' and date_ = date('now','+6 day')")

	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Scituate' and date_ = date('now')) where beach_name = 'Scituate' and date_ = date('now')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Scituate' and date_ = date('now','+1 day')) where beach_name = 'Scituate' and date_ = date('now','+1 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Scituate' and date_ = date('now','+2 day')) where beach_name = 'Scituate' and date_ = date('now','+2 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Scituate' and date_ = date('now','+3 day')) where beach_name = 'Scituate' and date_ = date('now','+3 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Scituate' and date_ = date('now','+4 day')) where beach_name = 'Scituate' and date_ = date('now','+4 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Scituate' and date_ = date('now','+5 day')) where beach_name = 'Scituate' and date_ = date('now','+5 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Scituate' and date_ = date('now','+6 day')) where beach_name = 'Scituate' and date_ = date('now','+6 day')")

	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Cape Cod' and date_ = date('now')) where beach_name = 'Cape Cod' and date_ = date('now')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Cape Cod' and date_ = date('now','+1 day')) where beach_name = 'Cape Cod' and date_ = date('now','+1 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Cape Cod' and date_ = date('now','+2 day')) where beach_name = 'Cape Cod' and date_ = date('now','+2 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Cape Cod' and date_ = date('now','+3 day')) where beach_name = 'Cape Cod' and date_ = date('now','+3 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Cape Cod' and date_ = date('now','+4 day')) where beach_name = 'Cape Cod' and date_ = date('now','+4 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Cape Cod' and date_ = date('now','+5 day')) where beach_name = 'Cape Cod' and date_ = date('now','+5 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Cape Cod' and date_ = date('now','+6 day')) where beach_name = 'Cape Cod' and date_ = date('now','+6 day')")

	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Green Harbor' and date_ = date('now')) where beach_name = 'Green Harbor' and date_ = date('now')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Green Harbor' and date_ = date('now','+1 day')) where beach_name = 'Green Harbor' and date_ = date('now','+1 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Green Harbor' and date_ = date('now','+2 day')) where beach_name = 'Green Harbor' and date_ = date('now','+2 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Green Harbor' and date_ = date('now','+3 day')) where beach_name = 'Green Harbor' and date_ = date('now','+3 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Green Harbor' and date_ = date('now','+4 day')) where beach_name = 'Green Harbor' and date_ = date('now','+4 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Green Harbor' and date_ = date('now','+5 day')) where beach_name = 'Green Harbor' and date_ = date('now','+5 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Green Harbor' and date_ = date('now','+6 day')) where beach_name = 'Green Harbor' and date_ = date('now','+6 day')")

	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Cape Ann' and date_ = date('now')) where beach_name = 'Cape Ann' and date_ = date('now')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Cape Ann' and date_ = date('now','+1 day')) where beach_name = 'Cape Ann' and date_ = date('now','+1 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Cape Ann' and date_ = date('now','+2 day')) where beach_name = 'Cape Ann' and date_ = date('now','+2 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Cape Ann' and date_ = date('now','+3 day')) where beach_name = 'Cape Ann' and date_ = date('now','+3 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Cape Ann' and date_ = date('now','+4 day')) where beach_name = 'Cape Ann' and date_ = date('now','+4 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Cape Ann' and date_ = date('now','+5 day')) where beach_name = 'Cape Ann' and date_ = date('now','+5 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Cape Ann' and date_ = date('now','+6 day')) where beach_name = 'Cape Ann' and date_ = date('now','+6 day')")

	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Devereux Beach' and date_ = date('now')) where beach_name = 'Devereux Beach' and date_ = date('now')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Devereux Beach' and date_ = date('now','+1 day')) where beach_name = 'Devereux Beach' and date_ = date('now','+1 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Devereux Beach' and date_ = date('now','+2 day')) where beach_name = 'Devereux Beach' and date_ = date('now','+2 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Devereux Beach' and date_ = date('now','+3 day')) where beach_name = 'Devereux Beach' and date_ = date('now','+3 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Devereux Beach' and date_ = date('now','+4 day')) where beach_name = 'Devereux Beach' and date_ = date('now','+4 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Devereux Beach' and date_ = date('now','+5 day')) where beach_name = 'Devereux Beach' and date_ = date('now','+5 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Devereux Beach' and date_ = date('now','+6 day')) where beach_name = 'Devereux Beach' and date_ = date('now','+6 day')")

	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Salisbury' and date_ = date('now')) where beach_name = 'Salisbury' and date_ = date('now')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Salisbury' and date_ = date('now','+1 day')) where beach_name = 'Salisbury' and date_ = date('now','+1 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Salisbury' and date_ = date('now','+2 day')) where beach_name = 'Salisbury' and date_ = date('now','+2 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Salisbury' and date_ = date('now','+3 day')) where beach_name = 'Salisbury' and date_ = date('now','+3 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Salisbury' and date_ = date('now','+4 day')) where beach_name = 'Salisbury' and date_ = date('now','+4 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Salisbury' and date_ = date('now','+5 day')) where beach_name = 'Salisbury' and date_ = date('now','+5 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Salisbury' and date_ = date('now','+6 day')) where beach_name = 'Salisbury' and date_ = date('now','+6 day')")


	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'NH Seacoast' and date_ = date('now')) where beach_name = 'NH Seacoast' and date_ = date('now')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'NH Seacoast' and date_ = date('now','+1 day')) where beach_name = 'NH Seacoast' and date_ = date('now','+1 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'NH Seacoast' and date_ = date('now','+2 day')) where beach_name = 'NH Seacoast' and date_ = date('now','+2 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'NH Seacoast' and date_ = date('now','+3 day')) where beach_name = 'NH Seacoast' and date_ = date('now','+3 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'NH Seacoast' and date_ = date('now','+4 day')) where beach_name = 'NH Seacoast' and date_ = date('now','+4 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'NH Seacoast' and date_ = date('now','+5 day')) where beach_name = 'NH Seacoast' and date_ = date('now','+5 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'NH Seacoast' and date_ = date('now','+6 day')) where beach_name = 'NH Seacoast' and date_ = date('now','+6 day')")

	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Seabrook' and date_ = date('now')) where beach_name = 'Seabrook' and date_ = date('now')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Seabrook' and date_ = date('now','+1 day')) where beach_name = 'Seabrook' and date_ = date('now','+1 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Seabrook' and date_ = date('now','+2 day')) where beach_name = 'Seabrook' and date_ = date('now','+2 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Seabrook' and date_ = date('now','+3 day')) where beach_name = 'Seabrook' and date_ = date('now','+3 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Seabrook' and date_ = date('now','+4 day')) where beach_name = 'Seabrook' and date_ = date('now','+4 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Seabrook' and date_ = date('now','+5 day')) where beach_name = 'Seabrook' and date_ = date('now','+5 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Seabrook' and date_ = date('now','+6 day')) where beach_name = 'Seabrook' and date_ = date('now','+6 day')")

	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Rye' and date_ = date('now')) where beach_name = 'Rye' and date_ = date('now')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Rye' and date_ = date('now','+1 day')) where beach_name = 'Rye' and date_ = date('now','+1 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Rye' and date_ = date('now','+2 day')) where beach_name = 'Rye' and date_ = date('now','+2 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Rye' and date_ = date('now','+3 day')) where beach_name = 'Rye' and date_ = date('now','+3 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Rye' and date_ = date('now','+4 day')) where beach_name = 'Rye' and date_ = date('now','+4 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Rye' and date_ = date('now','+5 day')) where beach_name = 'Rye' and date_ = date('now','+5 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Rye' and date_ = date('now','+6 day')) where beach_name = 'Rye' and date_ = date('now','+6 day')")

	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Hampton' and date_ = date('now')) where beach_name = 'Hampton' and date_ = date('now')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Hampton' and date_ = date('now','+1 day')) where beach_name = 'Hampton' and date_ = date('now','+1 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Hampton' and date_ = date('now','+2 day')) where beach_name = 'Hampton' and date_ = date('now','+2 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Hampton' and date_ = date('now','+3 day')) where beach_name = 'Hampton' and date_ = date('now','+3 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Hampton' and date_ = date('now','+4 day')) where beach_name = 'Hampton' and date_ = date('now','+4 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Hampton' and date_ = date('now','+5 day')) where beach_name = 'Hampton' and date_ = date('now','+5 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Hampton' and date_ = date('now','+6 day')) where beach_name = 'Hampton' and date_ = date('now','+6 day')")

	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Plymouth' and date_ = date('now')) where beach_name = 'Plymouth' and date_ = date('now')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Plymouth' and date_ = date('now','+1 day')) where beach_name = 'Plymouth' and date_ = date('now','+1 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Plymouth' and date_ = date('now','+2 day')) where beach_name = 'Plymouth' and date_ = date('now','+2 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Plymouth' and date_ = date('now','+3 day')) where beach_name = 'Plymouth' and date_ = date('now','+3 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Plymouth' and date_ = date('now','+4 day')) where beach_name = 'Plymouth' and date_ = date('now','+4 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Plymouth' and date_ = date('now','+5 day')) where beach_name = 'Plymouth' and date_ = date('now','+5 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Plymouth' and date_ = date('now','+6 day')) where beach_name = 'Plymouth' and date_ = date('now','+6 day')")

	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Baileys Beach' and date_ = date('now')) where beach_name = 'Baileys Beach' and date_ = date('now')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Baileys Beach' and date_ = date('now','+1 day')) where beach_name = 'Baileys Beach' and date_ = date('now','+1 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Baileys Beach' and date_ = date('now','+2 day')) where beach_name = 'Baileys Beach' and date_ = date('now','+2 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Baileys Beach' and date_ = date('now','+3 day')) where beach_name = 'Baileys Beach' and date_ = date('now','+3 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Baileys Beach' and date_ = date('now','+4 day')) where beach_name = 'Baileys Beach' and date_ = date('now','+4 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Baileys Beach' and date_ = date('now','+5 day')) where beach_name = 'Baileys Beach' and date_ = date('now','+5 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Baileys Beach' and date_ = date('now','+6 day')) where beach_name = 'Baileys Beach' and date_ = date('now','+6 day')")

	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Cocoa Beach' and date_ = date('now')) where beach_name = 'Cocoa Beach' and date_ = date('now')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Cocoa Beach' and date_ = date('now','+1 day')) where beach_name = 'Cocoa Beach' and date_ = date('now','+1 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Cocoa Beach' and date_ = date('now','+2 day')) where beach_name = 'Cocoa Beach' and date_ = date('now','+2 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Cocoa Beach' and date_ = date('now','+3 day')) where beach_name = 'Cocoa Beach' and date_ = date('now','+3 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Cocoa Beach' and date_ = date('now','+4 day')) where beach_name = 'Cocoa Beach' and date_ = date('now','+4 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Cocoa Beach' and date_ = date('now','+5 day')) where beach_name = 'Cocoa Beach' and date_ = date('now','+5 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Cocoa Beach' and date_ = date('now','+6 day')) where beach_name = 'Cocoa Beach' and date_ = date('now','+6 day')")

	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Myrtle Beach' and date_ = date('now')) where beach_name = 'Myrtle Beach' and date_ = date('now')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Myrtle Beach' and date_ = date('now','+1 day')) where beach_name = 'Myrtle Beach' and date_ = date('now','+1 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Myrtle Beach' and date_ = date('now','+2 day')) where beach_name = 'Myrtle Beach' and date_ = date('now','+2 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Myrtle Beach' and date_ = date('now','+3 day')) where beach_name = 'Myrtle Beach' and date_ = date('now','+3 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Myrtle Beach' and date_ = date('now','+4 day')) where beach_name = 'Myrtle Beach' and date_ = date('now','+4 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Myrtle Beach' and date_ = date('now','+5 day')) where beach_name = 'Myrtle Beach' and date_ = date('now','+5 day')")
	cursor.execute("UPDATE SurfMaster2 SET Avg_Day = (SELECT avg(SwellSizeFt) FROM SurfMaster2 WHERE beach_name = 'Myrtle Beach' and date_ = date('now','+6 day')) where beach_name = 'Myrtle Beach' and date_ = date('now','+6 day')")


	cursor.execute("CREATE TABLE IF NOT EXISTS user(ID INTEGER PRIMARY KEY, username TEXT, email TEXT, password TEXT)")
	cursor.execute("CREATE TABLE IF NOT EXISTS ArtistMonitor(ID INTEGER PRIMARY KEY, DJName TEXT, usn TEXT, email TEXT, cellphone TEXT, delivery TEXT)")
	cursor.execute("CREATE TABLE IF NOT EXISTS Tracks(Artist TEXT, Song TEXT, Label TEXT, Price TEXT, ChartPosition TEXT, Genre TEXT, Websource TEXT)")
	cursor.execute("CREATE TABLE IF NOT EXISTS Sendr_Usr(Email TEXT, FirstName TEXT, DeliveryType TEXT)")

	conn.commit()
	cursor.close()
	conn.close()

my_function()
my_function2()
my_function3()
my_function4()
my_function5()

	#Executing this script should give us 616 rows