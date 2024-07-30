# import conn 
# import hashlib

# cursor = conn.connect()

# def login():
#     print("Welcome to Advanced Library System")
#     print("Login to your account")
#     username = input("Enter your username: ")
#     password = input("Enter your password: ")
#     cursor.execute("SELECT user_level FROM users where username = %s and password = %s", (username, hashlib.sha1(password.encode()).hexdigest()))
#     if cursor.rowcount > 0:
#         print("Login successful")
#         # level = cursor.fetchone()[0]
#         # if level == 1:
#         #     print("Welcome Admin")
#         print("Welcome " + username)
#     else:
#         print("Login failed")
#         print("Please try again")
#         login()


# login()

import conn
import hashlib
# import admin
# import user

connection = conn.connect()



if connection.is_connected():
    cursor = connection.cursor()

    def login():
        global log
        global username

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
        #     if log!= None:
        #         user_level = log[0]
        #         if user_level == 1:
        #            print("------------------------------------------------------")
        #            print("        Welcome to Advanced Library System")
        #            print("------------------------------------------------------")
        #            print("Welcome Admin")
        #            admin.admin()

        #         elif user_level == 2:
        #            print("Welcome to Advanced Library System")
        #            print("Welcome User")
        #            user.user()
            # else:
            #     print("Login failed")
            #     print("Please try again")
            #     login()
            # return log
        else:
            print("Login failed")
            print("Please try again")
            login()

    # login()

    # cursor.close()
    # connection.close()
else:
    print("Failed to connect to the database.")

