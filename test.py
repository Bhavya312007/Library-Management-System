import conn
import hashlib

connection = conn.connect()
cursor = connection.cursor()

print("Welcome to Advanced Library System")
print("Login to your account")
# username = input("Enter your username: ")
# password = input("Enter your password: ")
username = "user"
password = "user"
hashed_password = hashlib.sha1(password.encode()).hexdigest()
# print(hashed_password)
cursor.execute("SELECT user_level FROM users WHERE username = %s AND password = %s", (username, hashed_password))
myresult =cursor.fetchone()
# if cursor.rowcount > 0:
#     print("Login successful")
#     print("Welcome " + username)
# print(cursor.rowcount)
# sql = "SELECT * FROM users where username = %s and password = %s",
# cursor.execute(sql, (username, hashed_password))
# myresult = cursor.fetchall(sql)
# for x in myresult:
#   print(x)
print(myresult)

if myresult[0] == 1:
    print("Welcome Admin")
else:
    print("Welcome " + username)
        