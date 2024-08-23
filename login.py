import conn
import hashlib
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)


connection = conn.connect()

global username
global password

if connection.is_connected():
    cursor = connection.cursor()
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        global log
        
        global username
        global password

        if request.method == 'POST':
          username = request.form['username']
          password = request.form['password']   
          hashed_password = hashlib.sha1(password.encode()).hexdigest()
          print(hashed_password)
          cursor.execute("SELECT user_level FROM users WHERE username = %s AND password = %s", (username, hashed_password))
          log= cursor.fetchone()
        #   print(cursor.rowcount)
        #   print(log)
          if cursor.rowcount > 0:
              # print("Login successful")
              # print("Welcome " + username)
              # return username
              session['username'] = username
              flash('Login successful!', 'success')
              return redirect(url_for('main'))
          return log,username
          # else:
          #     print("Login failed")
          #     print("Please try again")
          #     login()
        else:
              flash('Invalid credentials. Please try again.', 'danger')
        return render_template('login.html')
else:
    print("Failed to connect to the database.")

