import os
from flask import Flask, render_template, redirect, request, url_for, session
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
        # If entered data exist in DB, user will be logged in and username saved to session storage
        login_data = db_users.check_username_password(username, password)
        print(login_data)
        if login_data:
            print('Login successfull')
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            print('Not successful')
            return render_template('login.html')
    return render_template('login.html')


@app.route('/logout')
def logout():
    # Remove username from session storage and redirect
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT', 5000)),
            debug=True)