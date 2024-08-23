import mysql.connector
from mysql.connector import Error
import hashlib
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = '6268121321'



today = date.today()
formatted_date = today.strftime('%B %d, %Y')




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
    
connection = connect()
cursor = connection.cursor()

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
def home():
    if 'username' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

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

# Functions for user management
@app.route('/admin/view_users')
def view_users():
    if 'username' not in session or session.get('log')[0] != 1:
        return redirect(url_for('login'))

    
    if not connection:
        return "Failed to connect to the database.", 500
    
    
    cursor.execute("SELECT * FROM users WHERE user_level = 2")
    users = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('view_users.html', users=users)

@app.route('/admin/add_user', methods=['GET', 'POST'])
def add_user():
    if 'username' not in session or session.get('log')[0] != 1:
        return redirect(url_for('login'))

    if request.method == 'POST':
        connection = connect()
        if not connection:
            return "Failed to connect to the database.", 500
        
        cursor = connection.cursor()
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha1(password.encode()).hexdigest()
        user_level = request.form['user_level']

        cursor.execute("INSERT INTO users (username, password, user_level) VALUES (%s, %s, %s)", 
                       (username, hashed_password, user_level))
        connection.commit()
        cursor.close()
        connection.close()

        flash('User added successfully!', 'success')
        return redirect(url_for('view_users'))

    return render_template('add_user.html')

@app.route('/admin/delete_user/<username>', methods=['POST'])
def delete_user(username):
    if 'username' not in session or session.get('log')[0] != 1:
        return redirect(url_for('login'))

    connection = connect()
    if not connection:
        return "Failed to connect to the database.", 500
    
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE username = %s", (username,))
    connection.commit()
    cursor.close()
    connection.close()

    flash('User deleted successfully!', 'success')
    return redirect(url_for('view_users'))

@app.route('/admin/update_user/<username>', methods=['GET', 'POST'])
def update_user(username):
    if 'username' not in session or session.get('log')[0] != 1:
        return redirect(url_for('login'))

    connection = connect()
    if not connection:
        return "Failed to connect to the database.", 500
    
    cursor = connection.cursor()

    if request.method == 'POST':
        password = request.form['password']
        hashed_password = hashlib.sha1(password.encode()).hexdigest()
        user_level = request.form['user_level']

        cursor.execute("UPDATE users SET password = %s, user_level = %s WHERE username = %s", 
                       (hashed_password, user_level, username))
        connection.commit()
        cursor.close()
        connection.close()

        flash('User updated successfully!', 'success')
        return redirect(url_for('view_users'))

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    return render_template('update_user.html', user=user)

# Functions for book management
@app.route('/admin/view_books')
def view_books():
    if 'username' not in session or session.get('log')[0] != 1:
        return redirect(url_for('login'))

    connection = connect()
    if not connection:
        return "Failed to connect to the database.", 500
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('view_books.html', books=books)

@app.route('/admin/add_book', methods=['GET', 'POST'])
def add_book():
    if 'username' not in session or session.get('log')[0] != 1:
        return redirect(url_for('login'))

    if request.method == 'POST':
        connection = connect()
        if not connection:
            return "Failed to connect to the database.", 500
        
        cursor = connection.cursor()
        bookno = request.form['bookno']
        name = request.form['name']
        author = request.form['author']
        category = request.form['category']
        quantity = request.form['quantity']

        cursor.execute("INSERT INTO books (bookno, name, author, category, quantity) VALUES (%s, %s, %s, %s, %s)", 
                       (bookno, name, author, category, quantity))
        connection.commit()
        cursor.close()
        connection.close()

        flash('Book added successfully!', 'success')
        return redirect(url_for('view_books'))

    return render_template('add_book.html')

@app.route('/admin/delete_book/<bookno>', methods=['POST'])
def delete_book(bookno):
    if 'username' not in session or session.get('log')[0] != 1:
        return redirect(url_for('login'))

    connection = connect()
    if not connection:
        return "Failed to connect to the database.", 500
    
    cursor = connection.cursor()
    cursor.execute("DELETE FROM books WHERE bookno = %s", (bookno,))
    connection.commit()
    cursor.close()
    connection.close()

    flash('Book deleted successfully!', 'success')
    return redirect(url_for('view_books'))

@app.route('/admin/update_book/<bookno>', methods=['GET', 'POST'])
def update_book(bookno):
    if 'username' not in session or session.get('log')[0] != 1:
        return redirect(url_for('login'))

    connection = connect()
    if not connection:
        return "Failed to connect to the database.", 500
    
    cursor = connection.cursor()

    if request.method == 'POST':
        name = request.form['name']
        author = request.form['author']
        category = request.form['category']
        quantity = request.form['quantity']

        cursor.execute("UPDATE books SET name = %s, author = %s, category = %s, quantity = %s WHERE bookno = %s", (name, author, category, quantity, bookno))
        connection.commit()
        cursor.close()
        connection.close()

        flash('Book updated successfully!', 'success')
        return redirect(url_for('view_books'))

    cursor.execute("SELECT * FROM books WHERE bookno = %s", (bookno,))
    book = cursor.fetchone()
    cursor.close()
    connection.close()

    return render_template('update_book.html', book=book)





