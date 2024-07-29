import conn 
import hashlib

cursor = conn.connect()

def login():
    print("Welcome to Advanced Library System")
    print("Login to your account")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    cursor.execute("SELECT user_level FROM users where username = %s and password = %s", (username, hashlib.sha1(password.encode()).hexdigest()))
    if cursor.rowcount > 0:
        print("Login successful")
        level = cursor.fetchone()[0]
        if level == 1:
            print("Welcome Admin")
        print("Welcome " + username)
    else:
        print("Login failed")
        print("Please try again")
        login()


login()

