import conn
import login
import hashlib
# import main

connection = conn.connect()

if connection.is_connected():
    cursor = connection.cursor()

    def user():
        print("User Page")
        print("1. User Settings")
        print("2. Search Books")
        print("3. Borrow Books")
        print("4. Return Books")
        print("5. Renew Books")
        print("6. Fine Status")
        print("7. Logout")

        choice = input("Enter your choice: ")
        if choice == '1':
            user_settings()
        elif choice == '2':
            search_books()
        elif choice == '3':
            borrow_books()
        elif choice == '4':
            return_books()
        elif choice == '5':
            renew_books()
        elif choice == '6':
            fine_status()
        elif choice == '7':
            logout()
        else:
            print("Invalid choice")
            user()

    def user_settings():
        print("User Settings")
        print("1. Change Password")
        print("2. Logout")
        choice = input("Enter your choice: ")
        if choice == '1':
            change_password()
        elif choice == '2':
            logout()
        else:
            print("Invalid choice")
            user_settings()
    
    def change_password():
        print("Change Password")
        old_password = input("Enter your old password: ")
        new_password = input("Enter your new password: ")
        confirm_password = input("Confirm your new password: ")
        old_password = hashlib.sha1(old_password.encode()).hexdigest()
        if new_password == confirm_password:
            cursor.execute("SELECT password FROM users WHERE username = %s", (login.username,))
            password = cursor.fetchone()[0]
            if password == old_password:
                new_password = hashlib.sha1(new_password.encode()).hexdigest()
                cursor.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, login.username))
                connection.commit()
                print("Password changed successfully")
                logout()
            else:
                print("Incorrect password")
                change_password()
        else:
            print("Passwords do not match")
            change_password()

    def search_books():
        print("Search Books")
        search = input("Enter book name or author: ")
        cursor.execute("SELECT * FROM books WHERE name LIKE %s OR author LIKE %s", ('%' + search + '%', '%' + search + '%'))
        books = cursor.fetchall()
        for book in books:
            print(book)
        user()

    def borrow_books():
        print("Borrow Books")
        bookid = input("Enter book ID: ")
        cursor.execute("SELECT * FROM books WHERE bookid = %s", (bookid,))
        book = cursor.fetchone()
        if book != None:
            if book[4] == 0:
                cursor.execute("INSERT INTO borrow (username, bookid) VALUES (%s, %s)", (login.username, bookid))
                cursor.execute("UPDATE books SET available = 1 WHERE bookid = %s", (bookid,))
                connection.commit()
                print("Book borrowed successfully")
                user()
            else:
                print("Book not available")
                user()
        else:
            print("Book not found")
            user()

    def return_books():
        print("Return Books")
        bookid = input("Enter book ID: ")
        cursor.execute("SELECT * FROM borrow WHERE username = %s AND bookid = %s", (login.username, bookid))
        borrow = cursor.fetchone()
        if borrow != None:
            cursor.execute("DELETE FROM borrow WHERE username = %s AND bookid = %s", (login.username, bookid))
            cursor.execute("UPDATE books SET available = 0 WHERE bookid = %s", (bookid,))
            connection.commit()
            print("Book returned successfully")
            user()
        else:
            print("Book not borrowed")
            user()

    def renew_books():
        print("Renew Books")
        bookid = input("Enter book ID: ")
        cursor.execute("SELECT * FROM borrow WHERE username = %s AND bookid = %s", (login.username, bookid))
        borrow = cursor.fetchone()
        if borrow != None:
            cursor.execute("UPDATE borrow SET date_borrowed = CURRENT_DATE WHERE username = %s AND bookid = %s", (login.username, bookid))
            connection.commit()
            print("Book renewed successfully")
            user()
        else:
            print("Book not borrowed")
            user()

    def fine_status():
        print("Fine Status")
        cursor.execute("SELECT * FROM borrow WHERE username = %s AND date_borrowed < CURRENT_DATE - INTERVAL 28 DAY", (login.username,))
        fines = cursor.fetchall()
        if len(fines) == 0:
            print("You have no fine")
        else:
            print("You have fine for the following books")
            for fine in fines:
               print(fine)
            user()
            print("Pay Fine in Accounts Block")

    def logout():
        print("Logout")
        # main.main()


user()