import datetime

class Mission:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

        self.controller = Controller(self.connection, self.cursor)
        self.planner = Planner(self.connection, self.cursor)

class Controller:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
    
    def start_mission(self, missionid, shipids):
        ids = ' '.join(str(id) for id in shipids)
        self.cursor.execute("update Mission set status = concat('Ongoing', ' ', %s) where missionid = %s", [ids, missionid])
        for shipid in shipids:
            self.cursor.execute("update Ship set status = 'Active', dockstatus = 'u', location = 'Location specified in Mission Document' where shipid = %s", [shipid])
        self.connection.commit()
    
    def end_mission(self, missionid, shipids):
        self.cursor.execute("update Mission set status = 'Completed', enddate = %s where missionid = %s", [datetime.date.today(), missionid])
        for shipid in shipids:
            self.cursor.execute("update Ship set status = 'Inactive' where shipid = %s", [shipid])
        self.connection.commit()
    
    def pause_mission(self, missionid):
        self.cursor.execute("update Mission set status = 'Paused' where missionid = %s", [missionid])
        self.connection.commit()
    
    def abort_mission(self, missionid, shipids):
        self.cursor.execute("update Mission set status = 'Aborted' where missionid = %s", [missionid])
        for shipid in shipids:
            self.cursor.execute("update Ship set status = 'Inactive' where shipid = %s", [shipid])
        self.connection.commit()
    
    def modifymission(self, missionid, name = None, type = None, objective = None, duration = None, startdate = None, enddate = None):
        if all(x is not None for x in [name, type, objective, duration, startdate, enddate]):
            self.cursor.execute("update Mission set name = %s, missiontype = %s, objective = %s, duration = %s, startdate = %s, enddate = %s where missionid = %s", [name, type, objective, duration, startdate, enddate, missionid])
            self.connection.commit()
        else:
            for k, v in { "name": name, "missiontype": type, "objective": objective, "duration": duration, "startdate": startdate, "enddate": enddate }.items():
                if v is not None:
                    self.cursor.execute(f"update Mission set {k} = %s where missionid = %s", [v, missionid])
                    self.connection.commit()
        

class Planner:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
    
    def plan_mission(self, name, type, objective, duration = None, startdate = None, enddate = None):
        self.cursor.execute("insert into Mission (name, missiontype, objective, status, duration, startdate, enddate) values (%s, %s, %s, 'Planned', %s, %s, %s)", [name, type, objective, duration, startdate, enddate])
        self.connection.commit()
    
    def delete_mission(self, missionid):
        self.cursor.execute("delete from Mission where missionid = %s", [missionid])
        self.connection.commit()
    
    def deleteall(self):
        self.cursor.execute("delete from Mission")
        self.connection.commit()
    
    def fetchall(self):
        self.cursor.execute("select * from Mission")
        return self.cursor.fetchall()
    
    def fetchplanned(self):
        self.cursor.execute("select * from Mission where status in ('Planned', 'Paused')")
        return self.cursor.fetchall()
    
    def fetchongoing(self):
        self.cursor.execute("select * from Mission where status like 'Ongoing%'")
        return self.cursor.fetchall()
    
    def fetchexecuted(self):
        self.cursor.execute("select * from Mission where status in ('Completed', 'Aborted')")
        return self.cursor.fetchall()
    
    def search(self, missionid):
        self.cursor.execute("select * from Mission where missionid = %s", [missionid])
        return self.cursor.fetchall()
    
    def searchby(self, searchop, searchkey):
        self.cursor.execute(f"select * from Mission where {searchop} = %s", [searchkey])
        return self.cursor.fetchall()

    def availabletypes(self):
        self.cursor.execute("select distinct missiontype from Mission")
        return self.cursor.fetchall()
    
    def availablestatuses(self):
        self.cursor.execute("select distinct status from Mission")
        return self.cursor.fetchall()
        