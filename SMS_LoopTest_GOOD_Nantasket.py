import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import sqlite3
import sys
from twilio.rest import Client
#sys.setdefaultencoding('utf8')

# select random msg
account_sid = "AC9b35d0f731d55b40837d58c7029f1c9e"
auth_token  = "8ea852ad93611021ab3ac94f6dff6606"

while True:
	try:
		conn = sqlite3.connect('SurfSend.db')
		cursor = conn.cursor()
		# this returns records containing beach specific information we are to send for users who signed up for said beach
		# in this case, let's grab info for Nantasket emails we are going to send
		cur2 = cursor.execute("select * from surfmaster2 where surfmaster2.time_ not in ('3am','12am','9pm') limit 2;")
		info2 = cur2.fetchall()
		conn.commit()
		conn.close()
		conn.close()

		newlist = [row[0:19] for row in info2]

		row1 = newlist[0]
		row2 = newlist[1]
		# print(x)
		# print(x[2])

		#ROW 1 VALUES
		swellsize1 = row1[1]
		swellinterval1 = row1[2]
		windmph1 = row1[3]
		winddesc1 = row1[4]
		airtemp1 = row1[5]
		beachname1 = row1[6]
		date1 = row1[8]
		time1 = row1[9]
		state1 = row1[10]
		avg1 = row1[11]


		# print(swellsize1)
		# print(beachname1)
		# print(date1)
		# print(email1)

		#ROW 2 VALUES
		swellsize2 = row2[1]
		swellinterval2 = row2[2]
		windmph2 = row2[3]
		winddesc2 = row2[4]
		airtemp2 = row2[5]
		beachname2 = row2[6]
		date2 = row2[8]
		time2 = row2[9]
		state2 = row2[10]
		avg2 = row2[11]

		# print(swellsize2)
		# print(beachname2)
		# print(date2)
		# print(email2)

		# Message Example: Nantasket: 12ft at 9sec on 2018-10-29 ~ 9am
		message1 = '-----------' + beachname1 +'-----------' + '\n' + 'Date/Time: ' + date1 + ' ~ ' + str(time1) + '\n'  'WaveInfo: ' + str(swellsize1) + 'ft' + ' at ' + str(swellinterval1) + 'sec'  + '\n' + 'WindInfo: ' + str(windmph1) + ', ' + winddesc1 + '\n' + 'Predicted Wave Height Avg (day): ' + str(avg1) + '\n' + 'AirTemp: ' + str(airtemp1)
		message2 = '-----------' + beachname2 +'-----------' + '\n' + 'Date/Time: ' + date2 + ' ~ ' + str(time2) + '\n'  'WaveInfo: ' + str(swellsize2) + 'ft' + ' at ' + str(swellinterval2) + 'sec'  + '\n' + 'WindInfo: ' + str(windmph2) + ', ' + winddesc2 + '\n' + 'Predicted Wave Height Avg (day): ' + str(avg2) + '\n' + 'AirTemp: ' + str(airtemp2)
		message_all = message1 + '\n' + '\n' + message2
		print(message1)
		print(message2)



		# send to emails for users belonging to same beach as the data we selected
		# so, again, for this - we are using Nantasket
		conn5 = sqlite3.connect('SurfSend.db')
		cursor5 = conn5.cursor()
		cur5 = cursor5.execute('SELECT cellphone FROM ArtistMonitor WHERE DJName = "Nantasket"')
		info5 = cur5.fetchall()
		conn5.commit()
		conn5.close()
		conn5.close()

		cellphone_list = [row[0] for row in info5]

		for cell in cellphone_list:
			client = Client(account_sid, auth_token)
			message = client.messages.create(
			to=cell,
			from_="7817252098",
			body=message_all)

			# print(message.sid) #To print sid
			print(cell)













		# msg = MIMEMultipart()
		# msg['From'] = 'mkramer265@gmail.com'
		# msg['To'] = 'mkramer789@gmail.com'
		# msg['Subject'] = 'Funny'
		# # message = j + 'ft' ' @ ' + k + ' on ' + l
		# # print(message)
		# msg.attach(MIMEText(message_all))

		# mailserver = smtplib.SMTP('smtp.gmail.com',587)
		# # identify ourselves to smtp gmail client
		# mailserver.ehlo()
		# # secure our email with tls encryption
		# mailserver.starttls()
		# # re-identify ourselves as an encrypted connection
		# mailserver.ehlo()
		# mailserver.login('mkramer265@gmail.com', 'Celtics123')

		# mailserver.sendmail('mkramer265@gmail.com',cellphone_list,msg.as_string())

		# mailserver.quit()

		# connx = sqlite3.connect('StriveDB2.db')
		# cursorx = connx.cursor()
		# curx = cursorx.execute("INSERT INTO RIDX VALUES (?)", (k,))
		# connx.commit()
		# cursorx.close()
		# connx.close()
		break

	except UnicodeEncodeError:
		pass

print('We broke outside of the loop. That means we must have succeeded')
