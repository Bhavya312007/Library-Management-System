import conn
import hashlib


connection = conn.connect()

global username
global password

if connection.is_connected():
    cursor = connection.cursor()

    def login():
        global log
        
        global username
        global password

        print("Welcome to Advanced Library System")
        print("Login to your account")
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        hashed_password = hashlib.sha1(password.encode()).hexdigest()
        print(hashed_password)
        cursor.execute("SELECT user_level FROM users WHERE username = %s AND password = %s", (username, hashed_password))
        log= cursor.fetchone()
        print(cursor.rowcount)
        print(log)
        if cursor.rowcount > 0:
            print("Login successful")
            print("Welcome " + username)
            return username
        else:
            print("Login failed")
            print("Please try again")
            login()
else:
    print("Failed to connect to the database.")

