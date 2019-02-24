from flask import *
from functools import wraps
import sqlite3
from flask_bootstrap import Bootstrap
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email, Length, EqualTo, DataRequired, ValidationError
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm, CsrfProtect
import smtplib
# from email.MIMEMultipart import MIMEMultipart
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from email.MIMEText import MIMEText
import pygal
from pygal.style import BlueStyle
from datetime import date
from datetime import timedelta
import calendar
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, TimedJSONWebSignatureSerializer as Serializer

from forms import (RequestResetForm, ResetPasswordForm, LoginForm,
                             RegisterForm, User, EmailForm, PasswordForm) 

# from folder import file
# k = file.Klasa()

# from Feb10_Cleanup import forms

# RequestResetForm = forms.RequestResetForm()
# ResetPasswordForm = forms.ResetPasswordForm()
# LoginForm = forms.LoginForm() 
# RegisterForm = forms.RegisterForm() 
# User = forms.User() 
# EmailForm = forms.EmailForm() 
# PasswordForm = forms.PasswordForm()  


artists = ['Solomun', 'Dubfire']

DATABASE = 'SurfSend.db'

app = Flask(__name__)
app.secret_key = 'my precious'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\Mike\\Desktop\\PythonSuccess\\Feb3_Moar\\SurfSend.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
app.config.from_object(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
csrf = CsrfProtect(app)
#new
bcrypt = Bcrypt(app)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'mkramer265@gmail.com'
app.config['MAIL_PASSWORD'] = 'Celtics123'
mail = Mail(app)


@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))

   
def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

@app.route('/')  
def home():
	return render_template('home.html')

@app.route('/welcome')
def welcome():
	return render_template('welcome.html')

