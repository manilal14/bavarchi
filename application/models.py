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
    query="MATCH (u:User) where u.email = '"+username+"' Match (u:User)-[o:Ordered]->(o1:Order)-[d:Dishes]->(f:Food_Items) where f.food_id="+food_id+" and f.name='"+item+"' detach delete d"
    return graph.run(query)

def find_food(fname):
    return matcher.match('Food_Items',name=fname).first()
    
    	

class User:

    def find_food_items(self,id,name):
        print("food_id ="+str(id))
        #not working by id
        #return matcher.match('Food_Items', food_id=id).first()
        return matcher.match('Food_Items', name=name).first()

    def find_order(self,uname):
        return matcher.match('Order',name=uname).first()
    def check_status(self,status):
        return matcher.match('Order',order_status=status).first()
       
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

    def placeorder(self,username):
        q = '''MATCH (n:User) where n.email = '{}'
        match (u:User)-[:Ordered]->(o1:Order)-[d:Dishes]->(f:Food_Items) set o1.order_status="ordered"
        return f.food_id AS food_id, f.name As name,
        f.desc AS description, f.price AS price'''.format(username)
        graph.run(q)
        return True

    def orderhistory(self,username):
        q = '''MATCH (n:User) where n.email = '{}'
        Match (u:User)-[:Ordered]->(o1:Order)-[d:Dishes]->(f:Food_Items) where o1.order_status="ordered"
        return o1.name AS username, 
        o1.order_item As name, o1.price AS price, o1.order_status AS description limit 1
        '''.format(username)
        return graph.run(q).data()
    
    def getUserCartOrder(self, username):
        q = '''MATCH (n:User) where n.email = '{}'
        match (u:User)-[:Ordered]->(o1:Order)-[d:Dishes]->(f:Food_Items) where o1.order_status="ordering"
        return f.food_id AS food_id, f.name As name,
        f.desc AS description, f.price AS price'''.format(username)
        return graph.run(q)

    def add_to_cart(self, username, food_id, item,price):
        user = self.find_user(username)

        if self.find_order(username) and self.check_status("ordering"):
            order=self.find_order(username) and self.check_status("ordering")
            q = '''MATCH (n:User) where n.email = '{0}'
            match (u:User)-[:Ordered]->(o1:Order)-[d:Dishes]->(f:Food_Items) where o1.order_status="ordering" set o1.order_item=o1.order_item+", "+'{1}' 
            return f.price AS price'''.format(username,item)
            pr=graph.run(q).data()
            pp=str(int(pr[0]['price'])+int(price))
            q1 = "MATCH (n:User) where n.email = '"+username+"' match (u:User)-[:Ordered]->(o1:Order)-[d:Dishes]->(f:Food_Items) where o1.order_status='ordering' set o1.price="+pp+" return f.food_id AS food_id, f.name As name,f.desc AS description, f.price AS price"
            graph.run(q1)
            print(order)
        else:
            p=int(price)
            order=Node('Order', name=username,order_status="ordering",order_item=item,price=p)
            graph.create(order)
        

        food=find_food(item)
        rel1=Relationship(user,'Ordered',order)
        graph.create(rel1)
        rel2=Relationship(order,'Dishes',food)
        graph.create(rel2)


        return True

    def getOrder_man(self):

        q = '''Match (u:User)-[:Ordered]->(o1:Order)-[d:Dishes]->(f:Food_Items) where o1.order_status="ordered"
        return o1.name AS username, 
        o1.order_item As name, o1.price AS price limit 1
        '''
        #query="MATCH (user:User)-[:ORDERED]->(order:Order) - [:dishes]->(food:Food_Items) RETURN food.name AS name,food.price AS price,user.email AS username,order.id AS id,order.date AS date,order.timestamp AS time, food.desc AS description"
        return graph.run(q).data()

