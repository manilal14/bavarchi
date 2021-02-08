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
    print("111111111")
    if not find_food(item):
        print("2222222")
        return False

    query = "Match(f:Food_Items) where f.food_id="+food_id+" and f.name='"+item+"' delete f "
    graph.run(query)
    return True 


class User:

    def find_user(self, ema):
        return matcher.match('User',email=ema).first()

    def find(self,uname):
        return matcher.match('User',username=uname).first()

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

    def add_order(self,username,item,price,food_id):
        user=self.find(username)
        print(user)
        print(item)
        order=Node('Order',name=item,price=price,food_id=food_id)
        food=find_food(item)
        rel1=Relationship(user,'ORDERED',order)
        graph.create(rel1)
        rel2=Relationship(order,'dishes',food)
        graph.create(rel2)
    def getOrder(self,username):
        query='''MATCH (user:User)-[:ORDERED]->(order:Order)
        
        RETURN order.name AS name,order.price AS price,order.food_id AS food_id,order.id AS id,order.date AS date,order.timestamp AS time'''
        return graph.run(query).data()