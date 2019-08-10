#DEPENDENCIES
from flask import Flask, render_template, url_for, request, redirect, session, logging, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#DATABASE SHIT
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#USER MODEL
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(80))
	last_name = db.Column(db.String(80))
	password = db.Column(db.String(80))
	email_address = db.Column(db.String(80), unique=True)
	

	def __init__(self, first_name, last_name, email_address, password):
		self.email_address = email_address
		self.password = password
		self.first_name = first_name
		self.last_name = last_name

#TEAM MODEL
class Team(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(80))
	last_name = db.Column(db.String(80))
	email_address = db.Column(db.String(80), unique=True)
	team_leader = db.Column(db.String(80), unique=True)
	url = db.Column(db.String(80), unique=True)
	

	def __init__(self, first_name, last_name, email_address, password):
		self.first_name = first_name
		self.last_name = last_name
		self.email_address = email_address
		self.team_leader = team_leader
		self.url = url
		

#SERVER ROUTES
@app.route("/", methods=['GET', 'POST'])
def landing():
	return render_template('landing.html')

@app.route("/register", methods=['GET', 'POST']) 
def register():

	if request.method == 'POST':
		data = User.query.filter_by(email_address=request.form['email_address']).first()
		if data is not None:
			return "user exists"
		else:
			new_user = User(email_address=request.form['email_address'], password=request.form['password'],  first_name=request.form['first_name'], last_name=request.form['last_name'])
			db.session.add(new_user)
			db.session.commit()
			session['logged_in'] = True
			return redirect(url_for('home'))
	else:
		return render_template('register.html')  

@app.route("/login", methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	else:
		email_address = request.form['email_address']
		password = request.form['password']

	data = User.query.filter_by(email_address = email_address, password = password).first()

	if data is not None:
		session['logged_in'] = True
		session['email_address'] = email_address 
		return redirect(url_for('home'))
	else:
		return 'User Does Not Exist'  

@app.route("/home", methods=['GET', 'POST'])
def home():
	return render_template('home.html')

@app.route("/analytics", methods=['GET', 'POST'])
def analytics():
	return render_template('analytics.html')

@app.route("/settings", methods=['GET', 'POST'])
def settings():
	return render_template('settings.html')

    
if __name__ == "__main__":
	db.create_all()
	app.secret_key = '1234'
	app.run(debug=True)