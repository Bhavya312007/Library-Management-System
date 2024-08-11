import conn
import hashlib


connection = conn.connect()

if connection.is_connected():
    cursor = connection.cursor()

    def admin():
        print("Admin Page")
        print("1. User Settings")
        print("2. Book Settings")
        print("3. Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            user()
        elif choice == '2':
            page()
        elif choice == '3':
            logout()
        else:
            print("Invalid choice")
            admin()
        

        

    def user():
        print("User Page")
        print("1. Add User")
        print("2. View Users")
        print("3. Delete User")
        print("4. Update User")
        print("5. Logout")
        print("6. Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_user()
        elif choice == '2':
            view_users()
        elif choice == '3':
            delete_user()
        elif choice == '4':
            update_user()
        elif choice == '5':
            logout()
        elif choice == '6':
            admin()
        else:
            print("Invalid choice")
            user()
    
    def page():
        print("1. Add Book")
        print("2. View Books")
        print("3. Delete Book")
        print("4. Update Book")
        print("5. Logout")
        print("6. Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_book()
        elif choice == '2':
            view_books()
        elif choice == '3':
            delete_book()
        elif choice == '4':
            update_book()
        elif choice == '5':
            logout()
        elif choice == '6':
            admin()
        else:
            print("Invalid choice")
            page()

    def add_user():
        print("Add User")
        username = input("Enter username: ")
        password = input("Enter password: ")
        hashed_password = hashlib.sha1(password.encode()).hexdigest()
        user_level = input("Enter user level: ")
        if user_level == '1' or user_level == '2':
            pass
        else:
            print("Invalid user level")
            add_user()
        cursor.execute("INSERT INTO users (username, password, user_level) VALUES (%s, %s, %s)", (username, hashed_password, user_level))
        connection.commit()
        print("User added successfully")
        user()
        
    def view_users():
        print("View Users")
        cursor.execute("SELECT * FROM users where user_level = 2")
        users = cursor.fetchall()
        for u in users:
            print(u)
        user()
    
    def delete_user():
        print("Delete User")
        username = input("Enter username: ")
        cursor.execute("DELETE FROM users WHERE username = %s", (username,))
        connection.commit()
        print("User deleted successfully")
        user()

    def update_user():
        print("Update User")
        username = input("Enter username of the User: ")
        password = input("Enter password For Change: ")
        hashed_password = hashlib.sha1(password.encode()).hexdigest()
        user_level = input("Enter user level To Change: ")
        cursor.execute("UPDATE users SET password = %s, user_level = %s WHERE username = %s", (hashed_password, user_level, username))
        connection.commit()
        print("User updated successfully")
        user()

    def add_book():
        print("Add Book")
        bookno = input("Enter bookno: ")
        name = input("Enter name: ")
        author = input("Enter author: ")
        category = input("Enter category: ")
        quantity = input("Enter quantity: ")
        cursor.execute("INSERT INTO books (bookno,name, author, category, quantity) VALUES (%s, %s,%s, %s,%s)", (bookno,name, author, category, quantity))
        connection.commit()
        print("Book added successfully")
        page()

    def view_books():
        print("View Books")
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        for book in books:
            print(book)
        page()
    
    def delete_book():
        print("Delete Book")
        name = input("Enter Bookno: ")
        cursor.execute("DELETE FROM books WHERE bookno = %s", (name,))
        connection.commit()
        print("Book deleted successfully")
        page()

    def update_book():
        print("Update Book")
        name = input("Enter name: ")
        author = input("Enter author: ")
        category = input("Enter category: ")
        quantity = input("Enter quantity: ")
        cursor.execute("UPDATE books SET author = %s, category = %s, quantity = %s WHERE name = %s", (author, category, quantity, name))
        connection.commit()
        print("Book updated successfully")
        page()

    def logout():
        print("Logout")
        connection.close()
        # login.login()
        # main.main()


# admin()


# admin()