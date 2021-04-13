This repository is a Flask based Web application.

Name : Bavarchi Restuarant

Technology : Flask (1.1.2) and Neo4j (py2neo = 2021.0.0)

Description : A website where users can order dishes from the menu of the "Bavarchi restuarant"

OS supported : Windows 10 and Ubuntu

Contributors : Manilal Kasera (https://github.com/manilal14), Monica Gaddipati (https://github.com/MonicaGaddipati123), Rishabh Sharma (https://github.com/rishabhsharma03), Shazeb Fahmi (https://github.com/shazebfahmi)
               
Functionalities : 1. Manager and Users are 2 types of "login", to access the website.
                  2. Users can add multiple food items from the menu list provided by the restuarant manager into their cart and then can finally place order.
                  3. Managers recieve the order when a users places an order. Manager also has functionality to mark the order as delivered once the order is delivered. 
                  4. Manager can add/remove the dishes available at the restaurant as required.
                  5. New users can register themselves from clicking the register button.
                  6. Manager can directly login without registering, as they have special access.

How to run? :   1. Download Neo4j desktop application from the official website "https://neo4j.com/download/" and open it.
                2. Create New project -> select the created project -> Add -> Local DBMS -> Username='neo4j' -> password='test' -> Start
                3. Now the database is up and running. We now start the Flask web application.
                4. Clone the repository by going to command promt and run : $git clone https://github.com/shazebfahmi/bavarchi_personal.git
                5. Activate the virtual environment : $venv\Scripts\activate
                6. Download the required modules : $pip install -r requirement.txt
                7. Start the flask server : $ flask run
                8. Open any web browser and goto : 127.0.0.1:5000 
                9. New users need to register prior to logging in.
                10. Manager access can be gained by entering these credentials : Email:manager , Password:manager
                11. Initially there are no food items listed in the website for the users. The manager needs to login and add them.
                11. Register a few users and order a few dishes and observe the changes visually in the graph database as mentioned in point 3 below
                      

Technicalities : 1. The Database used is Neo4j, since it is a graph database, it allows for faster query execution when compared to the traditional databases.
                 2. It doesn't need to set any primary key/ foreign key constraints since the nodes are connected with each other as per relationship defined.
                 3. The node graph can be visualised in an interactive way from the "database browser" which can be started from "Neo4j desktop application".(After starting a database click on "Open" and after browser opens, type "match (n) return (n)" and click run button)
                 4. We can observe the 'User' nodes and 'Order' nodes and the relationship between them visually.
            
            
            
