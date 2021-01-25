from application import app
from flask import render_template,request


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/login')
def login():
	return render_template('login.html')


@app.route('/verify_login', methods = ['GET', 'POST'])
def verify_login():
	d = {1:'Hotel',2:'Delivery person',3:'Customer'}
	return "<h1> Welcome {} to Swiggy ".format(d[int(request.form['but']) ])
