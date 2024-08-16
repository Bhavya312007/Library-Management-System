import conn
import login
import hashlib
from datetime import date
today = date.today()
formatted_date = today.strftime('%B %d, %Y')
print(formatted_date)


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
        user = login.username
        print(user)
        if new_password == confirm_password:
            cursor.execute("SELECT password FROM users WHERE username = %s", (user,))
            password = cursor.fetchone()[0]
            if password == old_password:
                new_password = hashlib.sha1(new_password.encode()).hexdigest()
                cursor.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, login.username))
                connection.commit()
                print("Password changed successfully")
                # logout()
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
        cursor.execute("SELECT id FROM users WHERE username = %s", (login.username,))
        user_id = cursor.fetchone()[0]
        print("Borrow Books")
        bookid = input("Enter book ID: ")
        print(bookid)
        cursor.execute("SELECT * FROM books WHERE bookno = %s", (bookid,))
        book = cursor.fetchone()
        print(book)
        
        if book:
            if book[4] > 0:
                quantity=book[4]-1
                cursor.execute("INSERT INTO borrows (user_id, bookno ,borrow_date) VALUES (%s, %s,%s)", (user_id, bookid, today))
                cursor.execute("UPDATE books SET quantity = %s WHERE bookno = %s", (quantity,bookid,))
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
        cursor.execute("SELECT id FROM users WHERE username = %s", (login.username,))
        user_id = cursor.fetchone()[0]
        print("Return Books")
        bookid = input("Enter book ID: ")
        cursor.execute("SELECT * FROM borrows WHERE user_id = %s AND bookno = %s", (user_id, bookid))
        borrow = cursor.fetchone()
        
        print(borrow)
        if borrow != None:
            cursor.execute("DELETE FROM borrows WHERE user_id = %s AND bookno = %s", (user_id, bookid))
            cursor.execute("UPDATE books SET quantity = quantity + 1 WHERE bookno = %s", (bookid,))

            connection.commit()
            print("Book returned successfully")
            user()
        else:
            print("Book not borrowed")
            user()

    def renew_books():
        cursor.execute("SELECT id FROM users WHERE username = %s", (login.username,))
        user_id = cursor.fetchone()[0]
        print("Renew Books")
        bookid = input("Enter book ID: ")
        cursor.execute("SELECT * FROM borrows WHERE user_id = %s AND bookno = %s", (user_id, bookid))
        borrow = cursor.fetchone()
        print(borrow)
        if borrow != None:
            cursor.execute("UPDATE borrows SET borrow_date = %s WHERE user_id = %s AND bookno = %s", (today, user_id, bookid))
            connection.commit()
            print("Book renewed successfully")
            user()
        else:
            print("Book not borrowed")
            user()

    def fine_status():
        cursor.execute("SELECT id FROM users WHERE username = %s", (login.username,))
        user_id = cursor.fetchone()[0]
        print("Fine Status")
        cursor.execute("SELECT * FROM borrows WHERE user_id = %s AND borrow_date < CURRENT_DATE - INTERVAL 28 DAY", (user_id,))
        fines = cursor.fetchall()
        if len(fines) == 0:
            print("You have no fine")
        else:
            print("You have fine for the following books")
            for fine in fines:
               print(fine)
            user()
            print("Pay Fine in Accounts Block")
        user()

    def logout():
        print("Logout")
        connection.close()



# user()