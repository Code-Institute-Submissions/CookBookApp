import os
from flask import Flask, render_template, redirect, request, url_for, session, flash
from validate import RegistrationForm
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
            return render_template('login.html', error_message=error_wrong_username_password)
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    # Check if fields are valid with validate() method
    if request.method == 'POST' and form.validate():
        first = form.first.data.title()
        last = form.last.data.title()
        username = form.username.data
        password = form.password.data
        # Check if name contains only alpha characters
        if first.isalpha() and last.isalpha():
            # Check DB if username is availible
            username_availible = db_users.check_username_dont_exists(username)
            print(username_availible)
            if username_availible:
                # User data added to DB, user redirected to account page, username saved to session storage
                db_users.add_new_user_to_db(first, last, username, password)
                print('Registration successfull')
                session['username'] = form.username.data
                flash('Welcome to your new account!')
                return redirect(url_for('account'))
            else:
                print('Username taken, please choose a new one')
                # Display error message if username already taken
                error_username_taken = 'Username is already taken, please choose a new one'
                return render_template('register.html', form=form, error_message=error_username_taken)
        else:
            # Error message if name contains anything else than alpha characters
            error_wrong_name = 'Please enter your name'
            return render_template('register.html', form=form, error_message=error_wrong_name)
    return render_template('register.html', form=form)

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