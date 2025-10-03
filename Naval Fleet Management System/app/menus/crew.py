class Crew:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
    
    def add(self, name, gender, dob, crew_type, status):
        if self.connection.is_connected():
            self.cursor.execute(
                "INSERT INTO Crew (Name, Gender, DOB, CrewType, Status) VALUES (%s, %s, %s, %s, %s)",
                [name, gender, dob, crew_type, status]
            )
            self.connection.commit()
    
    def update(self, crew_id, name=None, gender=None, dob=None, crew_type=None, status=None):
        if self.connection.is_connected():
            if all(x is not None for x in [name, gender, dob, crew_type, status]):
                self.cursor.execute(
                    "UPDATE Crew SET Name=%s, Gender=%s, DOB=%s, CrewType=%s, Status=%s WHERE CrewID=%s",
                    [name, gender, dob, crew_type, status, crew_id]
                )
                self.connection.commit()
            else:
                for k, v in {
                    "Name": name,
                    "Gender": gender,
                    "DOB": dob,
                    "CrewType": crew_type,
                    "Status": status
                }.items():
                    if v is not None:
                        self.cursor.execute(f"UPDATE Crew SET {k}=%s WHERE CrewID=%s", [v, crew_id])
                        self.connection.commit()
    
    def delete(self, crew_id):
        if self.connection.is_connected():
            self.cursor.execute("DELETE FROM Crew WHERE CrewID=%s", [crew_id])
            self.connection.commit()
    
    def deleteall(self):
        if self.connection.is_connected():
            self.cursor.execute("DELETE FROM Crew")
            self.connection.commit()
    
    def fetchall(self):
        if self.connection.is_connected():
            self.cursor.execute("SELECT crewid, Name, Gender, DOB, CrewType FROM Crew")
            return self.cursor.fetchall()
    
    def search(self, crew_id):
        if self.connection.is_connected():
            self.cursor.execute("SELECT crewid, Name, Gender, DOB, CrewType FROM Crew WHERE CrewID=%s", [crew_id])
            return self.cursor.fetchall()
        
    def searchby(self, searchop, searchkey):
        if self.connection.is_connected():
            self.cursor.execute(f"SELECT crewid, Name, Gender, DOB, CrewType FROM Crew WHERE {searchop}=%s", [searchkey])
            return self.cursor.fetchall()
    
    def fetchstats(self):
        if self.connection.is_connected():
            self.cursor.execute("SELECT CrewID, Name, Status FROM Crew")
            return self.cursor.fetchall()
    
    def availabletypes(self):
        if self.connection.is_connected():
            self.cursor.execute("SELECT DISTINCT CrewType FROM Crew")
            return self.cursor.fetchall()
