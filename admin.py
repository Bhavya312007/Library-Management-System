import conn
import hashlib

connection = conn.connect()

if connection.is_connected():
    cursor = connection.cursor()

    def admin():
        print("Admin Page")
        

        

    def user():
        print("User Page")
        print("1. Add User")
        print("2. View Users")
        print("3. Delete User")
        print("4. Update User")
        print("5. Logout")
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
        else:
            print("Invalid choice")
            user()
    
    def page():
        print("1. Add Book")
        print("2. View Books")
        print("3. Delete Book")
        print("4. Update Book")
        print("5. Logout")
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

    def add_user():
        print("Add User")
        username = input("Enter username: ")
        password = input("Enter password: ")
        hashed_password = hashlib.sha1(password.encode()).hexdigest()
        user_level = input("Enter user level: ")
        cursor.execute("INSERT INTO users (username, password, user_level) VALUES (%s, %s, %s)", (username, hashed_password, user_level))
        connection.commit()
        print("User added successfully")
        user()
        
    def view_users():
        print("View Users")
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        for user in users:
            print(user)
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
        username = input("Enter username: ")
        password = input("Enter password: ")
        hashed_password = hashlib.sha1(password.encode()).hexdigest()
        user_level = input("Enter user level: ")
        cursor.execute("UPDATE users SET password = %s, user_level = %s WHERE username = %s", (hashed_password, user_level, username))
        connection.commit()
        print("User updated successfully")
        user()

    