# Corey ---------------------------------------------------------------------------------------------------------------
def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request',
				  sender='mkramer265@gmail.com',
				  recipients=[user.email])
	msg.body = '''To reset your password, visit the following link:
{url}
If you did not make this request then simply ignore this email and no changes will be made.
'''.format(url=url_for('reset_token', token=token, _external=True))

	mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An email has been sent with instructions to reset your password.', 'info')
		return redirect(url_for('login'))
	return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	user = User.verify_reset_token(token)
	if user is None:
		flash('That is an invalid or expired token', 'warning')
		return redirect(url_for('reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash('Your password has been updated! You are now able to log in', 'success')
		return redirect(url_for('login'))
	return render_template('reset_token.html', title='Reset Password', form=form)

# ---------------------------------------------------------------------------------------------------------------

#MSKnew
@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
	form = EmailForm()

	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user:
			# if check_password_hash(user.password, form.password.data):
			# 	login_user(user, remember=form.remember.data)
			# 	return redirect(url_for('scrapelist2'))

			email_list = 'mkramer265@gmail.com'

			user_name = form.username.data
			message_all = 'Hi ' + user_name + '!' + '\n' + '\n' + 'Heres your Password Reset link!' + '\n' + 'If you have any questions or things you would like to report, please email surfsendhelp@gmail.com.' + '\n' + '\n' + 'Warm Regards,' + '\n' + '	-Team SurfSend'

			msg = MIMEMultipart()
			msg['From'] = 'mkramer265@gmail.com'
			msg['To'] = 'mkramer789@gmail.com'
			msg['Subject'] = 'Thanks for Registering!'
			# message = j + 'ft' ' @ ' + k + ' on ' + l
			# print(message)
			msg.attach(MIMEText(message_all))

			mailserver = smtplib.SMTP('smtp.gmail.com',587)
			# identify ourselves to smtp gmail client
			mailserver.ehlo()
			# secure our email with tls encryption
			mailserver.starttls()
			# re-identify ourselves as an encrypted connection
			mailserver.ehlo()
			mailserver.login('mkramer265@gmail.com', 'Celtics123')

			mailserver.sendmail('mkramer265@gmail.com',email_list,msg.as_string())

			mailserver.quit()





		flash('Invalid Username/Password')
		#return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

	return render_template('reset_request.html', form=form)




#msknew
@app.route('/reset', methods=["GET", "POST"])
def reset():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first_or_404()
		if user:

			subject = "Password reset requested"

			# Here we use the URLSafeTimedSerializer we created in `util` at the
			# beginning of the chapter
			token = ts.dumps(user.email, salt='recover-key')

			recover_url = url_for(
				'reset_with_token',
				token=token,
				_external=True)

			html = render_template(
				'email/recover.html',
				recover_url=recover_url)

			# Let's assume that send_email was defined in myapp/util.py
			send_email(user.email, subject, html)


			email_list = form.email.data

			msg = MIMEMultipart()
			msg['From'] = 'mkramer265@gmail.com'
			msg['To'] = 'mkramer789@gmail.com'
			msg['Subject'] = 'Password Reset Link'
			# message = j + 'ft' ' @ ' + k + ' on ' + l
			# print(message)
			msg.attach(MIMEText(html))

			mailserver = smtplib.SMTP('smtp.gmail.com',587)
			# identify ourselves to smtp gmail client
			mailserver.ehlo()
			# secure our email with tls encryption
			mailserver.starttls()
			# re-identify ourselves as an encrypted connection
			mailserver.ehlo()
			mailserver.login('mkramer265@gmail.com', 'Celtics123')

			mailserver.sendmail('mkramer265@gmail.com',email_list,msg.as_string())

			mailserver.quit()



			flash('Password Reset Email Sent!')
		else:
			flash('User Doesnt Exist!')	
	return render_template('forgot.html', form=form)
	#msk


@app.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
	try:
		email = ts.loads(token, salt="recover-key", max_age=86400)
	except:
		abort(404)

	form = PasswordForm()

	if form.validate_on_submit():
		user = User.query.filter_by(email=email).first_or_404()

		user.password = form.password.data

		db.session.add(user)
		db.session.commit()

		return redirect(url_for('signin'))

	return render_template('reset_with_token.html', form=form, token=token)


#-------------------------- RHODE ISLAND BEACHES--------------------------------
@app.route('/TwoBeach')
@csrf.exempt
def TwoBeach():
	#responsible for getting X,Y values, both lists stored as variables mylist & newl
	conn = sqlite3.connect('SurfSend.db')
	conn.row_factory = lambda cursor, row: row[0]
	c = conn.cursor()
	# valuesx = c.execute("select swellsizeft from surfmaster2 where beach_name = '2nd Beach' and date_ = '2018-11-23'").fetchall()
	values = c.execute("select distinct avg_day from surfmaster2 where beach_name ='2nd Beach'").fetchall()

	mmm = [float(i) for i in values]

	labels = c.execute("select distinct date_ from surfmaster2").fetchall()
	mylist = []
	for l in labels:
		dates = l[5:]
		mylist.append(str(dates))
	print(mylist)
	print(mmm)

	#code responsible for graphing the pygal chart ... using data from the DB, from list objects mylist & newl
	graph = pygal.Line()
	graph.title = '2nd Beach 7 Day Surf Forecast'
	graph.x_labels = mylist
	graph.add('Avg Wave Height',  mmm)
	graph_data = graph.render_data_uri()
	#original code, used for creating table in Nahant.html

	# getdate() table
	conn = sqlite3.connect('SurfSend.db')
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='2nd Beach' and date_ = date('now') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info1 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='2nd Beach' and date_ = date('now')")
	info2 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+1 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='2nd Beach' and date_ = date('now','+1 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info3 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+1
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='2nd Beach' and date_ = date('now','+1 day')")
	info4 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+2 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='2nd Beach' and date_ = date('now','+2 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info5 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+2
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='2nd Beach' and date_ = date('now','+2 day')")
	info6 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+3 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='2nd Beach' and date_ = date('now','+3 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info7 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+3
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='2nd Beach' and date_ = date('now','+3 day')")
	info8 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+4 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='2nd Beach' and date_ = date('now','+4 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info9 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+4
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='2nd Beach' and date_ = date('now','+4 day')")
	info10 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+5 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='2nd Beach' and date_ = date('now','+5 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info11 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+5
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='2nd Beach' and date_ = date('now','+5 day')")
	info12 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+6 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='2nd Beach' and date_ = date('now','+6 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info13 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+5
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='2nd Beach' and date_ = date('now','+6 day')")
	info14 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# CurrentSurfConditions in page header
	# For now, setting all 'current conditions' to mid-day conditions (time_ = 12pm)
	cursor = conn.cursor()
	cursor.execute("select swellsizeft, swellintervalsec, windmph, airtemp, WindDescription from surfmaster2 where date_ = date('now') and time_ = '12pm' and beach_name = '2nd Beach'")
	info15 = [dict(SwellSizeFt1=row[0], SwellIntervalSec1=row[1], WindMPH1=row[2], AirTemp1=row[3], WindDescription1=row[4]) for row in cursor.fetchall()]
	cursor.close()

	return render_template('TwoBeach.html', selected='submit',info1=info1, info2=info2, info3=info3, info4=info4, info5=info5, info6=info6, info7=info7, info8=info8,  info9=info9,  info10=info10,  info11=info11,  info12=info12,  info13=info13,  info14=info14, info15=info15,  graph_data=graph_data)


@app.route('/Narragansett')
@csrf.exempt
def Narragansett():
	#responsible for getting X,Y values, both lists stored as variables mylist & newl
	conn = sqlite3.connect('SurfSend.db')
	conn.row_factory = lambda cursor, row: row[0]
	c = conn.cursor()
	# valuesx = c.execute("select swellsizeft from surfmaster2 where beach_name = '2nd Beach' and date_ = '2018-11-23'").fetchall()
	values = c.execute("select distinct avg_day from surfmaster2 where beach_name ='Narragansett'").fetchall()

	mmm = [float(i) for i in values]

	labels = c.execute("select distinct date_ from surfmaster2").fetchall()
	mylist = []
	for l in labels:
		dates = l[5:]
		mylist.append(str(dates))
	print(mylist)
	print(mmm)

	#code responsible for graphing the pygal chart ... using data from the DB, from list objects mylist & newl
	graph = pygal.Line()
	graph.title = 'Narragansett 7 Day Surf Forecast'
	graph.x_labels = mylist
	graph.add('Avg Wave Height',  mmm)
	graph_data = graph.render_data_uri()
	#original code, used for creating table in Nahant.html

	# getdate() table
	conn = sqlite3.connect('SurfSend.db')
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Narragansett' and date_ = date('now') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info1 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Narragansett' and date_ = date('now')")
	info2 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+1 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Narragansett' and date_ = date('now','+1 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info3 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+1
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Narragansett' and date_ = date('now','+1 day')")
	info4 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+2 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Narragansett' and date_ = date('now','+2 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info5 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+2
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Narragansett' and date_ = date('now','+2 day')")
	info6 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+3 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Narragansett' and date_ = date('now','+3 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info7 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+3
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Narragansett' and date_ = date('now','+3 day')")
	info8 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+4 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Narragansett' and date_ = date('now','+4 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info9 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+4
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Narragansett' and date_ = date('now','+4 day')")
	info10 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+5 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Narragansett' and date_ = date('now','+5 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info11 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+5
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Narragansett' and date_ = date('now','+5 day')")
	info12 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+6 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Narragansett' and date_ = date('now','+6 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info13 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+5
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Narragansett' and date_ = date('now','+6 day')")
	info14 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# CurrentSurfConditions in page header
	# For now, setting all 'current conditions' to mid-day conditions (time_ = 12pm)
	cursor = conn.cursor()
	cursor.execute("select swellsizeft, swellintervalsec, windmph, airtemp, WindDescription from surfmaster2 where date_ = date('now') and time_ = '12pm' and beach_name = 'Narragansett'")
	info15 = [dict(SwellSizeFt1=row[0], SwellIntervalSec1=row[1], WindMPH1=row[2], AirTemp1=row[3], WindDescription1=row[4]) for row in cursor.fetchall()]
	cursor.close()



	return render_template('Narragansett.html', selected='submit',info1=info1, info2=info2, info3=info3, info4=info4, info5=info5, info6=info6, info7=info7, info8=info8,  info9=info9,  info10=info10,  info11=info11,  info12=info12,  info13=info13,  info14=info14, info15=info15,  graph_data=graph_data)



@app.route('/Ruggles')
@csrf.exempt
def Ruggles():
	#responsible for getting X,Y values, both lists stored as variables mylist & newl
	conn = sqlite3.connect('SurfSend.db')
	conn.row_factory = lambda cursor, row: row[0]
	c = conn.cursor()
	# valuesx = c.execute("select swellsizeft from surfmaster2 where beach_name = '2nd Beach' and date_ = '2018-11-23'").fetchall()
	values = c.execute("select distinct avg_day from surfmaster2 where beach_name ='Ruggles'").fetchall()

	mmm = [float(i) for i in values]

	labels = c.execute("select distinct date_ from surfmaster2").fetchall()
	mylist = []
	for l in labels:
		dates = l[5:]
		mylist.append(str(dates))
	print(mylist)
	print(mmm)

	#code responsible for graphing the pygal chart ... using data from the DB, from list objects mylist & newl
	graph = pygal.Line()
	graph.title = 'Ruggles 7 Day Surf Forecast'
	graph.x_labels = mylist
	graph.add('Avg Wave Height',  mmm)
	graph_data = graph.render_data_uri()
	#original code, used for creating table in Nahant.html

	# getdate() table
	conn = sqlite3.connect('SurfSend.db')
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Ruggles' and date_ = date('now') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info1 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Ruggles' and date_ = date('now')")
	info2 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+1 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Ruggles' and date_ = date('now','+1 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info3 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+1
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Ruggles' and date_ = date('now','+1 day')")
	info4 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+2 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Ruggles' and date_ = date('now','+2 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info5 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+2
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Ruggles' and date_ = date('now','+2 day')")
	info6 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+3 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Ruggles' and date_ = date('now','+3 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info7 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+3
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Ruggles' and date_ = date('now','+3 day')")
	info8 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+4 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Ruggles' and date_ = date('now','+4 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info9 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+4
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Ruggles' and date_ = date('now','+4 day')")
	info10 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+5 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Ruggles' and date_ = date('now','+5 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info11 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+5
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Ruggles' and date_ = date('now','+5 day')")
	info12 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+6 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Ruggles' and date_ = date('now','+6 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info13 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+5
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Ruggles' and date_ = date('now','+6 day')")
	info14 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# CurrentSurfConditions in page header
	# For now, setting all 'current conditions' to mid-day conditions (time_ = 12pm)
	cursor = conn.cursor()
	cursor.execute("select swellsizeft, swellintervalsec, windmph, airtemp, WindDescription from surfmaster2 where date_ = date('now') and time_ = '12pm' and beach_name = 'Ruggles'")
	info15 = [dict(SwellSizeFt1=row[0], SwellIntervalSec1=row[1], WindMPH1=row[2], AirTemp1=row[3], WindDescription1=row[4]) for row in cursor.fetchall()]
	cursor.close()



	return render_template('Ruggles.html', selected='submit',info1=info1, info2=info2, info3=info3, info4=info4, info5=info5, info6=info6, info7=info7, info8=info8,  info9=info9,  info10=info10,  info11=info11,  info12=info12,  info13=info13,  info14=info14, info15=info15,  graph_data=graph_data)



#--------------------------MA BEACHES--------------------------------




@app.route('/Nahant')
@csrf.exempt
def Nahant():
	#responsible for getting X,Y values, both lists stored as variables mylist & newl
	conn = sqlite3.connect('SurfSend.db')
	conn.row_factory = lambda cursor, row: row[0]
	c = conn.cursor()
	# valuesx = c.execute("select swellsizeft from surfmaster2 where beach_name = '2nd Beach' and date_ = '2018-11-23'").fetchall()
	values = c.execute("select distinct avg_day from surfmaster2 where beach_name ='Nahant'").fetchall()

	mmm = [float(i) for i in values]

	labels = c.execute("select distinct date_ from surfmaster2").fetchall()
	mylist = []
	for l in labels:
		dates = l[5:]
		mylist.append(str(dates))

	# WEEKDAY NAME, GETDATE()
	my_date = date.today()
	day_today = calendar.day_name[my_date.weekday()]

	# MM/DD
	mmdd = mylist[0]

	# CONCAT WEEKDAY NAME + MM/DD, GETDATE()
	date_fin = day_today + " " + mmdd
	print(date_fin)



	# WEEKDAY NAME, GETDATE()+1
	day_plus1 = datetime.now() + timedelta(days=1)
	d1 = calendar.day_name[day_plus1.weekday()]

	# MM/DD
	mmdd = mylist[1]

	# CONCAT WEEKDAY NAME + MM/DD, GETDATE()+1
	date_fin1 = d1 + " " + mmdd
	print(date_fin1)


	# WEEKDAY NAME, GETDATE()+2
	day_plus2 = datetime.now() + timedelta(days=2)
	d2 = calendar.day_name[day_plus2.weekday()]

	# MM/DD
	mmdd = mylist[2]

	# CONCAT WEEKDAY NAME + MM/DD, GETDATE()+2
	date_fin2 = d2 + " " + mmdd
	print(date_fin2)


	# WEEKDAY NAME, GETDATE()+3
	day_plus3 = datetime.now() + timedelta(days=3)
	d3 = calendar.day_name[day_plus3.weekday()]

	# MM/DD
	mmdd = mylist[3]

	# CONCAT WEEKDAY NAME + MM/DD, GETDATE()+3
	date_fin3 = d3 + " " + mmdd
	print(date_fin3)


	# WEEKDAY NAME, GETDATE()+4
	day_plus4 = datetime.now() + timedelta(days=4)
	d4 = calendar.day_name[day_plus4.weekday()]

	# MM/DD
	mmdd = mylist[4]

	# CONCAT WEEKDAY NAME + MM/DD, GETDATE()+4
	date_fin4 = d4 + " " + mmdd
	print(date_fin4)


	# WEEKDAY NAME, GETDATE()+5
	day_plus5 = datetime.now() + timedelta(days=5)
	d5 = calendar.day_name[day_plus5.weekday()]

	# MM/DD
	mmdd = mylist[5]

	# CONCAT WEEKDAY NAME + MM/DD, GETDATE()+5
	date_fin5 = d5 + " " + mmdd
	print(date_fin5)


	# WEEKDAY NAME, GETDATE()+6
	day_plus6 = datetime.now() + timedelta(days=6)
	d6 = calendar.day_name[day_plus6.weekday()]

	# MM/DD
	mmdd = mylist[6]

	# CONCAT WEEKDAY NAME + MM/DD, GETDATE()+6
	date_fin6 = d6 + " " + mmdd
	print(date_fin6)



	#code responsible for graphing the pygal chart ... using data from the DB, from list objects mylist & newl
	graph = pygal.Line(fill=True, interpolate='cubic', label_font_size=66)
	graph.title = 'Nahant 7 Day Surf Forecast'
	graph.x_labels = mylist
	graph.add('Avg Wave Height',  mmm)
	graph_data = graph.render_data_uri()
	#original code, used for creating table in Nahant.html

	# getdate() table
	conn = sqlite3.connect('SurfSend.db')
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Nahant' and date_ = date('now') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info1 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Nahant' and date_ = date('now')")
	info2 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+1 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Nahant' and date_ = date('now','+1 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info3 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+1
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Nahant' and date_ = date('now','+1 day')")
	info4 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+2 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Nahant' and date_ = date('now','+2 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info5 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+2
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Nahant' and date_ = date('now','+2 day')")
	info6 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+3 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Nahant' and date_ = date('now','+3 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info7 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+3
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Nahant' and date_ = date('now','+3 day')")
	info8 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+4 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Nahant' and date_ = date('now','+4 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info9 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+4
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Nahant' and date_ = date('now','+4 day')")
	info10 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+5 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Nahant' and date_ = date('now','+5 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info11 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+5
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Nahant' and date_ = date('now','+5 day')")
	info12 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+6 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Nahant' and date_ = date('now','+6 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info13 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+6
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Nahant' and date_ = date('now','+6 day')")
	info14 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# CurrentSurfConditions in page header
	# For now, setting all 'current conditions' to mid-day conditions (time_ = 12pm)
	cursor = conn.cursor()
	cursor.execute("select swellsizeft, swellintervalsec, windmph, airtemp, WindDescription from surfmaster2 where date_ = date('now') and time_ = '12pm' and beach_name = 'Nahant'")
	info15 = [dict(SwellSizeFt1=row[0], SwellIntervalSec1=row[1], WindMPH1=row[2], AirTemp1=row[3], WindDescription1=row[4]) for row in cursor.fetchall()]
	cursor.close()

	return render_template('Nahant.html', selected='submit',info1=info1, info2=info2, info3=info3, info4=info4, info5=info5, info6=info6, info7=info7, info8=info8,  info9=info9,  info10=info10,  info11=info11,  info12=info12,  info13=info13,  info14=info14, info15=info15, date_fin=date_fin, date_fin1=date_fin1, date_fin2=date_fin2, date_fin3=date_fin3, date_fin4=date_fin4, date_fin5=date_fin5, date_fin6=date_fin6, graph_data=graph_data)


@app.route('/Nantasket')
@csrf.exempt
def Nantasket():
	#responsible for getting X,Y values, both lists stored as variables mylist & newl
	conn = sqlite3.connect('SurfSend.db')
	conn.row_factory = lambda cursor, row: row[0]
	c = conn.cursor()
	# valuesx = c.execute("select swellsizeft from surfmaster2 where beach_name = '2nd Beach' and date_ = '2018-11-23'").fetchall()
	values = c.execute("select distinct avg_day from surfmaster2 where beach_name ='Nantasket'").fetchall()

	mmm = [float(i) for i in values]

	labels = c.execute("select distinct date_ from surfmaster2").fetchall()
	mylist = []
	for l in labels:
		dates = l[5:]
		mylist.append(str(dates))
	print(mylist)
	print(mmm)

	#code responsible for graphing the pygal chart ... using data from the DB, from list objects mylist & newl
	graph = pygal.Line()
	graph.title = 'Nantasket 7 Day Surf Forecast'
	graph.x_labels = mylist
	graph.add('Avg Wave Height',  mmm)
	graph_data = graph.render_data_uri()
	#original code, used for creating table in Nahant.html

	# getdate() table
	conn = sqlite3.connect('SurfSend.db')
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Nantasket' and date_ = date('now') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info1 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Nantasket' and date_ = date('now')")
	info2 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+1 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Nantasket' and date_ = date('now','+1 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info3 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+1
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Nantasket' and date_ = date('now','+1 day')")
	info4 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+2 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Nantasket' and date_ = date('now','+2 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info5 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+2
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Nantasket' and date_ = date('now','+2 day')")
	info6 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+3 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Nantasket' and date_ = date('now','+3 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info7 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+3
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Nantasket' and date_ = date('now','+3 day')")
	info8 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+4 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Nantasket' and date_ = date('now','+4 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info9 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+4
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Nantasket' and date_ = date('now','+4 day')")
	info10 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+5 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Nantasket' and date_ = date('now','+5 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info11 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+5
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Nantasket' and date_ = date('now','+5 day')")
	info12 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+6 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Nantasket' and date_ = date('now','+6 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info13 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+6
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Nantasket' and date_ = date('now','+6 day')")
	info14 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# CurrentSurfConditions in page header
	# For now, setting all 'current conditions' to mid-day conditions (time_ = 12pm)
	cursor = conn.cursor()
	cursor.execute("select swellsizeft, swellintervalsec, windmph, airtemp, WindDescription from surfmaster2 where date_ = date('now') and time_ = '12pm' and beach_name = 'Nantasket'")
	info15 = [dict(SwellSizeFt1=row[0], SwellIntervalSec1=row[1], WindMPH1=row[2], AirTemp1=row[3], WindDescription1=row[4]) for row in cursor.fetchall()]
	cursor.close()



	return render_template('Nantasket.html', selected='submit',info1=info1, info2=info2, info3=info3, info4=info4, info5=info5, info6=info6, info7=info7, info8=info8,  info9=info9,  info10=info10,  info11=info11,  info12=info12,  info13=info13,  info14=info14, info15=info15,  graph_data=graph_data)


@app.route('/Scituate')
@csrf.exempt
def Scituate():
	#responsible for getting X,Y values, both lists stored as variables mylist & newl
	conn = sqlite3.connect('SurfSend.db')
	conn.row_factory = lambda cursor, row: row[0]
	c = conn.cursor()
	# valuesx = c.execute("select swellsizeft from surfmaster2 where beach_name = '2nd Beach' and date_ = '2018-11-23'").fetchall()
	values = c.execute("select distinct avg_day from surfmaster2 where beach_name ='Scituate'").fetchall()

	mmm = [float(i) for i in values]

	labels = c.execute("select distinct date_ from surfmaster2").fetchall()
	mylist = []
	for l in labels:
		dates = l[5:]
		mylist.append(str(dates))
	print(mylist)
	print(mmm)

	#code responsible for graphing the pygal chart ... using data from the DB, from list objects mylist & newl
	graph = pygal.Line()
	graph.title = 'Scituate 7 Day Surf Forecast'
	graph.x_labels = mylist
	graph.add('Avg Wave Height',  mmm)
	graph_data = graph.render_data_uri()
	#original code, used for creating table in Nahant.html

	# getdate() table
	conn = sqlite3.connect('SurfSend.db')
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Scituate' and date_ = date('now') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info1 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Scituate' and date_ = date('now')")
	info2 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+1 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Scituate' and date_ = date('now','+1 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info3 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+1
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Scituate' and date_ = date('now','+1 day')")
	info4 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+2 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Scituate' and date_ = date('now','+2 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info5 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+2
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Scituate' and date_ = date('now','+2 day')")
	info6 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+3 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Scituate' and date_ = date('now','+3 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info7 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+3
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Scituate' and date_ = date('now','+3 day')")
	info8 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+4 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Scituate' and date_ = date('now','+4 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info9 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+4
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Scituate' and date_ = date('now','+4 day')")
	info10 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+5 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Scituate' and date_ = date('now','+5 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info11 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+5
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Scituate' and date_ = date('now','+5 day')")
	info12 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+6 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Scituate' and date_ = date('now','+6 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info13 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+5
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Scituate' and date_ = date('now','+6 day')")
	info14 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# CurrentSurfConditions in page header
	# For now, setting all 'current conditions' to mid-day conditions (time_ = 12pm)
	cursor = conn.cursor()
	cursor.execute("select swellsizeft, swellintervalsec, windmph, airtemp, WindDescription from surfmaster2 where date_ = date('now') and time_ = '12pm' and beach_name = 'Scituate'")
	info15 = [dict(SwellSizeFt1=row[0], SwellIntervalSec1=row[1], WindMPH1=row[2], AirTemp1=row[3], WindDescription1=row[4]) for row in cursor.fetchall()]
	cursor.close()

	return render_template('Scituate.html', selected='submit',info1=info1, info2=info2, info3=info3, info4=info4, info5=info5, info6=info6, info7=info7, info8=info8,  info9=info9,  info10=info10,  info11=info11,  info12=info12,  info13=info13,  info14=info14, info15=info15,  graph_data=graph_data)


@app.route('/CapeCod')
@csrf.exempt
def CapeCod():
	#responsible for getting X,Y values, both lists stored as variables mylist & newl
	conn = sqlite3.connect('SurfSend.db')
	conn.row_factory = lambda cursor, row: row[0]
	c = conn.cursor()
	# valuesx = c.execute("select swellsizeft from surfmaster2 where beach_name = '2nd Beach' and date_ = '2018-11-23'").fetchall()
	values = c.execute("select distinct avg_day from surfmaster2 where beach_name ='Cape Cod'").fetchall()

	mmm = [float(i) for i in values]

	labels = c.execute("select distinct date_ from surfmaster2").fetchall()
	mylist = []
	for l in labels:
		dates = l[5:]
		mylist.append(str(dates))
	print(mylist)
	print(mmm)

	#code responsible for graphing the pygal chart ... using data from the DB, from list objects mylist & newl
	graph = pygal.Line()
	graph.title = 'Cape Cod 7 Day Surf Forecast'
	graph.x_labels = mylist
	graph.add('Avg Wave Height',  mmm)
	graph_data = graph.render_data_uri()
	#original code, used for creating table in Nahant.html

	# getdate() table
	conn = sqlite3.connect('SurfSend.db')
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Cape Cod' and date_ = date('now') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info1 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Cape Cod' and date_ = date('now')")
	info2 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+1 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Cape Cod' and date_ = date('now','+1 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info3 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+1
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Cape Cod' and date_ = date('now','+1 day')")
	info4 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+2 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Cape Cod' and date_ = date('now','+2 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info5 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+2
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Cape Cod' and date_ = date('now','+2 day')")
	info6 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+3 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Cape Cod' and date_ = date('now','+3 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info7 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+3
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Cape Cod' and date_ = date('now','+3 day')")
	info8 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+4 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Cape Cod' and date_ = date('now','+4 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info9 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+4
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Cape Cod' and date_ = date('now','+4 day')")
	info10 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+5 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Cape Cod' and date_ = date('now','+5 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info11 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+5
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Cape Cod' and date_ = date('now','+5 day')")
	info12 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+6 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Cape Cod' and date_ = date('now','+6 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info13 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+5
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Cape Cod' and date_ = date('now','+6 day')")
	info14 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# CurrentSurfConditions in page header
	# For now, setting all 'current conditions' to mid-day conditions (time_ = 12pm)
	cursor = conn.cursor()
	cursor.execute("select swellsizeft, swellintervalsec, windmph, airtemp, WindDescription from surfmaster2 where date_ = date('now') and time_ = '12pm' and beach_name = 'Cape Cod'")
	info15 = [dict(SwellSizeFt1=row[0], SwellIntervalSec1=row[1], WindMPH1=row[2], AirTemp1=row[3], WindDescription1=row[4]) for row in cursor.fetchall()]
	cursor.close()



	return render_template('CapeCod.html', selected='submit',info1=info1, info2=info2, info3=info3, info4=info4, info5=info5, info6=info6, info7=info7, info8=info8,  info9=info9,  info10=info10,  info11=info11,  info12=info12,  info13=info13,  info14=info14, info15=info15,  graph_data=graph_data)


@app.route('/GreenHarbor')
@csrf.exempt
def GreenHarbor():
	#responsible for getting X,Y values, both lists stored as variables mylist & newl
	conn = sqlite3.connect('SurfSend.db')
	conn.row_factory = lambda cursor, row: row[0]
	c = conn.cursor()
	# valuesx = c.execute("select swellsizeft from surfmaster2 where beach_name = '2nd Beach' and date_ = '2018-11-23'").fetchall()
	values = c.execute("select distinct avg_day from surfmaster2 where beach_name ='Green Harbor'").fetchall()

	mmm = [float(i) for i in values]

	labels = c.execute("select distinct date_ from surfmaster2").fetchall()
	mylist = []
	for l in labels:
		dates = l[5:]
		mylist.append(str(dates))
	print(mylist)
	print(mmm)

	#code responsible for graphing the pygal chart ... using data from the DB, from list objects mylist & newl
	graph = pygal.Line()
	graph.title = 'Green Harbor 7 Day Surf Forecast'
	graph.x_labels = mylist
	graph.add('Avg Wave Height',  mmm)
	graph_data = graph.render_data_uri()
	#original code, used for creating table in Nahant.html

	# getdate() table
	conn = sqlite3.connect('SurfSend.db')
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name = 'Green Harbor' and date_ = date('now') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info1 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name = 'Green Harbor' and date_ = date('now')")
	info2 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+1 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name = 'Green Harbor' and date_ = date('now','+1 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info3 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+1
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name = 'Green Harbor' and date_ = date('now','+1 day')")
	info4 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+2 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name = 'Green Harbor' and date_ = date('now','+2 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info5 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+2
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name = 'Green Harbor' and date_ = date('now','+2 day')")
	info6 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+3 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name = 'Green Harbor' and date_ = date('now','+3 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info7 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+3
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name = 'Green Harbor' and date_ = date('now','+3 day')")
	info8 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+4 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name = 'Green Harbor' and date_ = date('now','+4 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info9 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+4
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name = 'Green Harbor' and date_ = date('now','+4 day')")
	info10 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+5 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name = 'Green Harbor' and date_ = date('now','+5 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info11 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+5
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name = 'Green Harbor' and date_ = date('now','+5 day')")
	info12 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+6 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name = 'Green Harbor' and date_ = date('now','+6 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info13 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+5
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name = 'Green Harbor' and date_ = date('now','+6 day')")
	info14 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# CurrentSurfConditions in page header
	# For now, setting all 'current conditions' to mid-day conditions (time_ = 12pm)
	cursor = conn.cursor()
	cursor.execute("select swellsizeft, swellintervalsec, windmph, airtemp, WindDescription from surfmaster2 where date_ = date('now') and time_ = '12pm' and beach_name = 'Green Harbor'")
	info15 = [dict(SwellSizeFt1=row[0], SwellIntervalSec1=row[1], WindMPH1=row[2], AirTemp1=row[3], WindDescription1=row[4]) for row in cursor.fetchall()]
	cursor.close()



	return render_template('GreenHarbor.html', selected='submit',info1=info1, info2=info2, info3=info3, info4=info4, info5=info5, info6=info6, info7=info7, info8=info8,  info9=info9,  info10=info10,  info11=info11,  info12=info12,  info13=info13,  info14=info14, info15=info15,  graph_data=graph_data)

@app.route('/CapeAnn')
@csrf.exempt
def CapeAnn():
	#responsible for getting X,Y values, both lists stored as variables mylist & newl
	conn = sqlite3.connect('SurfSend.db')
	conn.row_factory = lambda cursor, row: row[0]
	c = conn.cursor()
	# valuesx = c.execute("select swellsizeft from surfmaster2 where beach_name = '2nd Beach' and date_ = '2018-11-23'").fetchall()
	values = c.execute("select distinct avg_day from surfmaster2 where beach_name ='Cape Ann'").fetchall()

	mmm = [float(i) for i in values]

	labels = c.execute("select distinct date_ from surfmaster2").fetchall()
	mylist = []
	for l in labels:
		dates = l[5:]
		mylist.append(str(dates))
	print(mylist)
	print(mmm)

	#code responsible for graphing the pygal chart ... using data from the DB, from list objects mylist & newl
	graph = pygal.Line()
	graph.title = 'Cape Ann 7 Day Surf Forecast'
	graph.x_labels = mylist
	graph.add('Avg Wave Height',  mmm)
	graph_data = graph.render_data_uri()
	#original code, used for creating table in Nahant.html

	# getdate() table
	conn = sqlite3.connect('SurfSend.db')
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name = 'Cape Ann' and date_ = date('now') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info1 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name = 'Cape Ann' and date_ = date('now')")
	info2 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+1 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name = 'Cape Ann' and date_ = date('now','+1 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info3 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+1
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name = 'Cape Ann' and date_ = date('now','+1 day')")
	info4 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+2 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name = 'Cape Ann' and date_ = date('now','+2 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info5 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+2
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name = 'Cape Ann' and date_ = date('now','+2 day')")
	info6 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+3 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name = 'Cape Ann' and date_ = date('now','+3 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info7 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+3
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name = 'Cape Ann' and date_ = date('now','+3 day')")
	info8 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+4 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name = 'Cape Ann' and date_ = date('now','+4 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info9 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+4
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name = 'Cape Ann' and date_ = date('now','+4 day')")
	info10 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+5 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name = 'Cape Ann' and date_ = date('now','+5 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info11 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+5
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name = 'Cape Ann' and date_ = date('now','+5 day')")
	info12 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+6 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name = 'Cape Ann' and date_ = date('now','+6 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info13 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+5
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name = 'Cape Ann' and date_ = date('now','+6 day')")
	info14 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# CurrentSurfConditions in page header
	# For now, setting all 'current conditions' to mid-day conditions (time_ = 12pm)
	cursor = conn.cursor()
	cursor.execute("select swellsizeft, swellintervalsec, windmph, airtemp, WindDescription from surfmaster2 where date_ = date('now') and time_ = '12pm' and beach_name = 'Cape Ann'")
	info15 = [dict(SwellSizeFt1=row[0], SwellIntervalSec1=row[1], WindMPH1=row[2], AirTemp1=row[3], WindDescription1=row[4]) for row in cursor.fetchall()]
	cursor.close()



	return render_template('CapeAnn.html', selected='submit',info1=info1, info2=info2, info3=info3, info4=info4, info5=info5, info6=info6, info7=info7, info8=info8,  info9=info9,  info10=info10,  info11=info11,  info12=info12,  info13=info13,  info14=info14, info15=info15,  graph_data=graph_data)


@app.route('/Devereux')
@csrf.exempt
def Devereux():
	#responsible for getting X,Y values, both lists stored as variables mylist & newl
	conn = sqlite3.connect('SurfSend.db')
	conn.row_factory = lambda cursor, row: row[0]
	c = conn.cursor()
	# valuesx = c.execute("select swellsizeft from surfmaster2 where beach_name = '2nd Beach' and date_ = '2018-11-23'").fetchall()
	values = c.execute("select distinct avg_day from surfmaster2 where beach_name ='Devereux Beach'").fetchall()

	mmm = [float(i) for i in values]

	labels = c.execute("select distinct date_ from surfmaster2").fetchall()
	mylist = []
	for l in labels:
		dates = l[5:]
		mylist.append(str(dates))
	print(mylist)
	print(mmm)

	#code responsible for graphing the pygal chart ... using data from the DB, from list objects mylist & newl
	graph = pygal.Line()
	graph.title = 'Devereux Beach 7 Day Surf Forecast'
	graph.x_labels = mylist
	graph.add('Avg Wave Height',  mmm)
	graph_data = graph.render_data_uri()
	#original code, used for creating table in Nahant.html

	# getdate() table
	conn = sqlite3.connect('SurfSend.db')
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Devereux Beach' and date_ = date('now') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info1 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Devereux Beach' and date_ = date('now')")
	info2 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+1 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Devereux Beach' and date_ = date('now','+1 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info3 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+1
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Devereux Beach' and date_ = date('now','+1 day')")
	info4 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+2 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Devereux Beach' and date_ = date('now','+2 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info5 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+2
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Devereux Beach' and date_ = date('now','+2 day')")
	info6 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+3 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Devereux Beach' and date_ = date('now','+3 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info7 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+3
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Devereux Beach' and date_ = date('now','+3 day')")
	info8 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+4 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Devereux Beach' and date_ = date('now','+4 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info9 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+4
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Devereux Beach' and date_ = date('now','+4 day')")
	info10 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+5 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Devereux Beach' and date_ = date('now','+5 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info11 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+5
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Devereux Beach' and date_ = date('now','+5 day')")
	info12 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+6 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Devereux Beach' and date_ = date('now','+6 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info13 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+5
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Devereux Beach' and date_ = date('now','+6 day')")
	info14 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# CurrentSurfConditions in page header
	# For now, setting all 'current conditions' to mid-day conditions (time_ = 12pm)
	cursor = conn.cursor()
	cursor.execute("select swellsizeft, swellintervalsec, windmph, airtemp, WindDescription from surfmaster2 where date_ = date('now') and time_ = '12pm' and beach_name = 'Devereux Beach'")
	info15 = [dict(SwellSizeFt1=row[0], SwellIntervalSec1=row[1], WindMPH1=row[2], AirTemp1=row[3], WindDescription1=row[4]) for row in cursor.fetchall()]
	cursor.close()


	return render_template('Devereux.html', selected='submit',info1=info1, info2=info2, info3=info3, info4=info4, info5=info5, info6=info6, info7=info7, info8=info8,  info9=info9,  info10=info10,  info11=info11,  info12=info12,  info13=info13,  info14=info14, info15=info15,  graph_data=graph_data)


@app.route('/Salisbury')
@csrf.exempt
def Salisbury():
	#responsible for getting X,Y values, both lists stored as variables mylist & newl
	conn = sqlite3.connect('SurfSend.db')
	conn.row_factory = lambda cursor, row: row[0]
	c = conn.cursor()
	# valuesx = c.execute("select swellsizeft from surfmaster2 where beach_name = '2nd Beach' and date_ = '2018-11-23'").fetchall()
	values = c.execute("select distinct avg_day from surfmaster2 where beach_name ='Salisbury'").fetchall()

	mmm = [float(i) for i in values]

	labels = c.execute("select distinct date_ from surfmaster2").fetchall()
	mylist = []
	for l in labels:
		dates = l[5:]
		mylist.append(str(dates))
	print(mylist)
	print(mmm)

	#code responsible for graphing the pygal chart ... using data from the DB, from list objects mylist & newl
	graph = pygal.Line()
	graph.title = 'Salisbury Beach 7 Day Surf Forecast'
	graph.x_labels = mylist
	graph.add('Avg Wave Height',  mmm)
	graph_data = graph.render_data_uri()
	#original code, used for creating table in Nahant.html

	# getdate() table
	conn = sqlite3.connect('SurfSend.db')
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Salisbury' and date_ = date('now') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info1 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Salisbury' and date_ = date('now')")
	info2 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+1 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Salisbury' and date_ = date('now','+1 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info3 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+1
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Salisbury' and date_ = date('now','+1 day')")
	info4 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+2 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Salisbury' and date_ = date('now','+2 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info5 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+2
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Salisbury' and date_ = date('now','+2 day')")
	info6 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+3 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Salisbury' and date_ = date('now','+3 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info7 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+3
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Salisbury' and date_ = date('now','+3 day')")
	info8 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+4 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Salisbury' and date_ = date('now','+4 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info9 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+4
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Salisbury' and date_ = date('now','+4 day')")
	info10 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+5 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Salisbury' and date_ = date('now','+5 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info11 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+5
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Salisbury' and date_ = date('now','+5 day')")
	info12 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+6 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Salisbury' and date_ = date('now','+6 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info13 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+5
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Salisbury' and date_ = date('now','+6 day')")
	info14 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# CurrentSurfConditions in page header
	# For now, setting all 'current conditions' to mid-day conditions (time_ = 12pm)
	cursor = conn.cursor()
	cursor.execute("select swellsizeft, swellintervalsec, windmph, airtemp, WindDescription from surfmaster2 where date_ = date('now') and time_ = '12pm' and beach_name = 'Salisbury'")
	info15 = [dict(SwellSizeFt1=row[0], SwellIntervalSec1=row[1], WindMPH1=row[2], AirTemp1=row[3], WindDescription1=row[4]) for row in cursor.fetchall()]
	cursor.close()



	return render_template('Salisbury.html', selected='submit',info1=info1, info2=info2, info3=info3, info4=info4, info5=info5, info6=info6, info7=info7, info8=info8,  info9=info9,  info10=info10,  info11=info11,  info12=info12,  info13=info13,  info14=info14, info15=info15,  graph_data=graph_data)

@app.route('/Plymouth')
@csrf.exempt
def Plymouth():
	#responsible for getting X,Y values, both lists stored as variables mylist & newl
	conn = sqlite3.connect('SurfSend.db')
	conn.row_factory = lambda cursor, row: row[0]
	c = conn.cursor()
	# valuesx = c.execute("select swellsizeft from surfmaster2 where beach_name = '2nd Beach' and date_ = '2018-11-23'").fetchall()
	values = c.execute("select distinct avg_day from surfmaster2 where beach_name ='Plymouth'").fetchall()

	mmm = [float(i) for i in values]

	labels = c.execute("select distinct date_ from surfmaster2").fetchall()
	mylist = []
	for l in labels:
		dates = l[5:]
		mylist.append(str(dates))
	print(mylist)
	print(mmm)

	#code responsible for graphing the pygal chart ... using data from the DB, from list objects mylist & newl
	graph = pygal.Line()
	graph.title = 'Plymouth Beach 7 Day Surf Forecast'
	graph.x_labels = mylist
	graph.add('Avg Wave Height',  mmm)
	graph_data = graph.render_data_uri()
	#original code, used for creating table in Nahant.html

	# getdate() table
	conn = sqlite3.connect('SurfSend.db')
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Plymouth' and date_ = date('now') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info1 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Plymouth' and date_ = date('now')")
	info2 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+1 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Plymouth' and date_ = date('now','+1 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info3 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+1
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Plymouth' and date_ = date('now','+1 day')")
	info4 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+2 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Plymouth' and date_ = date('now','+2 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info5 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+2
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Plymouth' and date_ = date('now','+2 day')")
	info6 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+3 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Plymouth' and date_ = date('now','+3 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info7 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+3
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Plymouth' and date_ = date('now','+3 day')")
	info8 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+4 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Plymouth' and date_ = date('now','+4 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info9 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+4
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Plymouth' and date_ = date('now','+4 day')")
	info10 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+5 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Plymouth' and date_ = date('now','+5 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info11 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+5
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Plymouth' and date_ = date('now','+5 day')")
	info12 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+6 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Plymouth' and date_ = date('now','+6 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info13 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+5
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Plymouth' and date_ = date('now','+6 day')")
	info14 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# CurrentSurfConditions in page header
	# For now, setting all 'current conditions' to mid-day conditions (time_ = 12pm)
	cursor = conn.cursor()
	cursor.execute("select swellsizeft, swellintervalsec, windmph, airtemp, WindDescription from surfmaster2 where date_ = date('now') and time_ = '12pm' and beach_name = 'Plymouth'")
	info15 = [dict(SwellSizeFt1=row[0], SwellIntervalSec1=row[1], WindMPH1=row[2], AirTemp1=row[3], WindDescription1=row[4]) for row in cursor.fetchall()]
	cursor.close()



	return render_template('Plymouth.html', selected='submit',info1=info1, info2=info2, info3=info3, info4=info4, info5=info5, info6=info6, info7=info7, info8=info8,  info9=info9,  info10=info10,  info11=info11,  info12=info12,  info13=info13,  info14=info14, info15=info15, graph_data=graph_data)


#--------------------------NH BEACHES--------------------------------

@app.route('/Rye')
@csrf.exempt
def Rye():
	#responsible for getting X,Y values, both lists stored as variables mylist & newl
	conn = sqlite3.connect('SurfSend.db')
	conn.row_factory = lambda cursor, row: row[0]
	c = conn.cursor()
	# valuesx = c.execute("select swellsizeft from surfmaster2 where beach_name = '2nd Beach' and date_ = '2018-11-23'").fetchall()
	values = c.execute("select distinct avg_day from surfmaster2 where beach_name ='Rye'").fetchall()

	mmm = [float(i) for i in values]

	labels = c.execute("select distinct date_ from surfmaster2").fetchall()
	mylist = []
	for l in labels:
		dates = l[5:]
		mylist.append(str(dates))
	print(mylist)
	print(mmm)

	#code responsible for graphing the pygal chart ... using data from the DB, from list objects mylist & newl
	graph = pygal.Line()
	graph.title = 'Rye Beach 7 Day Surf Forecast'
	graph.x_labels = mylist
	graph.add('Avg Wave Height',  mmm)
	graph_data = graph.render_data_uri()
	#original code, used for creating table in Nahant.html

	# getdate() table
	conn = sqlite3.connect('SurfSend.db')
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Rye' and date_ = date('now') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info1 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Rye' and date_ = date('now')")
	info2 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+1 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Rye' and date_ = date('now','+1 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info3 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+1
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Rye' and date_ = date('now','+1 day')")
	info4 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+2 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Rye' and date_ = date('now','+2 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info5 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+2
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Rye' and date_ = date('now','+2 day')")
	info6 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+3 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Rye' and date_ = date('now','+3 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info7 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+3
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Rye' and date_ = date('now','+3 day')")
	info8 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+4 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Rye' and date_ = date('now','+4 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info9 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+4
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Rye' and date_ = date('now','+4 day')")
	info10 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+5 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Rye' and date_ = date('now','+5 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info11 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+5
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Rye' and date_ = date('now','+5 day')")
	info12 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+6 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Rye' and date_ = date('now','+6 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info13 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+5
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Rye' and date_ = date('now','+6 day')")
	info14 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# CurrentSurfConditions in page header
	# For now, setting all 'current conditions' to mid-day conditions (time_ = 12pm)
	cursor = conn.cursor()
	cursor.execute("select swellsizeft, swellintervalsec, windmph, airtemp, WindDescription from surfmaster2 where date_ = date('now') and time_ = '12pm' and beach_name = 'Rye'")
	info15 = [dict(SwellSizeFt1=row[0], SwellIntervalSec1=row[1], WindMPH1=row[2], AirTemp1=row[3], WindDescription1=row[4]) for row in cursor.fetchall()]
	cursor.close()



	return render_template('Rye.html', selected='submit',info1=info1, info2=info2, info3=info3, info4=info4, info5=info5, info6=info6, info7=info7, info8=info8,  info9=info9,  info10=info10,  info11=info11,  info12=info12,  info13=info13,  info14=info14, info15=info15,  graph_data=graph_data)

@app.route('/Hampton')
@csrf.exempt
def Hampton():
	#responsible for getting X,Y values, both lists stored as variables mylist & newl
	conn = sqlite3.connect('SurfSend.db')
	conn.row_factory = lambda cursor, row: row[0]
	c = conn.cursor()
	# valuesx = c.execute("select swellsizeft from surfmaster2 where beach_name = '2nd Beach' and date_ = '2018-11-23'").fetchall()
	values = c.execute("select distinct avg_day from surfmaster2 where beach_name ='Hampton'").fetchall()

	mmm = [float(i) for i in values]

	labels = c.execute("select distinct date_ from surfmaster2").fetchall()
	mylist = []
	for l in labels:
		dates = l[5:]
		mylist.append(str(dates))
	print(mylist)
	print(mmm)

	#code responsible for graphing the pygal chart ... using data from the DB, from list objects mylist & newl
	graph = pygal.Line()
	graph.title = 'Hampton Beach 7 Day Surf Forecast'
	graph.x_labels = mylist
	graph.add('Avg Wave Height',  mmm)
	graph_data = graph.render_data_uri()
	#original code, used for creating table in Nahant.html

	# getdate() table
	conn = sqlite3.connect('SurfSend.db')
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Hampton' and date_ = date('now') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info1 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Hampton' and date_ = date('now')")
	info2 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+1 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Hampton' and date_ = date('now','+1 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info3 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+1
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Hampton' and date_ = date('now','+1 day')")
	info4 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+2 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Hampton' and date_ = date('now','+2 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info5 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+2
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Hampton' and date_ = date('now','+2 day')")
	info6 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+3 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Hampton' and date_ = date('now','+3 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info7 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+3
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Hampton' and date_ = date('now','+3 day')")
	info8 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+4 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Hampton' and date_ = date('now','+4 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info9 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+4
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Hampton' and date_ = date('now','+4 day')")
	info10 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+5 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Hampton' and date_ = date('now','+5 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info11 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+5
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Hampton' and date_ = date('now','+5 day')")
	info12 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+6 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Hampton' and date_ = date('now','+6 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info13 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+5
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Hampton' and date_ = date('now','+6 day')")
	info14 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# CurrentSurfConditions in page header
	# For now, setting all 'current conditions' to mid-day conditions (time_ = 12pm)
	cursor = conn.cursor()
	cursor.execute("select swellsizeft, swellintervalsec, windmph, airtemp, WindDescription from surfmaster2 where date_ = date('now') and time_ = '12pm' and beach_name = 'Hampton'")
	info15 = [dict(SwellSizeFt1=row[0], SwellIntervalSec1=row[1], WindMPH1=row[2], AirTemp1=row[3], WindDescription1=row[4]) for row in cursor.fetchall()]
	cursor.close()



	return render_template('Hampton.html', selected='submit',info1=info1, info2=info2, info3=info3, info4=info4, info5=info5, info6=info6, info7=info7, info8=info8,  info9=info9,  info10=info10,  info11=info11,  info12=info12,  info13=info13,  info14=info14, info15=info15,  graph_data=graph_data)


@app.route('/Seabrook')
@csrf.exempt
def Seabrook():
	#responsible for getting X,Y values, both lists stored as variables mylist & newl
	conn = sqlite3.connect('SurfSend.db')
	conn.row_factory = lambda cursor, row: row[0]
	c = conn.cursor()
	# valuesx = c.execute("select swellsizeft from surfmaster2 where beach_name = '2nd Beach' and date_ = '2018-11-23'").fetchall()
	values = c.execute("select distinct avg_day from surfmaster2 where beach_name ='Seabrook'").fetchall()

	mmm = [float(i) for i in values]

	labels = c.execute("select distinct date_ from surfmaster2").fetchall()
	mylist = []
	for l in labels:
		dates = l[5:]
		mylist.append(str(dates))
	print(mylist)
	print(mmm)

	#code responsible for graphing the pygal chart ... using data from the DB, from list objects mylist & newl
	graph = pygal.Line()
	graph.title = 'Seabrook Beach 7 Day Surf Forecast'
	graph.x_labels = mylist
	graph.add('Avg Wave Height',  mmm)
	graph_data = graph.render_data_uri()
	#original code, used for creating table in Nahant.html

	# getdate() table
	conn = sqlite3.connect('SurfSend.db')
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Seabrook' and date_ = date('now') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info1 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Seabrook' and date_ = date('now')")
	info2 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+1 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Seabrook' and date_ = date('now','+1 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info3 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+1
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Seabrook' and date_ = date('now','+1 day')")
	info4 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+2 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Seabrook' and date_ = date('now','+2 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info5 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+2
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Seabrook' and date_ = date('now','+2 day')")
	info6 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+3 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Seabrook' and date_ = date('now','+3 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info7 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+3
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Seabrook' and date_ = date('now','+3 day')")
	info8 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+4 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Seabrook' and date_ = date('now','+4 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info9 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+4
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Seabrook' and date_ = date('now','+4 day')")
	info10 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+5 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Seabrook' and date_ = date('now','+5 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info11 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+5
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Seabrook' and date_ = date('now','+5 day')")
	info12 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+6 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='Seabrook' and date_ = date('now','+6 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info13 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+5
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='Seabrook' and date_ = date('now','+6 day')")
	info14 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# CurrentSurfConditions in page header
	# For now, setting all 'current conditions' to mid-day conditions (time_ = 12pm)
	cursor = conn.cursor()
	cursor.execute("select swellsizeft, swellintervalsec, windmph, airtemp, WindDescription from surfmaster2 where date_ = date('now') and time_ = '12pm' and beach_name = 'Seabrook'")
	info15 = [dict(SwellSizeFt1=row[0], SwellIntervalSec1=row[1], WindMPH1=row[2], AirTemp1=row[3], WindDescription1=row[4]) for row in cursor.fetchall()]
	cursor.close()



	return render_template('Seabrook.html', selected='submit',info1=info1, info2=info2, info3=info3, info4=info4, info5=info5, info6=info6, info7=info7, info8=info8,  info9=info9,  info10=info10,  info11=info11,  info12=info12,  info13=info13,  info14=info14, info15=info15,  graph_data=graph_data)

@app.route('/NHSeacoast')
@csrf.exempt
def NHSeacoast():
	#responsible for getting X,Y values, both lists stored as variables mylist & newl
	conn = sqlite3.connect('SurfSend.db')
	conn.row_factory = lambda cursor, row: row[0]
	c = conn.cursor()
	# valuesx = c.execute("select swellsizeft from surfmaster2 where beach_name = '2nd Beach' and date_ = '2018-11-23'").fetchall()
	values = c.execute("select distinct avg_day from surfmaster2 where beach_name ='NH Seacoast'").fetchall()

	mmm = [float(i) for i in values]

	labels = c.execute("select distinct date_ from surfmaster2").fetchall()
	mylist = []
	for l in labels:
		dates = l[5:]
		mylist.append(str(dates))
	print(mylist)
	print(mmm)

	#code responsible for graphing the pygal chart ... using data from the DB, from list objects mylist & newl
	graph = pygal.Line()
	graph.title = 'NHSeacoast Beach 7 Day Surf Forecast'
	graph.x_labels = mylist
	graph.add('Avg Wave Height',  mmm)
	graph_data = graph.render_data_uri()
	#original code, used for creating table in Nahant.html

	# getdate() table
	conn = sqlite3.connect('SurfSend.db')
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='NH Seacoast' and date_ = date('now') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info1 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='NH Seacoast' and date_ = date('now')")
	info2 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+1 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='NH Seacoast' and date_ = date('now','+1 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info3 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+1
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='NH Seacoast' and date_ = date('now','+1 day')")
	info4 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+2 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='NH Seacoast' and date_ = date('now','+2 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info5 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+2
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='NH Seacoast' and date_ = date('now','+2 day')")
	info6 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# getdate()+3 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='NH Seacoast' and date_ = date('now','+3 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info7 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+3
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='NH Seacoast' and date_ = date('now','+3 day')")
	info8 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+4 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='NH Seacoast' and date_ = date('now','+4 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info9 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+4
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='NH Seacoast' and date_ = date('now','+4 day')")
	info10 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+5 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='NH Seacoast' and date_ = date('now','+5 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info11 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+5
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='NH Seacoast' and date_ = date('now','+5 day')")
	info12 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()


	# getdate()+6 table
	cursor = conn.cursor()
	cursor.execute("select SwellSizeFt, SwellIntervalSec, WindMPH, WindDescription, AirTemp, beach_name, date_, time_, state from SurfMaster2 where beach_name ='NH Seacoast' and date_ = date('now','+6 day') order by SurfMaster2.beach_name ASC, SurfMaster2.date_ ASC")
	info13 = [dict(SwellSize=row[0], SwellInterval=row[1], WindSpeed=row[2], WindDescription=row[3], AirTemperature=row[4], Beach=row[5], Day=row[6], Tiempo=row[7], St8=row[8]) for row in cursor.fetchall()]
	cursor.close()

	# distinct day for getdate()+5
	cursor = conn.cursor()
	cursor.execute("select distinct date_ from SurfMaster2 where beach_name ='NH Seacoast' and date_ = date('now','+6 day')")
	info14 = [dict(DayDistinct=row[0]) for row in cursor.fetchall()]
	cursor.close()

	# CurrentSurfConditions in page header
	# For now, setting all 'current conditions' to mid-day conditions (time_ = 12pm)
	cursor = conn.cursor()
	cursor.execute("select swellsizeft, swellintervalsec, windmph, airtemp, WindDescription from surfmaster2 where date_ = date('now') and time_ = '12pm' and beach_name = 'NHSeacoast'")
	info15 = [dict(SwellSizeFt1=row[0], SwellIntervalSec1=row[1], WindMPH1=row[2], AirTemp1=row[3], WindDescription1=row[4]) for row in cursor.fetchall()]
	cursor.close()


	return render_template('NHSeacoast.html', selected='submit',info1=info1, info2=info2, info3=info3, info4=info4, info5=info5, info6=info6, info7=info7, info8=info8,  info9=info9,  info10=info10,  info11=info11,  info12=info12,  info13=info13,  info14=info14,  info15=info15, graph_data=graph_data)


#---------------------------------- END BEACHES ----------------------------------#

@app.route('/scrapelist2', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def scrapelist2():
	if request.method == 'POST':
		global feed
		conn = sqlite3.connect('SurfSend.db')
		cursor = conn.cursor()
		posts = [dict(DJname=row[0]) for row in cursor.fetchall()]
		DJname = request.form['Producername']
		DJName2 = DJname.split('- ', 1)[-1]
		Email = request.form['Email']
		CellPhone = request.form['CellPhone']
		Delivery = request.form['options']
		usrn = current_user.username
		cursor.execute("INSERT INTO ArtistMonitor VALUES (NULL,?,?,?,?,?)", (DJName2,usrn,Email,CellPhone,Delivery))
		conn.commit()
		cursor.close()
		conn.close()
		artists.append(request.form['Producername'])
	usrn2 = current_user.username
	g.db = connect_db()
	cur = g.db.execute("select DJName, email, cellphone from ArtistMonitor where usn = (?)", (usrn2,))
	cur2 = g.db.execute('select * from Tracks where artist in (select DJname from ArtistMonitor)')
	pull = [dict(DJname=row[0], email=row[1], cellphone=row[2]) for row in cur.fetchall()]
	watch = [dict(Artist=row[0], Song=row[1], Websource=row[2], Genre=row[3]) for row in cur2.fetchall()]
	g.db.close()
	return render_template('scrapelist2.html', selected='submit', pull=pull, watch=watch, usrn2=usrn2)



@app.route('/delete_artist/<DJName>', methods=['POST'])
@csrf.exempt
def delete_artist(DJName):
	conn = sqlite3.connect('Surfsend.db')
	cursor = conn.cursor()
	del1 = [dict(id=row[0], DJName=row[1]) for row in cursor.fetchall()]
#	DJName1 = request.args.get('DJName')
	cursor.execute("DELETE FROM ArtistMonitor WHERE DJName = ?", (DJName,))
	conn.commit()
	cursor.close()
	conn.close()
	flash('Beach Deleted')
	return redirect(url_for('scrapelist2', del1=del1))



#not orig
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('scrapelist2'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('scrapelist2'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)




@app.route('/hello')
@login_required
def hello():
	conn = sqlite3.connect('Surfsend.db')
	cursor = conn.cursor()
	cur = cursor.execute('select Artist, Song, Label, Price from BeatPortTechHouse')
	info = [dict(Artist=row[0], Song=row[1], Label=row[2], Price=row[3]) for row in cur.fetchall()]
	cursor.close()
	return render_template('hello.html', info=info)



@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()

	if form.validate_on_submit():
		hashed_password = generate_password_hash(form.password.data, method='sha256')
		new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(new_user)
		db.session.commit()


		flash(Markup('User Created! <a href="/login" class="alert-link">Sign In Now &#8594;</a>'))

		#mskhere


		#Send A Welcome Email Upon Registering
		email_list = form.email.data

		user_name = form.username.data
		message_all = 'Hi ' + user_name + '!' + '\n' + 'Thanks for registering for SurfSend!' + '\n' + 'If you have any questions or things you would like to report, please email surfsendhelp@gmail.com.' + '\n' + '\n' + 'Warm Regards,' + '\n' + '	-Team SurfSend'

		msg = MIMEMultipart()
		msg['From'] = 'mkramer265@gmail.com'
		msg['To'] = 'mkramer789@gmail.com'
		msg['Subject'] = 'Thanks for Registering!'
		# message = j + 'ft' ' @ ' + k + ' on ' + l
		# print(message)
		msg.attach(MIMEText(message_all))

		mailserver = smtplib.SMTP('smtp.gmail.com',587)
		# identify ourselves to smtp gmail client
		mailserver.ehlo()
		# secure our email with tls encryption
		mailserver.starttls()
		# re-identify ourselves as an encrypted connection
		mailserver.ehlo()
		mailserver.login('mkramer265@gmail.com', 'Celtics123')

		mailserver.sendmail('mkramer265@gmail.com',email_list,msg.as_string())

		mailserver.quit()
		#return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

	return render_template('register.html', form=form)



@app.route('/sendr', methods=['GET', 'POST'])
@csrf.exempt
def sendr():
	if request.method == 'POST':
		global feed
		conn = sqlite3.connect('SurfSend.db')
		cursor = conn.cursor()
		posts = [dict(URL_sc=row[0], Time_sc=row[1] ) for row in cursor.fetchall()]
		# FirstName
		FN = request.form['FirstName']
		# Email
		EM = request.form['Email']
		# Radio Button Value
		Radio_sc = request.form['options']
		cursor.execute("INSERT INTO Sendr_Usr VALUES (?,?,?)", (EM,FN,Radio_sc,))
		conn.commit()
		cursor.close()
		conn.close()


		scl_sc = '#t='
		appendx_sc = "".join((FN, scl_sc, EM))

		return render_template('sendr.html', FN=FN, EM=EM, scl_sc=scl_sc, appendx_sc=appendx_sc)
	return render_template('sendr.html')


@app.route('/exit', methods=['GET', 'POST'])
@csrf.exempt
def exit():
	if request.method == 'POST':
		global feed
		conn = sqlite3.connect('SurfSend.db')
		cursor = conn.cursor()
		posts = [dict(URL_sc=row[0], Time_sc=row[1] ) for row in cursor.fetchall()]
		# Email
		EM = request.form['EmailX']
		cursor.execute("DELETE FROM Sendr_Usr WHERE email = (?)", (EM,))
		conn.commit()
		cursor.close()
		conn.close()

		return render_template('exit.html', EM=EM)
	return render_template('exit.html')




def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to login first.')
			return redirect(url_for('login'))
	return wrap


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('welcome'))


if __name__ == '__main__':
    app.run(debug=True)