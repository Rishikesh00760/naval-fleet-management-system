import sqlite3
import keyring
from os import path

class Hosts():
    def __init__(self):
        if path.exists("hosts.db") == False:
            with open("hosts.db", "w") as f:
                pass

        self.connection = sqlite3.connect("hosts.db")
        self.cursor = self.connection.cursor()

        self.cursor.execute("create table if not exists hosts(HostID integer primary key autoincrement, Hostname varchar(255) not null unique)")
        self.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()
    
    def commit(self):
        self.connection.commit()
    
    def addhost(self, hostname, password):
        keyring.set_password("NavalFMS", hostname, password)
        self.cursor.execute("insert into hosts (Hostname) values (?)", [hostname])
        self.commit()
    
    def updatehost(self, hostid, hostname, password):
        keyring.set_password("NavalFMS", hostname, password)
        self.cursor.execute("update hosts set hostname = (?) where hostid = (?)", [hostname, hostid])
        self.commit()
    
    def deletehost(self, hostid):
        keyring.delete_password("NavalFMS", self.gethost(hostid)[0][1])
        self.cursor.execute("delete from hosts where hostid = (?)", [hostid])
        self.commit()
    
    def gethosts(self):
        self.cursor.execute("select HostID, Hostname from hosts")
        return self.cursor.fetchall()
    
    def gethost(self, hostid):
        self.cursor.execute("select * from hosts where hostid = ?", [hostid])
        return self.cursor.fetchall()
    
    def getpassword(self, hostname):
        return keyring.get_password("NavalFMS", hostname)
    
    def clear(self):
        for host in self.gethosts():
            keyring.delete_password("NavalFMS", host[1])
        self.cursor.execute("delete from hosts")
        self.commit()