@app.route('/user')
def user_page():
    if 'username' in session and session.get('log')[0] == 2:
        return render_template('user_dashboard.html')  # Create this HTML file for user actions
    else:
        return redirect(url_for('login'))

@app.route('/user_settings', methods=['GET', 'POST'])
def user_settings():
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        old_password = hashlib.sha1(old_password.encode()).hexdigest()
        user = session['username']
        
        if new_password == confirm_password:
            cursor.execute("SELECT password FROM users WHERE username = %s", (user,))
            password = cursor.fetchone()[0]
            if password == old_password:
                new_password = hashlib.sha1(new_password.encode()).hexdigest()
                cursor.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, user))
                connection.commit()
                flash('Password changed successfully', 'success')
                return redirect(url_for('user_page'))
            else:
                flash('Incorrect password', 'danger')
        else:
            flash('Passwords do not match', 'danger')
    
    return render_template('user_settings.html')  # Create this HTML form for changing the password

@app.route('/search_books', methods=['GET', 'POST'])
def search_books():
    if request.method == 'POST':
        search = request.form['search']
        cursor.execute("SELECT * FROM books WHERE name LIKE %s OR author LIKE %s", ('%' + search + '%', '%' + search + '%'))
        books = cursor.fetchall()
        return render_template('search_results.html', books=books)  # Create this HTML template to display search results
    
    return render_template('search_books.html')  # Create this HTML form to search for books

@app.route('/borrow_books', methods=['GET', 'POST'])
def borrow_books():
    if request.method == 'POST':
        cursor.execute("SELECT id FROM users WHERE username = %s", (session['username'],))
        user_id = cursor.fetchone()[0]
        bookid = request.form['bookid']
        
        cursor.execute("SELECT * FROM books WHERE bookno = %s", (bookid,))
        book = cursor.fetchone()
        
        if book:
            if book[4] > 0:
                quantity = book[4] - 1
                cursor.execute("INSERT INTO borrows (user_id, bookno, borrow_date) VALUES (%s, %s, %s)", (user_id, bookid, today))
                cursor.execute("UPDATE books SET quantity = %s WHERE bookno = %s", (quantity, bookid,))
                connection.commit()
                flash('Book borrowed successfully', 'success')
            else:
                flash('Book not available', 'danger')
        else:
            flash('Book not found', 'danger')
    
    return render_template('borrow_books.html')  # Create this HTML form to borrow books

@app.route('/return_books', methods=['GET', 'POST'])
def return_books():
    if request.method == 'POST':
        cursor.execute("SELECT id FROM users WHERE username = %s", (session['username'],))
        user_id = cursor.fetchone()[0]
        bookid = request.form['bookid']
        
        cursor.execute("SELECT * FROM borrows WHERE user_id = %s AND bookno = %s", (user_id, bookid))
        borrow = cursor.fetchone()
        
        if borrow:
            cursor.execute("DELETE FROM borrows WHERE user_id = %s AND bookno = %s", (user_id, bookid))
            cursor.execute("UPDATE books SET quantity = quantity + 1 WHERE bookno = %s", (bookid,))
            connection.commit()
            flash('Book returned successfully', 'success')
        else:
            flash('Book not borrowed', 'danger')
    
    return render_template('return_books.html')  # Create this HTML form to return books

@app.route('/renew_books', methods=['GET', 'POST'])
def renew_books():
    if request.method == 'POST':
        cursor.execute("SELECT id FROM users WHERE username = %s", (session['username'],))
        user_id = cursor.fetchone()[0]
        bookid = request.form['bookid']
        
        cursor.execute("SELECT * FROM borrows WHERE user_id = %s AND bookno = %s", (user_id, bookid))
        borrow = cursor.fetchone()
        
        if borrow:
            cursor.execute("UPDATE borrows SET borrow_date = %s WHERE user_id = %s AND bookno = %s", (today, user_id, bookid))
            connection.commit()
            flash('Book renewed successfully', 'success')
        else:
            flash('Book not borrowed', 'danger')
    
    return render_template('renew_books.html')  # Create this HTML form to renew books

@app.route('/fine_status')
def fine_status():
    cursor.execute("SELECT id FROM users WHERE username = %s", (session['username'],))
    user_id = cursor.fetchone()[0]
    cursor.execute("SELECT * FROM borrows WHERE user_id = %s AND borrow_date < CURRENT_DATE - INTERVAL 28 DAY", (user_id,))
    fines = cursor.fetchall()
    
    if len(fines) == 0:
        flash('You have no fine', 'info')
    else:
        flash('You have fines for the following books', 'warning')
    
    return render_template('fine_status.html', fines=fines)  # Create this HTML template to display fine status

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('log', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

