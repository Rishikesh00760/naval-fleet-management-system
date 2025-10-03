class Inventory():
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
    
    def add_item(self, name, category, quantity):
        if self.connection.is_connected():
            self.cursor.execute("insert into Inventory (name, category, quantity) values (%s, %s, %s)", [name, category, quantity])
            self.connection.commit()
    
    def update_item(self, itemid, name = None, category = None, quantity = None):
        if self.connection.is_connected():
            if all(x is not None for x in [name, category, quantity]):
                self.cursor.execute("update Inventory set name = %s, category = %s, quantity = %s where itemid = %s", [name, category, quantity, itemid])
                self.connection.commit()
            else:
                for k, v in { "name": name, "category": category, "quantity": quantity }.items():
                    if v is not None:
                        self.cursor.execute(f"update Inventory set {k} = %s where itemid = %s", [v, itemid])
                        self.connection.commit()
    
    def delete_item(self, itemid):
        if self.connection.is_connected():
            self.cursor.execute("delete from Inventory where itemid = %s", [itemid])
            self.connection.commit()

    def delete_all(self):
        if self.connection.is_connected():
            self.cursor.execute("delete from Inventory")
            self.connection.commit()
    
    def fetch_all(self):
        if self.connection.is_connected():
            self.cursor.execute("select * from Inventory")
            return self.cursor.fetchall()
    
    def search(self, searchop, searchkey):
        if self.connection.is_connected():
            self.cursor.execute(f"select * from Inventory where {searchop} = %s", [searchkey])
            return self.cursor.fetchall()
    
    def fetch_categories(self):
        if self.connection.is_connected():
            self.cursor.execute("select distinct category from Inventory")
            return self.cursor.fetchall()