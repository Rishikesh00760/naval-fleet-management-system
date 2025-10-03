class Route():
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
    
    def fetch_all(self):
        if self.connection.is_connected():
            self.cursor.execute("select * from Routes")
            return self.cursor.fetchall()
    
    def fetch_route(self, route_id):
        if self.connection.is_connected():
            self.cursor.execute("select * from Routes where routeid = %s", [route_id])
            return self.cursor.fetchall()
    
    def add(self, name, startlocation, endlocation, waypoints, distance):
        if self.connection.is_connected():
            self.cursor.execute(
                "insert into Routes (name, startlocation, endlocation, waypoints, distance) values (%s, %s, %s, %s, %s)",
                (name, startlocation, endlocation, waypoints, distance)
            )
            self.connection.commit()
    
    def delete(self, route_id):
        if self.connection.is_connected():
            self.cursor.execute("delete from Routes where routeid = %s", [route_id])
            self.connection.commit()
    
    def delete_all(self):
        if self.connection.is_connected():
            self.cursor.execute("delete from Routes")
            self.connection.commit()
    
    def update(self, route_id, name=None, startlocation=None, endlocation=None, waypoints=None, distance=None):
        if self.connection.is_connected():
            if all(x is not None for x in [name, startlocation, endlocation, waypoints, distance]):
                self.cursor.execute("update Routes set name = %s, startlocation = %s, endlocation = %s, waypoints = %s, distance = %s where routeid = %s", (name, startlocation, endlocation, waypoints, distance, route_id))
                self.connection.commit()
            else:
                for k, v in { "name": name, "startlocation": startlocation, "endlocation": endlocation, "waypoints": waypoints, "distance": distance }.items():
                    if v is not None:
                        self.cursor.execute(f"update Routes set {k} = %s where routeid = %s", [v, route_id])
                        self.connection.commit()