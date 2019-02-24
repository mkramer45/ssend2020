import flask
from flask import *
from functools import wraps
import sqlite3
from flask_bootstrap import Bootstrap
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm, CsrfProtect
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pygal
from pygal.style import BlueStyle



artists = ['Solomun', 'Dubfire']

DATABASE = 'SurfSend.db'

app = Flask(__name__)
app.secret_key = 'my precious'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/mkramer265/Jan13_SurfSend_AllGood\SurfSend.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
app.config.from_object(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
csrf = CsrfProtect(app)

class LoginForm(FlaskForm):
	username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
	remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
	email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
	username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(15), unique=True)
	email = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(80))


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
	print(mylist)
	print(mmm)

	#code responsible for graphing the pygal chart ... using data from the DB, from list objects mylist & newl
	graph = pygal.Line(fill=True, interpolate='cubic', style=BlueStyle)
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

	return render_template('Nahant.html', selected='submit',info1=info1, info2=info2, info3=info3, info4=info4, info5=info5, info6=info6, info7=info7, info8=info8,  info9=info9,  info10=info10,  info11=info11,  info12=info12,  info13=info13,  info14=info14, info15=info15,  graph_data=graph_data)


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




@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user:
			if check_password_hash(user.password, form.password.data):
				login_user(user, remember=form.remember.data)
				return redirect(url_for('scrapelist2'))

		flash('Invalid Username/Password')
		#return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

	return render_template('login.html', form=form)




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

		flash('User Created')
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