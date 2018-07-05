import os
from flask import Flask, render_template, redirect, request, url_for, session, flash
from validate import RegistrationForm
import fractions
from natsort import natsorted
from operator import itemgetter
import db_users
import db_read

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
    # Fix error when trying to access account page from url
    if 'username' in session:
        username = session['username']
    else:
        return redirect(url_for('index'))
    return render_template('account.html', username=username)

@app.route('/account/addrecipe', methods=['GET', 'POST'])
def add_recipe():
    # Redirect when trying to access add recipe page from url
    if 'username' in session:
        username = session['username']
    else:
        return redirect(url_for('login'))
    # Get data for dropdown selection from DB, sort numerical values
    types = db_read.get_food_types()
    servings_data = db_read.get_number_of_servings()
    servings = []
    for entry in natsorted(servings_data, key=itemgetter(1), reverse=False):
        servings.append(entry)
    minutes_data = db_read.get_preparation_time()
    minutes = []
    for entry in natsorted(minutes_data, key=itemgetter(1), reverse=False):
        minutes.append(entry)
    # Get all ingredients data from form
    if request.method == 'POST':
        quantities = request.form.getlist('quantity[]')
        if quantities:
            quantities.insert(0, request.form['quantity'])
        units = request.form.getlist('unit[]')
        if units:
            units.insert(0, request.form['unit'])
        ingredients = request.form.getlist('ingredient[]')
        if ingredients:
            ingredients.insert(0, request.form['ingredient'])
        input_data = zip(quantities, units, ingredients)
        sorted_input_data = list(input_data)
        print(sorted_input_data)
        # Get ID of new recipe and open that page with recipe details
        #return redirect(url_for('recipe_details', recipe_id=recipe_id))
    
    return render_template('recipe_add.html', username=username, types=types, n_servings=servings, n_minutes=minutes)

@app.route('/recipes')
def recipes():
    recipes = db_read.recipe_short()
    for entry in recipes:
        description = entry.description.split("\r")
    return render_template('recipes.html', recipes=recipes, description=description)

@app.route('/recipes/details/<recipe_id>')
def recipe_details(recipe_id):
    # Get all recipe data except ingredients
    data = db_read.recipe_details_description(recipe_id)
    # Split description into steps
    for entry in data:
        steps = entry.steps.split("\r")
        description = entry.description.split("\r")
    # Get ingredients for recipe, format floats
    ingredients_data = db_read.recipe_ingredients(recipe_id)
    for entry in ingredients_data:
        formatted_quantity = ('{} = {}'.format(entry.quantity, fractions.Fraction(entry.quantity)))
        entry.quantity = formatted_quantity[6:]
    return render_template('recipe_details.html', data=data, steps=steps, description=description, ingredients=ingredients_data)

@app.route('/logout')
def logout():
    # Remove username from session storage and redirect
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT', 5000)),
            debug=True)