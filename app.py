import os
from flask import Flask, render_template, redirect, request, url_for, session, flash
import db_users

app = Flask(__name__)
app.secret_key = "fhkjashgdfkhakjdfgkjasdgf"

@app.route('/')
def index():
    # If user is logged in, logout button will be displayed
    if 'username' in session:
        username = session['username']
    else:
        username = None
    return render_template('index.html', username=username)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # If entered data exist in DB, user will be logged in and username saved to session storage, else error message is displayed
        login_data = db_users.check_username_password(username, password)
        print(login_data)
        if login_data:
            print('Login successfull')
            session['username'] = request.form['username']
            flash('Welcome back!')  
            return redirect(url_for('account'))
        else:
            print('Not successful')
            error_wrong_username_password = 'Wrong username or password, please try again'
            return render_template('login.html', message=error_wrong_username_password)
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first = request.form['first_name'].title()
        last = request.form['last_name'].title()
        username = request.form['username']
        password = request.form['password']
        # Check DB if username is availible
        username_availible = db_users.check_username_dont_exists(username)
        print(username_availible)
        if username_availible:
            # User data added to DB, user redirected to account page, username saved to session storage
            db_users.add_new_user_to_db(first, last, username, password)
            print('Registration successfull')
            session['username'] = request.form['username']
            flash('Welcome to your new account!')
            return redirect(url_for('account'))
        else:
            print('Username taken, please choose a new one')
            # Display error message if username already taken
            error_username_taken = 'Username is already taken, please choose a new one'
            return render_template('register.html', message=error_username_taken)
    return render_template('register.html')

@app.route('/account')
def account():
    username = session['username']
    return render_template('account.html', username=username)

@app.route('/logout')
def logout():
    # Remove username from session storage and redirect
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT', 5000)),
            debug=True)