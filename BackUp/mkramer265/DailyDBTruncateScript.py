import sqlite3
#This script simply wipes our DB clean of all wave data
	#Each day's data will be updated daily ...with no previously scraped data lingering.
#Once the database as been cleared, a subsequently scheduled script will replace it with the day's new data


def DailyTruncate():

	conn = sqlite3.connect('SurfSend.db')
	cursor = conn.cursor()

	cursor.execute('DELETE FROM IDGrab;')
	cursor.execute('DROP TABLE SurfMaster2;')
	cursor.execute('DELETE FROM SurfReport;')
	cursor.execute('DELETE FROM WindDirection;')
	cursor.execute('DELETE FROM WindInfo;')

	conn.commit()
	cursor.close()
	conn.close()

DailyTruncate()