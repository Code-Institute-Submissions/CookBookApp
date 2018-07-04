import os
from flask import Flask, render_template, redirect, request, url_for, session
from cnxn import db_query

app = Flask(__name__)
app.secret_key = "fhkjashgdfkhakjdfgkjasdgf"

@app.route('/')
def home_page():
    data = db_query('SELECT recipe_id, title FROM data_Recipe;')
    return render_template('index.html', data=data)
    
    
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT', 5000)),
            debug=True)