from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
from flask.ext.bcrypt import Bcrypt
import re

app = Flask(__name__)
mysql = MySQLConnector(app, 'thewall')
bcrypt = Bcrypt(app)
app.secret_key = 'secretandrew'

@app.route('/')
def index():
    return render_template('index.html')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile('^[A-Za-z\s]*$')

@app.route('/register', methods=['POST'])
def register():
    message = False
    #check error handling
    if len(request.form['first_name']) < 2:
        flash('First name too short!')
        message = True
    if len(request.form['last_name']) < 2:
        flash('Last name too short!')
        message = True
    if not EMAIL_REGEX.match(request.form['email']):
        flash('Email not valid!')
        message = True
    if len(request.form['password']) < 8:
        flash('Password must be at least 8 characters.')
        message = True
    if request.form['password'] != request.form['confirm']:
        flash('Passwords do not match!')
        message = True
        
    if message == True:
        return redirect('/')
    else:
        hashpass = bcrypt.generate_password_hash(request.form['password'])
        query = 'INSERT INTO users(first_name, last_name, email, password, created_at, updated_at) VALUES (:first_name, :last_name, :email, :password, NOW(), NOW())'
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': hashpass
        }
        new_user = mysql.query_db(query, data)
        session['user_id'] = new_user
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        return redirect('/wall')
        
    #if false, flash error, redirect index
    #if true, add to dateabase and redirect to the wall
        #add user to session
    
@app.route('/login', methods=['POST'])
def login():
    #check for errors, flash error if false
    query = 'SELECT * FROM users WHERE email = :email'
    data = {
        'email': request.form['email']
    }
    user = mysql.query_db(query, data)
    if not user:
        flash('Email does not exist')
        return redirect('/')
    elif bcrypt.check_password_hash(user[0]['password'], request.form['password']):
        flash('Password invalid')
        return redirect('/')
    else:
        session['user_id'] = user[0]['id']
        session['first_name'] = user[0]['first_name']
        session['last_name'] = user[0]['last_name']
        return redirect('/wall')

@app.route('/wall')
def showAll():
    # SELECT * FROM wall.messages;
    query = 'SELECT * FROM thewall.messages JOIN users ON users.id = messages.user_id'
    messages = mysql.query_db(query)
    # show messages = return render_template('wall.html')
    return render_template('wall.html', messages = messages)
    
@app.route('/message', methods=['POST'])
def message():
    # grab data from form, insert to database
    if not request.form['message']:
        flash('You entered nothing')
        return redirect('/wall')
    # redirect to the wall
    query = 'INSERT INTO messages(message, created_at, updated_at, user_id) VALUES (:message, NOW(), NOW(), :user_id)'
    data = {
        'message': request.form['message'],
        'user_id': session['user_id']
    }
    mysql.query_db(query, data)
    return redirect('/wall')
    
app.run(debug=True)