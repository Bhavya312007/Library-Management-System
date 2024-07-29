import conn2
import hashlib

def main():
    connection = conn2.connect_to_database()

    if connection is not None:
        cursor = connection.cursor()

        def login():
            print("Welcome to Advanced Library System")
            print("Login to your account")
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            hashed_password = hashlib.sha1(password.encode()).hexdigest()
            cursor.execute("SELECT user_level FROM users WHERE username = %s AND password = %s", (username, hashed_password))
            if cursor.rowcount > 0:
                print("Login successful")
                print("Welcome " + username)
            else:
                print("Login failed")
                print("Please try again")
                login()

        login()

        cursor.close()
        connection.close()
    else:
        print("Failed to connect to the database.")

if __name__ == "__main__":
    main()
