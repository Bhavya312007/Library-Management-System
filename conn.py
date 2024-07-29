import mysql.connector
from mysql.connector import Error

def connect(host='localhost', user='root', password='', database='library'):
    try:
        connection = mysql.connector.connect(host=host,
                                             user=user,
                                             password=password,
                                             database=database)
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            return connection

    except Error as e:
       print("Error while connecting to MySQL", e)

# connect()