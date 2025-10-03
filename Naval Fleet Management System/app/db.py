import mysql.connector as connector
from mysql.connector import Error
from .menus.crew import Crew
from .menus.ship import Ship
from .menus.mission import Mission
from .menus.documents import Document
from .menus.inventory import Inventory
from .menus.base import Base
from .menus.route import Route

class DatabaseConnectionError(Exception): pass

class DB():
    def __init__(self, host = '127.0.0.1', password = 'root'):
        self.host = host
        self.user = "root"
        self.password = password
        self.database = "NavalFMS"

        self.connection = None
        self.cursor = None

        self.connect()

        if self.connection and self.cursor:
            self.crew = Crew(self.connection, self.cursor)
            self.ship = Ship(self.connection, self.cursor)
            self.mission = Mission(self.connection, self.cursor)
            self.documents = Document(self.connection, self.cursor)
            self.inventory = Inventory(self.connection, self.cursor)
            self.bases = Base(self.connection, self.cursor)
            self.routes = Route(self.connection, self.cursor)
    
    def connect(self):
        try:
            self.connection = connector.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database = self.database
            )
            
            self.cursor = self.connection.cursor()
        except Error as e:
            raise DatabaseConnectionError(f"Could not connect to database: {e}")
    
    def is_connected(self):
        return self.connection is not None and self.connection.is_connected()
    
    def disconnect(self):
        if self.is_connected():
            self.cursor.close()
            self.connection.close()

            self.cursor = None
            self.connection = None
    
    def changehost(self, host, password):
        if self.is_connected():
            self.disconnect()
        
        self.host = host
        self.password = password
        
        self.connect()