from application import app
from flask import render_template,request,session,url_for,redirect


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
	return render_template('login.html')

@app.route('/login' , methods = ['GET', 'POST'])
def login():

	if request.method == 'POST' and 'uname' in request.form and 'password' in request.form:
		if request.form['uname'] == 'manager' and request.form['password']=='manager':

			session['loggedin'] = 'manager'
			return render_template('managerpage.html')
		else:
			items = {}
			return render_template('menu_list.html',items= items)
			#else we need to here match with the content in the datatbase and then proceed

		#code to validate the user and redirect to specific page on correct macth
		#print('Inside the verification on login credentialas with values ',request.form['uname'],request.form['password'])
	return render_template('login.html')


@app.route('/register' , methods = ['GET', 'POST'] )
def register():
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		#code to push the entered data in to the neo4j database
		return render_template('login.html')
		print(request.form['username'])

	return render_template('register.html')


@app.route('/add_new_dish' , methods = ['GET', 'POST'] )
def add_new_dish():
	print(request.form['item'])
	print(request.form['price'])
	return render_template('managerpage.html',msg='Dish added successfully')

@app.route('/logout' , methods = ['GET', 'POST'] )
def logout():
	session.pop('loggedin', None)
	return render_template('login.html',msg='Logged Out Successfully')


@app.route('/orderplaced' , methods = ['GET', 'POST'] )
def orderplaced():
	return render_template('menu_list.html',msg='Order Placed Successfully')
