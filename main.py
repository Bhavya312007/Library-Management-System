import login
import admin
import user

def main():
  while True:
    login.login()

    log= login.log
    print(log)
    if log!= None:
        user_level = log[0]
        print(user_level)
        print(log)
        if user_level == 1:
            print("------------------------------------------------------")
            print("        Welcome to Advanced Library System")
            print("------------------------------------------------------")
            print("Welcome Admin")
            admin.admin()

        elif user_level == 2:
            print("Welcome to Advanced Library System")
            print("Welcome User")
            user.user()
    else:
        print("Login failed")
        print("Please try again")
        main()
main()