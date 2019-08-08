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
	email_address = db.Column(db.String(80), unique=True)
	password = db.Column(db.String(80))

	def __init__(self, email_address, password):
		self.email_address = email_address
		self.password = password


#SERVER ROUTES
@app.route("/", methods=['GET', 'POST'])
def landing():
    return render_template('landing.html')


@app.route('/home', methods=['GET', 'POST'])
def home():
	if request.method == 'GET':
		return "Hello World"


@app.route("/register", methods=['GET', 'POST']) 
def register():

	if request.method == 'POST':
		data = User.query.filter_by(email_address=request.form['email_address']).first()
		if data is not None:
			return "user exists"
		else:
			new_user = User(email_address=request.form['email_address'], password=request.form['password'])
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



if __name__ == "__main__":
	db.create_all()
	app.secret_key = '123'
	app.run(debug=True)