import login
import admin
import user

from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)

app.secret_key = '6268121321'


@app.route('/')
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
            # print("------------------------------------------------------")
            # print("        Welcome to Advanced Library System")
            # print("------------------------------------------------------")
            # print("Welcome Admin")
            return redirect(url_for('admin.html'))

        elif user_level == 2:
            # print("Welcome to Advanced Library System")
            # print("Welcome User")
            return redirect(url_for('user.html'))
    else:
        print("Login failed")
        print("Please try again")
        main()


        
    return render_template('index.html')

def home():
    if 'username' in session:
        return render_template('index.html')
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(debug=True)