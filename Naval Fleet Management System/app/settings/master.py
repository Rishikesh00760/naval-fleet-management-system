import sqlite3
from passlib.hash import bcrypt
from os import path

class Master():
    def __init__(self, hosts):
        if path.exists("master.db") == False:
            with open("master.db", "w") as f:
                pass

        self.connection = sqlite3.connect("master.db")
        self.cursor = self.connection.cursor()

        self.cursor.execute("create table if not exists master(master varchar not null)")
        self.commit()

        self.hosts = hosts
    
    def close(self):
        self.cursor.close()
        self.connection.close()
    
    def commit(self):
        self.connection.commit()
    
    def setpassword(self, password):
        passhash = bcrypt.hash(password)
        self.cursor.execute("insert into master values (?)", [passhash])
        self.commit()
    
    def changepassword(self, password):
        passhash = bcrypt.hash(password)
        self.cursor.execute("update master set master = (?)", [passhash])
        self.commit()
    
    def gethash(self):
        self.cursor.execute("select * from master")
        row = self.cursor.fetchone()
        if row:
            return row[0]
        return None

    def verifypassword(self, password):
        if bcrypt.verify(password, self.gethash()):
            return True
        return False
    
    def forgetpassword(self):
        self.hosts.clear()
        self.cursor.execute("delete from master")
        self.commit()