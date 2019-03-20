from flask import Flask, render_template, redirect, url_for, request
import pymysql
import dbClass

app = Flask(__name__)


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
        events = db.showEvents()
        return events
    result = db_query()
    return render_template('homePage.html', result=result, content_type='application/json')#First page the user sees
    #It will display news and other important updates

@app.route('/sports.html')
def sports():
    return render_template('sports.html')

@app.route('/test.html')
def _test():
    return render_template('newHomePageTest.html')

@app.route('/loginTest.html')
def _loginTest():
    return render_template('loginTest.html')

@app.route('/registerTest.html')
def _registerTest():
    return render_template('registerTest.html')

@app.route('/signup.html') #, methods=['GET', 'POST'])
def signup():
    error = None
    db = dbClass.Database()

    if request.method == 'PUT':
        userInputName = request.form['username']
        userInputPassword = request.form['password']
        
    
    return render_template('signup.html')

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
            return redirect(url_for('home'))#redirect to home
        else:
            error = 'Invalid Credentials. Please try again'

    return render_template('login.html', error=error)


if __name__ == "__main__":
    app.run()

    


