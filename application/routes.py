from application import app
from flask import render_template,request,session,url_for,redirect, flash
from .models import User, getAllFoodItems, add_dish, delete_dish, delete_item, accept_order_man, deliver_order_man,find_foods

@app.route('/')
def home():
	if isLoggedIn():
		all_items = getAllFoodItems()
		user = session.get('loggedin')
		return render_template("menu_list.html", user=user, foods=all_items)
	return render_template("homepage.html")

@app.route('/login' , methods = ['GET', 'POST'])
def login():

	if isLoggedIn():
		all_items = getAllFoodItems()
		user = session.get('loggedin')
		if user=='manager':
			return render_template('managerpage.html')

		return render_template("menu_list.html", user=user, foods=all_items)
	
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
				return render_template("menu_list.html", user=email,foods=all_items)

			else:
				flash('Invalid User', category='danger')

	return render_template('login.html')

@app.route('/register' , methods = ['GET', 'POST'] )
def register():
	
	if isLoggedIn():
		all_items = getAllFoodItems()
		user = session.get('loggedin')
		if user=='manager':
			return render_template('managerpage.html')

	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		name 	 = request.form['username']
		email 	 = request.form['email']
		password = request.form['password']

		res = User().registerUser(name, email, password)

		if res:
			session['loggedin'] = email
			if email=='manager':
				return render_template('managerpage.html')
			flash('Welcome '+email, category='success')
			all_items = getAllFoodItems()
			return render_template("menu_list.html",user=email,foods=all_items)
		else:
			flash('Email alreeady registered', category='danger')

	return render_template('register.html')


@app.route('/logout' , methods = ['GET', 'POST'] )
def logout():
	session.pop('loggedin', None)
	return render_template('homepage.html',msg='Logged Out Successfully')


#add to cart
@app.route('/addToCart' , methods = ['POST'] )
def addToCart():
	username 	= session.get('loggedin')
	food_id	 	= request.form['food_id']
	
	food_name	= request.form['item']
	price	= request.form['price']

	if User().add_to_cart(username, food_id, food_name,price):
		o1 = User().getUserCartOrder(username)
		return render_template('display.html',msg='Order Placed Successfully',o1=o1)
	else:
		#occur only if db crashed but have to handle this
		print("Cannot added to cart")

@app.route('/remove_order' , methods = ['GET', 'POST'] )
def remove_order():
	username 	= session.get('loggedin')
	item	 = request.form['item']
	print(item)
	food_id	 = request.form['food_id']
	price = request.form['price']

	if delete_item(username,food_id,item,price):
		
		o1 = User().getUserCartOrder(username)
		return render_template('display.html',msg='Dish removed successfully',o1=o1)
	elif delete_item(username,food_id,item,price):
		
		return render_template('display.html',msg2='Dish not present')

@app.route('/place_order' , methods = ['GET', 'POST'] )
def place_order():
	username 	= session.get('loggedin')
	if User().placeorder(username):
		all_items = getAllFoodItems()
		return render_template("menu_list.html", foods=all_items)

@app.route('/order_history' , methods = ['GET', 'POST'] )
def order_history():
	username 	= session.get('loggedin')
	o1 = User().orderhistory(username)
	print("hiiiiiii")
	print(o1)
	return render_template("order_history.html", o1=o1)


@app.route('/menu_list' , methods = ['GET', 'POST'] )
def menu_list():

	user = session.get('loggedin')
	if user=='manager':
			return render_template('managerpage.html')
	
	all_items = getAllFoodItems()
	return render_template("menu_list.html", foods=all_items)


@app.route('/myCart')
def myCart():
	if not isLoggedIn():
		return render_template('homepage.html',msg='Logged Out Successfully')
	
	username = session.get('loggedin')
	o1 = User().getUserCartOrder(username)
	return render_template('display.html',msg='Order Placed Successfully',o1=o1)

@app.route('/search',methods=['GET','POST'])
def search():
	item = request.form['searchitem']
	print(item)
	o1=find_foods(item)
	foods=o1
	print(foods)
	 
	return render_template("menu_list.html",foods=o1)
	

#--------------------------Helper functions ------------------------------------

def isLoggedIn():
	user = session.get('loggedin')
	if user == None:
		print("user is none")
		return False
	print("user is "+ user)
	return True




#--------------------------Related to Manager ------------------------------------

@app.route('/manager' , methods = ['GET', 'POST'])
def manager():
	session['loggedin'] = 'manager'
	return render_template('managerpage.html')

@app.route('/add_new_dish' , methods = ['GET', 'POST'] )
def add_new_dish():
	food_id 	 = request.form['food_id']
	item	 = request.form['item']
	price = request.form['price']
	image	 = request.form['image']
	desc 	 = request.form['desc']

	if add_dish(food_id,item,price,image,desc):
		return render_template('new_dish.html',msg='Dish added successfully')
	elif not add_dish(food_id,item,price,image,desc):
		return render_template('new_dish.html',msg2='Dish already present')


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
	food_id	 = request.form['food_id']

	if delete_dish(food_id,item):
		all_items = getAllFoodItems()
		return render_template('get_all_dish.html',msg='Dish removed successfully', foods=all_items)
	elif delete_dish(food_id,item):
		all_items = getAllFoodItems()
		return render_template('get_all_dish.html',msg2='Dish not present', foods=all_items)



@app.route('/display_order' , methods = ['GET', 'POST'] )
def display_order():
	o1= User().getOrder_man()
	return render_template('display_order.html',o1=o1)

@app.route('/accept_order' , methods = ['GET', 'POST'] )
def accept_order():
	username	 = request.form['username']
	price	 = request.form['price']
	item=request.form['item']
	if accept_order_man(username,price,item):
		o1= User().getOrder_man()
		return render_template('display_order.html',o1=o1)

@app.route('/deliver_order' , methods = ['GET', 'POST'] )
def deliver_order():
	o1=deliver_order_man()
	return render_template('deliver_order.html',o1=o1)