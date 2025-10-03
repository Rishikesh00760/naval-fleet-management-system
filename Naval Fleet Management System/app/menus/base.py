class Base():
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
    
    def add_item(self, name, location, type, status):
        if self.connection.is_connected():
            self.cursor.execute("insert into Bases (name, location, type, status) values (%s, %s, %s, %s)", [name, location, type, status])
            self.connection.commit()
    
    def update_item(self, bid, name = None, location = None, type = None, status = None):
        if self.connection.is_connected():
            if all(x is not None for x in [name, location, type, status]):
                self.cursor.execute("update Bases set name = %s, location = %s, type = %s, status = %s where baseid = %s", [name, location, type, status, bid])
                self.connection.commit()
            else:
                for k, v in { "name": name, "location": location, "type": type, "status": status }.items():
                    if v is not None:
                        self.cursor.execute(f"update Bases set {k} = %s where baseid = %s", [v, bid])
                        self.connection.commit()
    
    def delete_item(self, bid):
        if self.connection.is_connected():
            self.cursor.execute("delete from Bases where baseid = %s", [bid])
            self.connection.commit()

    def delete_all(self):
        if self.connection.is_connected():
            self.cursor.execute("delete from Bases")
            self.connection.commit()
    
    def fetch_all(self):
        if self.connection.is_connected():
            self.cursor.execute("select * from Bases")
            return self.cursor.fetchall()
    
    def search(self, searchop, searchkey):
        if self.connection.is_connected():
            self.cursor.execute(f"select * from Bases where {searchop} = %s", [searchkey])
            return self.cursor.fetchall()
    
    def fetchtypes(self):
        if self.connection.is_connected():
            self.cursor.execute("select distinct type from Bases")
            return self.cursor.fetchall()

    def fetchstatuses(self):
        if self.connection.is_connected():
            self.cursor.execute("select baseid, name, status from Bases")
            return self.cursor.fetchall()