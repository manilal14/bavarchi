from py2neo import Graph, Node, Relationship
from py2neo.matching import *

url = 'http://localhost:7474'
username = "neo4j"
password = "test"

graph = Graph(url, auth = (username, password))
matcher = NodeMatcher(graph)

def getAllFoodItems():
    query = '''
    Match(f:Food_Items)
    RETURN f.food_id AS food_id, f.name AS name,
    f.desc AS desc, f.price AS price, f.image_path AS image_path
    '''
    return graph.run(query).data()

def find_food(fname):
    return matcher.match('Food_Items',name=fname).first()

def add_dish(food_id, item, price, image, desc):
    if find_food(item):
        return False

    food = Node('Food_Items', name=item , food_id=int(food_id) , image_path=image , price=int(price) , desc=desc)
    graph.create(food)
    return True

def delete_dish(food_id,item):
    #print("111111111")
    if not find_food(item):
        #print("2222222")
        return False

    query = "Match(f:Food_Items) where f.food_id="+food_id+" and f.name='"+item+"' delete f "
    graph.run(query)
    return True

def delete_item(username,food_id,item):
    print(food_id,username,item)
    if not find_food(item):
        return False
    query="MATCH (n:User) where n.email = '"+username+"' Match (n)-[o:Ordered]->(f:Food_Items) where f.food_id="+food_id+" and f.name='"+item+"' detach delete o"
    return graph.run(query)
    
    	

class User:

    def find_food_items(self,id,name):
        print("food_id ="+str(id))
        #not working by id
        #return matcher.match('Food_Items', food_id=id).first()
        return matcher.match('Food_Items', name=name).first()
       
    def find_user(self, ema):
        return matcher.match('User',email=ema).first()

    def registerUser(self, name, email, password):
        if self.find_user(email):
            return False

        user = Node('User', name=name, email=email, password=password)
        graph.create(user)
        return True


    def verify_password(self, email, password):
        user = self.find_user(email)
        if user:
            return user['password'] == password
        return False
    
    def getUserCartOrder(self, username):
        q = '''MATCH (n:User) where n.email = '{}'
        match (n)-[:Ordered]->(f:Food_Items)
        return f.food_id AS food_id, f.name As name,
        f.desc AS description, f.price AS price'''.format(username)
        return graph.run(q)

    def add_to_cart(self, username, food_id, food_name):
        user = self.find_user(username)
        food_item = self.find_food_items(food_id, food_name)
        graph.create(Relationship(user,"Ordered", food_item))
        return True

    def getOrder_man(self):

        q = '''Match (u:User)-[:Ordered]->(f:Food_Items)
        return u.email AS username,f.food_id AS food_id, 
        f.name As name, f.desc AS description, f.price AS price
        '''
        #query="MATCH (user:User)-[:ORDERED]->(order:Order) - [:dishes]->(food:Food_Items) RETURN food.name AS name,food.price AS price,user.email AS username,order.id AS id,order.date AS date,order.timestamp AS time, food.desc AS description"
        return graph.run(q).data()

