class Document():
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

        self.reports = Reports(self.connection, self.cursor)
        self.logs = Logs(self.connection, self.cursor)

class Reports():
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
    
    def create_report(self, title, description, content, document_type):
        if self.connection.is_connected():
            self.cursor.execute("insert into Documents (title, description, content, documenttype) values (%s, %s, %s, %s)", [title, description, content, document_type])
            self.connection.commit()
    
    def read(self, did):
        if self.connection.is_connected():
            self.cursor.execute("select * from Documents where documentid = %s", [did])
            return self.cursor.fetchall()
    
    def show_all(self):
        if self.connection.is_connected():
            self.cursor.execute("select documentid, title, description, documenttype, createdat from Documents")
            return self.cursor.fetchall()
    
    def search(self, searchop, searchkey):
        if self.connection.is_connected():
            self.cursor.execute(f"select documentid, title, description, documenttype, createdat from Documents where {searchop} = %s", [searchkey])
            return self.cursor.fetchall()
    
    def delete(self, did):
        if self.connection.is_connected():
            self.cursor.execute("delete from Documents where documentid = %s", [did])
            self.connection.commit()
    
    def delete_all(self):
        if self.connection.is_connected():
            self.cursor.execute("delete from Documents")
            self.connection.commit()
    
    def available_types(self):
        if self.connection.is_connected():
            self.cursor.execute("select distinct documenttype from Documents")
            return self.cursor.fetchall()

class Logs():
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
    
    def add(self, title, description):
        if self.connection.is_connected():
            self.cursor.execute("insert into Logs (title, description) values (%s, %s)", [title, description])
            self.connection.commit()
    
    def read(self, logid):
        if self.connection.is_connected():
            self.cursor.execute("select * from Logs where logid = %s", [logid])
            return self.cursor.fetchall()
    
    def read_all(self):
        if self.connection.is_connected():
            self.cursor.execute("select * from Logs")
            return self.cursor.fetchall()
        