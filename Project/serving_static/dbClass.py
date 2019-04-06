import pymysql
import events_parsing

class Database():
    def __init__(self): 
        host = "127.0.0.1"
        user = "root"
        password = "Wedgewood79$"
        db = "project"
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                    DictCursor)
        self.cur = self.con.cursor()

    def showEvents(self):
        self.cur.execute("SELECT * FROM events")
        result = self.cur.fetchall()
        return result

    def showSschedule(self):
        self.cur.execute("SELECT * FROM schedule")
        result = self.cur.fetchall()
        return result

    def importUser(self, user, pword):
        stmt = "INSERT INTO users (user_name, user_password) VALUES (%s, %s)"
        val = (user,pword)
        self.cur.execute(stmt,val)
        # self.cur.execute("SELECT MAX user_id FROM users")
        self.cur.execute("DELETE FROM users WHERE user_name ='' ")
        self.cur.execute("DELETE FROM users WHERE user_password ='' ")
        self.con.commit()
        result = self.cur.fetchall()
        return result

    # def registerUser(self, user):
    #     insertStmt = "INSERT INTO users (user_name) VALUES(%s)"
    #     retrieveStmt = "SELECT user_name from users WHERE user_name = %s"
        
    #     self.cur.execute(insertStmt, user)
    #     self.cur.execute(retrieveStmt, user)

    #     row=self.cur.fetchone()
    #     if row != None:
    #         return row['user_name']
    
    # def registerPassword(self, pword):
    #     insertStmt = "INSERT INTO users (user_password) VALUES(%s)"
    #     retrieveStmt = "SELECT user_password FROM users WHERE user_password = %s"
        
    #     self.cur.execute(insertStmt, pword)
    #     self.cur.execute(retrieveStmt, pword)

    #     row=self.cur.fetchone()
    #     if row != None:
    #         return row['user_password']
        
    def list_users(self):
        self.cur.execute("SELECT user_name, user_password FROM users")
        result = self.cur.fetchall()
        return result

    def getUserID(self, user):
        stmt = "SELECT user_id FROM users WHERE user_name = %s"
        self.cur.execute(stmt, user)#eror in SQL syntax look here!
        result = self.cur.fetchone()
        return result


    def checkUser(self, user):  
        stmt = "SELECT user_name FROM users where user_name = %s" 
        self.cur.execute(stmt, user) #executes statment with cursor

        row=self.cur.fetchone() #used for capturing a single value
        if row != None:
            return row['user_name'] #this returns the column user_name 
    
    def checkPassword(self, user):
        stmt = "SELECT user_password FROM users where user_name = %s"
        self.cur.execute(stmt, user)
        row=self.cur.fetchone()
        if row != None:
            return row['user_password']

    def loadEvents(self):
        self.cur.execute("SELECT * FROM events")
        result = self.cur.fetchall()
        return result

    def updateEvents(self):
        events = events_parsing.load_CBU_events()
        self.cur.execute("DELETE FROM events")
        self.con.commit()
        for event in events:
            insertSQL = "INSERT INTO events VALUES ('"+ event['hours'] + "', '" + event['description'] + "', '" +  event['date'] + "')"
            self.cur.execute(insertSQL)
            self.con.commit()
        return
    
    def delete_events(self):
        self.cur.execute("DELETE FROM events")
        print("test")
        self.con.commit()
        return