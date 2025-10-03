class Ship():
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
    
    def add(self, name, shipclass, pennantno, type, status, location, DockStatus):
        if self.connection.is_connected():
            self.cursor.execute("insert into Ship (name, class, penantnumber, shiptype, status, location, dockstatus) values (%s, %s, %s, %s, %s, %s, %s)", [name, shipclass, pennantno, type, status, location, DockStatus])
            self.connection.commit()
    
    def update(self, id, name = None, shipclass = None, pennanto = None, type = None, status = None, location = None, DockStatus = None):
        if self.connection.is_connected():
            if all(x is not None for x in [name, shipclass, pennanto, type, status, location, DockStatus]):
                self.cursor.execute("update Ship set name = %s, class = %s, penantnumber = %s, type = %s, status = %s, location = %s, DockStatus = %s where shipid = %s", [name, shipclass, pennanto, type, status, location, DockStatus, id])
                self.connection.commit()
            else:
                for k, v in { "name": name, "class": shipclass, "penantnumber": pennanto, "type": type, "status": status, "location": location, "DockStatus": DockStatus }.items():
                    if v is not None:
                        self.cursor.execute(f"update Ship set {k} = %s where shipid = %s", [v, id])
                        self.connection.commit()
    
    def delete(self, id):
        if self.connection.is_connected():
            self.cursor.execute("delete from Ship where shipid = %s", [id])
            self.connection.commit()
        
    def deleteall(self):
        if self.connection.is_connected():
            self.cursor.execute("delete from Ship")
            self.connection.commit()
    
    def fetchall(self):
        if self.connection.is_connected():
            self.cursor.execute("select shipid, name, class, penantnumber, shiptype from Ship")
            return self.cursor.fetchall()
    
    def search(self, id):
        if self.connection.is_connected():
            self.cursor.execute("select shipid, name, class, penantnumber, shiptype from Ship where shipid = %s", [id])
            return self.cursor.fetchall()
        
    def searchby(self, searchop, searchkey):
        if self.connection.is_connected():
            self.cursor.execute(f"select shipid, name, class, penantnumber, shiptype from Ship where {searchop} = %s", [searchkey])
            return self.cursor.fetchall()
    
    def fetchstats(self):
        if self.connection.is_connected():
            self.cursor.execute("select shipid, name, penantnumber, status from Ship")
            return self.cursor.fetchall()
    
    def fetchlocation(self):
        if self.connection.is_connected():
            self.cursor.execute("select shipid, name, penantnumber, location from Ship")
            return self.cursor.fetchall()
    
    def fetchdocked(self):
        if self.connection.is_connected():
            self.cursor.execute("select shipid, name, penantnumber from Ship where DockStatus = 'd'")
            return self.cursor.fetchall()
    
    def fetchundocked(self):
        if self.connection.is_connected():
            self.cursor.execute("select shipid, name, penantnumber from Ship where DockStatus = 'u'")
            return self.cursor.fetchall()
    
    def availabletypes(self):
        if self.connection.is_connected():
            self.cursor.execute("select distinct shiptype from Ship")
            return self.cursor.fetchall()
    
    def availableclasses(self):
        if self.connection.is_connected():
            self.cursor.execute("select distinct class from Ship")
            return self.cursor.fetchall()