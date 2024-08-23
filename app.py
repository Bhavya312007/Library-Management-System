<<<<<<< Updated upstream
import login
import admin
import user
=======
import mysql.connector
from mysql.connector import Error
import hashlib
import login  # Assuming 'login.py' is a module you have
import admin  # Assuming 'admin.py' is a module you have
import user  # Assuming 'user.py' is a module you have
>>>>>>> Stashed changes

from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)

app.secret_key = '6268121321'

<<<<<<< Updated upstream

@app.route('/')
def main():   
    
  while True:
    login.login()

    log= login.log
    print(log)
    if log!= None:
        user_level = log[0]
        print(user_level)
        print(log)
        if user_level == 1:
            # print("------------------------------------------------------")
            # print("        Welcome to Advanced Library System")
            # print("------------------------------------------------------")
            # print("Welcome Admin")
            return redirect(url_for('admin.html'))

        elif user_level == 2:
            # print("Welcome to Advanced Library System")
            # print("Welcome User")
            return redirect(url_for('user.html'))
    else:
        print("Login failed")
        print("Please try again")
        main()


        
    return render_template('index.html')

=======
# Database connection function
def connect(host='localhost', db_user='root', db_password='', database='library'):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=db_user,
            password=db_password,
            database=database
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

# Main route
@app.route('/')
def main():
    if 'log' in session:
        user_level = session['log'][0]
        if user_level == 1:
            return redirect(url_for('admin_page'))
        elif user_level == 2:
            return redirect(url_for('user_page'))
    else:
        return redirect(url_for('login'))

# Home route
@app.route('/home')
>>>>>>> Stashed changes
def home():
    if 'username' in session:
        return render_template('index.html')
    return redirect(url_for('login'))
<<<<<<< Updated upstream
if __name__ == '__main__':
    app.run(debug=True)
=======

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    connection = connect()
    if not connection:
        return "Failed to connect to the database.", 500
    
    cursor = connection.cursor()
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']   
        hashed_password = hashlib.sha1(password.encode()).hexdigest()
        
        cursor.execute("SELECT user_level FROM users WHERE username = %s AND password = %s", (username, hashed_password))
        log = cursor.fetchone()
        
        if log:
            session['log'] = log
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('main'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    
    cursor.close()
    connection.close()
    return render_template('login.html')

# Admin page route
@app.route('/admin')
def admin_page():
    if 'username' in session and session.get('log')[0] == 1:
        return render_template('admin.html')
    else:
        return redirect(url_for('login'))

# User page route
@app.route('/user')
def user_page():
    if 'username' in session and session.get('log')[0] == 2:
        return render_template('user.html')
    else:
        return redirect(url_for('login'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('log', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))




if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> Stashed changes
