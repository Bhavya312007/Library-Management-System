import login
conn= login.conn

def main():
    log= login()
    if log==1:
        print("Welcome to Advanced Library System")
        print("Welcome Admin")

    elif log==3:
        print("Welcome to Advanced Library System")
        print("Welcome User")
    else:
        print("Login failed")
        print("Please try again")
        main()
main()