import conn
import hashlib

connection = conn.connect()
cursor = connection.cursor()

print("Welcome to Advanced Library System")
print("Login to your account")
username = input("Enter your username: ")
password = input("Enter your password: ")
hashed_password = hashlib.sha1(password.encode()).hexdigest()
print(hashed_password)
cursor.execute("SELECT * FROM users where username = %s and password = %s", (username, hashed_password))
cursor.fetchone()
if cursor.rowcount > 0:
    print("Login successful")
    print("Welcome " + username)
print(cursor.rowcount)
myresult = cursor.fetchone()

for x in myresult:
  print(x)
    
        