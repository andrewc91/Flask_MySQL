from flask import Flask, render_template, request, redirect
from mysqlconnection import MySQLConnector
import re
EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
app.secret_key = 'secretandrew'
mysql = MySQLConnector(app, 'friends')

@app.route('/')
def index():
    friends = mysql.query_db("SELECT * FROM friends")
    return render_template('index.html', friend=friends)
    
@app.route('/friends', methods=['POST'])
def create():
    query = "INSERT INTO friends (first_name, last_name, email, created_at, updated_at) Value(:first_name, :last_name, :email, NOW(), NOW())"
    
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
    }
    
    mysql.query_db(query, data)
    return redirect('/')

@app.route('/friends/<id>/edit')
def edit(id):
    data = {
        'id': id
    }
    friends = mysql.query_db('SELECT * FROM friends WHERE id=:id', data)
    return render_template('edit.html', friend=friends[0])

@app.route('/friends/<id>', methods=['POST'])
def update(id):
    query = "UPDATE friends SET first_name = :first_name, last_name=:last_name, email = :email WHERE id = :id"
    
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'id': id
    }
    mysql.query_db(query, data)
    return redirect('/')

@app.route('/friends/<id>/delete', methods=['GET'])
def destroy(id):
    query = "DELETE FROM friends WHERE id=:id"
    data = {
        'id': id
    }
    mysql.query_db(query, data)
    return redirect('/')

app.run(debug=True)