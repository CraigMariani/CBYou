from flask import Flask, render_template, redirect, url_for, request, flash, session, logging, abort, g
from flask_apscheduler import APScheduler
from apscheduler.triggers.cron import CronTrigger
from passlib.hash import sha256_crypt

import pymysql
import dbClass
import hashlib, uuid    

app = Flask(__name__)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
app.secret_key = 'super secret key'

hashedPasssword = None

@app.route('/showusers')
def showusers():
    def db_query(): 
        db = dbClass.Database()
        users = db.list_users()
        return users
    result = db_query()
    return render_template('users.html', result=result, content_type='application/json')

@app.route('/')
def home():
    def db_query():
        db = dbClass.Database()
        events = db.loadEvents()
        return events
    result = db_query()
    return render_template('homepage_new.html', result=result, content_type='application/json')#First page the user sees
    #It will display news and other important updates

@app.route('/schedule.html')
def schedule():
    def db_query():
        db = dbClass.Database()
        schedule = db.showSchedule()
        return schedule
    result = db_query()
    return render_template('schedule.html', result=result, content_type='application/json')

@app.route('/test.html')
def _test():
    return render_template('homepage_new.html')

@app.route('/study.html')
def _study():
    return render_template('study.html')
# @app.route('/loginTest.html')
# def _loginTest():
#     return render_template('loginTest.html')

# @app.route('/registerTest.html')
# def _registerTest():
#     return render_template('registerTest.html')

# @app.route('/signup.html', methods=['GET','POST']) 
@app.route('/signup.html', methods=['GET','POST']) 
def signup():
    error = None
    userInputName = None
    userInputPassword = None
    signupUser = None
    signupPassword = None

    

    db = dbClass.Database()
    
    if request.method == 'POST':
        userInputName = request.form['username']
        userInputPassword = request.form['password']

        #work on hashing the password later!
        # salt = uuid.uuid4().hex
        # hashed_password = hashlib.sha512(userInputPassword + salt).hexdigest()
        
        # signupUser = db.registerUser(userInputName)
        # signupPassword = db.registerPassword(userInputPassword)

        #work on having credentials to pass for username and password inside of below if statement!
        #example: username and password are both unique, contain min amount of chars, unique chars
        # if signupUser == userInputName and signupPassword == userInputPassword:

        
        #instead of this hash the password first!

        #hashedPassword = hashlib.md5(userInputPassword.encode())

        hashedpassword = sha256_crypt.encrypt(userInputPassword)

        #db.importUser(userInputName, hashedPassword.hexdigest())
        db.importUser(userInputName, hashedPassword)
        error = "Sign up successful"

        # else:
        #     error = "Error could not input to database"

    return render_template('signup.html', error=error)

# @app.route('/login.html',  methods=['GET', 'POST'])
@app.route('/login.html',  methods=['GET', 'POST'])
def login():
    error = None
    db = dbClass.Database()

    if request.method == 'POST': #if the user asks to submit his login to the database
       
    #access HTML input in login.HTML, stores username and password submitted 
        userInputName = request.form['username']
        userInputPassword = request.form['password']

    #access Python in dbClass.py 
        userCheck = db.checkUser(userInputName)
        pwdCheck = db.checkPassword(userInputName)


        #If the user input password and username are the same as the one in the database
        if userCheck == userInputName and pwdCheck == userInputPassword: 
            session['logged_in'] = True
            currentUser = db.getUserID(userCheck)
            return redirect(url_for('home'))#redirect to home
        else:
            error = 'Invalid Credentials. Please try again'

    return render_template('login.html', error=error)

@app.route('/forums.html')
def forum():
    return render_template('forums.html')

def update_events():
    db = dbClass.Database()
    sports = db.updateEvents()
    return

@app.route('/update.html')
def update():
    update_events()
    return render_template('secret.html')

@app.route('/delete.html')
def delete():
    dbClass.Database().delete_events()
    return render_template('secret.html')

if __name__ == "__main__":
    # app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    sess.init_app(app)


    app.run()


#app.apscheduler.add_job(update_events, 'cron', hour=0, minute=5)