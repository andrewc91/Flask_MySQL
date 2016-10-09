from flask import Flask, render_template, request, redirect, flash
import re
app = Flask(__name__)
app.secret_key = 'secretandrew'

from mysqlconnection import MySQLConnector
mysql = MySQLConnector (app, 'emails')
EREG = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/email', methods = ['POST'])
def validate():
    print request.form['email']
    if not EREG.match(request.form['email']):
        flash("Try again next time!")
        return redirect('/')
    else: 
        query = 'INSERT INTO user_emails(email, created_at, updated_at) values(:email, now(), now())'
        data = {
            'email': request.form["email"]
        }
        mysql.query_db(query, data)
        flash("Yay we did it")
        return redirect('/success')

@app.route('/success')
def success():
    query = "SELECT * FROM user_emails"
    emails = mysql.query_db(query)
    return render_template('success.html', emails = emails)

@app.route('/delete/<id>')
def delete(id):
    query = "DELETE FROM user_emails WHERE id = :id"
    data = {'id': id}
    mysql.query_db(query, data)
    return redirect('/success')

app.run(debug=True)