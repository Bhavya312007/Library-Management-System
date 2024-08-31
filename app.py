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
        
        cursor.execute("SELECT id,username FROM users WHERE username = %s AND password = %s", (username, hashed_password))
        log2 = cursor.fetchone()
        
        if log:
            session['log'] = log
            session['username'] = username
            session['log2'] = log2
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

    connection = connect()
    if not connection:
        return "Failed to connect to the database.", 500
    
    cursor = connection.cursor()
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

        cursor.execute("INSERT INTO users (username, password, user_level) VALUES (%s, \"%s\", %s);", 
                       (username, hashed_password, user_level))
        connection.commit()
        cursor.close()
        connection.close()

        flash('User added successfully!', 'success')
        return redirect(url_for('view_users'))

    return render_template('add_user.html')

@app.route('/admin/delete_user/<id>', methods=['POST'])
def delete_user(id):
    if 'username' not in session or session.get('log')[0] != 1:
        return redirect(url_for('login'))

    connection = connect()
    if not connection:
        return "Failed to connect to the database.", 500
    
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    connection.commit()
    cursor.close()
    connection.close()

    flash('User deleted successfully!', 'success')
    return redirect(url_for('view_users'))

@app.route('/admin/update_user/<id>', methods=['GET', 'POST'])
def update_user(id):
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

        cursor.execute("UPDATE users SET password = %s, user_level = %s WHERE id = %s", 
                       (hashed_password, user_level, id))
        connection.commit()
        cursor.close()
        connection.close()

        flash('User updated successfully!', 'success')
        return redirect(url_for('view_users'))

    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
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

        cursor.execute("UPDATE books SET name = %s, author = %s, category = %s, quantity = %s WHERE bookno = %s", 
                       (name, author, category, quantity, bookno))
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

# User settings and book management routes
@app.route('/user_settings', methods=['GET', 'POST'])
def user_settings():
    if 'username' not in session or session.get('log')[0] != 2:
        return redirect(url_for('login'))

    connection = connect()
    if not connection:
                return "Failed to connect to the database.", 500
    
    cursor = connection.cursor()

    if request.method == 'POST':
        oldPassword = request.form['old_password']
        newPassword = request.form['new_password']
        confirmPassword = request.form['confirm_password']
        old_hashed_password = hashlib.sha1(oldPassword.encode()).hexdigest()
        new_hashed_password = hashlib.sha1(newPassword.encode()).hexdigest()

        cursor.execute("SELECT id,username FROM users WHERE username = %s AND password = %s", (session['username'], old_hashed_password))
        if(cursor.fetchone()):
            if(newPassword==confirmPassword):
                cursor.execute("UPDATE users SET password = %s WHERE username = %s ;", (new_hashed_password, session['username']))
                flash('Password updated successfully!', 'success')
            else :
                flash("New password and confirm password does not match.",'danger')
        else :
            flash("Incorrect old Password.",'danger')
        connection.commit()
        # cursor.close()
        # connection.close()

        return redirect(url_for('user_page'))

    cursor.execute("SELECT * FROM users WHERE username = %s", (session['username'],))
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    return render_template('user_settings.html', user=user)

@app.route('/user/view_books')
def user_view_books():
    if 'username' not in session or session.get('log')[0] != 2:
        return redirect(url_for('login'))

    connection = connect()
    if not connection:
        return "Failed to connect to the database.", 500
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('user_view_books.html', books=books)
# Route to borrow books
@app.route('/borrow_books', methods=['GET', 'POST'])
def borrow_books():
    # Check if the user is logged in and is a standard user
    if 'log' not in session or session['log'][0] != 2:  # Ensure user_level is 2 (standard user)
        return redirect(url_for('login'))  # Redirect to login if not logged in or not a standard user

    # Establish a new database connection
    connection = connect()
    if not connection:
        return "Failed to connect to the database.", 500

    cursor = connection.cursor(dictionary=True)

    if request.method == 'POST':
        bookid = request.form.get('book_id')

        if bookid:  # Ensure book ID is provided
            cursor.execute("SELECT * FROM books WHERE bookno = %s", (bookid,))
            book = cursor.fetchone()

            if book:
                if book['quantity'] > 0:
                    # Borrow the book
                    quantity = book['quantity'] - 1
                    try:
                        cursor.execute("INSERT INTO borrows (user_id, bookno, borrow_date) VALUES (%s, %s, %s);",
                                       (session['log2'][0],bookid, date.today()))
                        cursor.execute("UPDATE books SET quantity = %s WHERE bookno = %s", (quantity, bookid))
                        connection.commit()
                        flash("Book borrowed successfully!","success")
                    except mysql.connector.Error as err:
                        flash(f"Error borrowing book: {err}")
                else:
                    flash("Book not available.")
            else:
                flash("Book not found.")
        else:
            flash("No book ID provided.")

    # Fetch available books for borrowing display
    cursor.execute("SELECT * FROM books WHERE quantity > 0")
    available_books = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    return render_template('borrow_books.html', books=available_books)

# Route to borrowed books
@app.route('/borrowed_books')
def borrowed_books():
    # Check if the user is logged in and is a standard user
    if 'log' not in session or session['log'][0] != 2:  # Ensure user_level is 2 (standard user)
        return redirect(url_for('login'))  # Redirect to login if not logged in or not a standard user

    # Establish a new database connection
    connection = connect()
    if not connection:
        return "Failed to connect to the database.", 500

    cursor = connection.cursor(dictionary=True)
    user_id = session['log2'][0]

    # Fetch available books for borrowing display
    cursor.execute("SELECT borrows.bookno AS bookno,borrow_date,return_date,name,author,category,quantity FROM borrows,books WHERE borrows.user_id=%s AND borrows.bookno=books.bookno;",(user_id,))
    borrowed_books = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    return render_template('borrowed_books.html', books=borrowed_books)

# Route to return books
@app.route('/return_books', methods=['GET', 'POST'])
def return_books():
    if 'log' in session:
        # Logic for returning books goes here            
        return render_template('return_books.html')
    else:
        flash('You need to log in first.')
        return redirect(url_for('login'))

# Route to renew books
@app.route('/renew_books', methods=['GET', 'POST'])
def renew_books():
    if 'log' in session:
        # Logic for renewing books goes here
        return render_template('renew_books.html')
    else:
        flash('You need to log in first.')
        return redirect(url_for('login'))

# Route to check fine status
@app.route('/fine_status')
def fine_status():
    if 'log' in session:
        # Logic for checking fine status goes here
        return render_template('fine_status.html')
    else:
        flash('You need to log in first.')
        return redirect(url_for('login'))

# Starting the Flask application
if __name__ == '__main__':
    app.run(debug=True)
