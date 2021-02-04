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


class User:

    def find_user(self, ema):
        return matcher.match('User',email=ema).first()

    def registerUser(self, name, email, password):
        if self.find_user(email):
            return False

        user = Node('User', name=name, email=email, password=password)
        graph.create(user)
        return True

    def find_user(self, ema):
        return matcher.match('User',email=ema).first()


    def verify_password(self, email, password):
        user = self.find_user(email)
        if user:
            return user['password'] == password
        return False
