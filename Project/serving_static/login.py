# from flask import Flask, render_template, redirect, url_for, request
# import pymysql, login, app, Blueprint 


# # app = Flask(__name__)
# login = Blueprint('login.html', __name__, template_folder='templates')

# class Database:
#     def __init__(self):
#         host = "127.0.0.1"
#         user = "root"
#         password = "Wedgewood79$"
#         db = "project"
#         self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
#                                     DictCursor)
#         self.cur = self.con.cursor()
#     def list_users(self):
#         self.cur.execute("SELECT user_name, user_password FROM users")
#         result = self.cur.fetchall()
#         return result
 
# @login.route('/showusers')
# def showusers():
#     def db_query():
#         db = Database()
#         users = db.list_users()
#         return users
#     result = db_query()
#     return render_template('users.html', result=result, content_type='application/json')

# # @simple_page.route('/login.html')
# # def show(page):

# @login.route('/login.html',  methods=['GET', 'POST'])
# def loginFunc():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != 'admin' or request.form['password'] != 'admin':
#             error = 'Invalid Credentials. Please try again.'
#         else:
#             return redirect(url_for('home'))
#     return render_template('login.html', error=error)