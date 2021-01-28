from application import app
from flask import render_template,request


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
	return render_template('login.html')

@app.route('/login' , methods = ['GET', 'POST'])
def login():

	if request.method == 'POST' and 'uname' in request.form and 'password' in request.form:
		pass
		#code to validate the user and redirect to specific page on correct macth
		#print('Inside the verification on login credentialas with values ',request.form['uname'],request.form['password'])
	return render_template('login.html')


@app.route('/register' , methods = ['GET', 'POST'] )
def register():
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		#code to push the entered data in to the neo4j database
		return render_template('login.html')

	return render_template('register.html')
