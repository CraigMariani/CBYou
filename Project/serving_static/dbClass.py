import pymysql

class Database:
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

    def list_users(self):
        self.cur.execute("SELECT user_name, user_password FROM users")
        result = self.cur.fetchall()
        return result

    def checkUser(self, user):  #what does %s mean? Regex for user Input?
        stmt = "SELECT user_name FROM users where user_name = ?" #pulls user_name from database users
        self.cur.execute(stmt, user) #executes statment with cursor
        row=self.cur.fetchone() #used for capturing a single value
        if row != None:
            return row['user_name'] #this returns the column user_name 
    
    def checkPassword(self, user):
        stmt = "SELECT user_password FROM users where user_name = ?"
        self.cur.execute(stmt, user)
        row=self.cur.fetchone()
        if row != None:
            return row['user_password']