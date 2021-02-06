from application import app
from flask import render_template,request,session,url_for,redirect, flash
from .models import User, getAllFoodItems, add_dish, delete_dish

@app.route('/')
@app.route('/home')
def home():
	return render_template('homepage.html')
@app.route('/index')



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

@app.route('/manager' , methods = ['GET', 'POST'])
def manager():
	session['loggedin'] = 'manager'
	return render_template('managerpage.html')
	return True
	


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
	food_id 	 = request.form['food_id']
	item	 = request.form['item']
	price = request.form['price']
	image	 = request.form['image']
	desc 	 = request.form['desc']
	
	#msg2=getAllFoodItems()
	if add_dish(food_id,item,price,image,desc):
		return render_template('new_dish.html',msg='Dish added successfully')
	elif not add_dish(food_id,item,price,image,desc):
		return render_template('new_dish.html',msg2='Dish already present')
		

@app.route('/logout' , methods = ['GET', 'POST'] )
def logout():
	session.pop('loggedin', None)
	return render_template('homepage.html',msg='Logged Out Successfully')


@app.route('/orderplaced' , methods = ['GET', 'POST'] )
def orderplaced():
	return render_template('menu_list.html',msg='Order Placed Successfully')

@app.route('/new_dish' , methods = ['GET', 'POST'] )
def new_dish():
	return render_template('new_dish.html')

@app.route('/get_all_dish' , methods = ['GET', 'POST'] )
def get_all_dish():
	all_items = getAllFoodItems()
	return render_template('get_all_dish.html', foods=all_items)

@app.route('/remove_dish' , methods = ['GET', 'POST'] )
def remove_dish():
	item	 = request.form['item']
	food_id 	 = request.form['food_id']
	
	if delete_dish(food_id,item):
		all_items = getAllFoodItems()
		return render_template('get_all_dish.html',msg='Dish removed successfully', foods=all_items)
	elif delete_dish(food_id,item):
		all_items = getAllFoodItems()
		return render_template('get_all_dish.html',msg2='Dish not present', foods=all_items)

