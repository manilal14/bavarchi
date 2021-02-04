from application import app
from flask import render_template,request,session,url_for,redirect, flash
from .models import User, getAllFoodItems

@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
	return render_template('homepage.html')


@app.route('/login' , methods = ['GET', 'POST'])
def login():

	if request.method == 'POST' and 'uname' in request.form and 'password' in request.form:
		if request.form['uname'] == 'manager' and request.form['password']=='manager':
			#have to remove it
			session['loggedin'] = 'manager'
			return render_template('managerpage.html')
		else:
			email 	 = request.form['uname']
			password = request.form['password']

			if User().verify_password(email, password):
				session['loggedin'] = email
				flash('Welcome '+email, category='success')
				all_items = getAllFoodItems()
				return render_template("menu_list.html", foods=all_items)
				
			else:
				flash('Invalid User', category='danger')
			
	return render_template('login.html')


@app.route('/register' , methods = ['GET', 'POST'] )
def register():

	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		name 	 = request.form['username']
		email 	 = request.form['email']
		password = request.form['password']

		res = User().registerUser(name, email, password)

		if res:
			session['loggedin'] = email
			flash('Welcome '+email, category='success')
			all_items = getAllFoodItems()
			return render_template("menu_list.html", foods=all_items)
		else:
			flash('Email alreeady registered', category='danger')

	return render_template('register.html')


@app.route('/add_new_dish' , methods = ['GET', 'POST'] )
def add_new_dish():
	print(request.form['item'])
	print(request.form['price'])
	return render_template('managerpage.html',msg='Dish added successfully')

@app.route('/logout' , methods = ['GET', 'POST'] )
def logout():
	session.pop('loggedin', None)
	return render_template('homepage.html',msg='Logged Out Successfully')


@app.route('/orderplaced' , methods = ['GET', 'POST'] )
def orderplaced():
	return render_template('menu_list.html',msg='Order Placed Successfully')
