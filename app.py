import os
from flask import Flask, render_template, redirect, request, url_for, session, flash
from validate import RegistrationForm
import fractions
from datetime import datetime
import re
import uuid
import helpers
import db_users
import db_recipes
import db_recipe_add

app = Flask(__name__)
app.secret_key = "fhkjashgdfkhakjdfgkjasdgf"

@app.route('/')
def index():
    # If user is logged in, logout button will be displayed
    username = helpers.username_set_or_none()
    return render_template('index.html', username=username)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        # If entered data exist in DB, user will be logged in else error message is displayed
        login_data = db_users.check_username_password(username, password)
        print(login_data)
        if login_data:
            # get user_id from DB, save user_id and username to session storage,
            print('Login successfull')
            session['username'] = request.form['username']
            id_data = db_users.get_user_id(username)
            for entry in id_data:
                session['user_id'] = entry.user_id
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
        first = form.first.data.strip().title()
        last = form.last.data.strip().title()
        username = form.username.data.strip()
        password = form.password.data.strip()
        # Check if name contains only alpha characters
        if first.isalpha() and last.isalpha():
            # Check DB if username is availible
            username_availible = db_users.check_username_dont_exists(username)
            print(username_availible)
            if username_availible:
                # User data added to DB, user_id and username saved to session storage
                db_users.add_new_user_to_db(first, last, username, password)
                print('Registration successfull')
                session['username'] = form.username.data
                id_data = db_users.get_user_id(username)
                for entry in id_data:
                    session['user_id'] = entry.user_id
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
    data = db_recipes.get_types_servings_time()
    types = data[0]
    servings = []
    minutes = []
    helpers.sort_numbers(data[1], servings)
    helpers.sort_numbers(data[2], minutes)
    
    return render_template('recipe_add.html', username=username, types=types, n_servings=servings, n_minutes=minutes)

@app.route('/account/addrecipe/check_data', methods=['GET', 'POST'])
def get_check_data():
    if request.method == 'POST':
    # Create random recipe_id, get user_id converted to UUID, other data
        recipe_id = uuid.uuid4()
        user_id = uuid.UUID(session['user_id'])
        creation_date = datetime.now()
        title = helpers.remove_whitespaces(request.form['title']).strip().title()
        description = request.form['description']
        image = request.form['image'].strip()
        steps = request.form['steps']
        
    # Get IDs of selected dropdown data, converted to UUIDs
        type_id = uuid.UUID(request.form.get('type_option'))
        servings_id = uuid.UUID(request.form.get('servings_option'))
        time_id = uuid.UUID(request.form.get('minutes_option'))

    # Get all ingredients data from form
        quantities = request.form.getlist('quantity[]')
        quantities.append(request.form['quantity'])
        units = request.form.getlist('unit[]')
        units.append(request.form['unit'])
        ingredients = request.form.getlist('ingredient[]')
        ingredients.append(request.form['ingredient'])

        # IDs for entered data
        quantity_ids = []
        unit_ids = []
        ingredient_ids = []
    # Check type and format quantity, check if ingredients data exists in DB
        for q in quantities:
            q2 = q.replace(",", ".")
            if helpers.isFloat(q2):
                q = float(q2)
            else:
                q = float('0')
            q_data = db_recipe_add.check_if_quantity_in_db(q)
        # If quantity data exists in DB, get their ID, else create it and add new record to dft_tablee
            if q_data:
                q_id_data = db_recipe_add.get_quantity_id(q)
                for data in q_id_data:
                    q_id = data.quantity_id
                    quantity_ids.append(q_id)
            else:
                q_id = uuid.uuid4()
                quantity_ids.append(q_id)
                db_recipe_add.add_new_quantity(q_id, q)
    # If units data exists in DB, get their ID, else create it and add new record to dft_table
        for u in units:
            u = u.strip().lower()
            u_data = db_recipe_add.check_if_unit_in_db(u)
            print(u_data)
            if u_data:
                u_id_data = db_recipe_add.get_unit_id(u)
                for data in u_id_data:
                    u_id = data.unit_id
                    unit_ids.append(u_id)
            else:
                u_id = uuid.uuid4()
                unit_ids.append(u_id)
                db_recipe_add.add_new_unit(u_id, u)
    # If ingredients data exists in DB, get their ID, else create it and add new record to dft_table
        for i in ingredients:
            i = i.strip().lower()
            i_data = db_recipe_add.check_if_ingredient_in_db(i)
            print(i_data)
            if i_data:
                i_id_data = db_recipe_add.get_ingredient_id(i)
                for data in i_id_data:
                    i_id = data.ingredient_id
                    ingredient_ids.append(i_id)
            else:
                i_id = uuid.uuid4()
                ingredient_ids.append(i_id)
                db_recipe_add.add_new_ingredient(i_id, i)


    # Merge lists with IDs and add each group + recipe_id to data_Ingredients
        for i,u,q in zip(ingredient_ids, unit_ids, quantity_ids):
                db_recipe_add.add_new_ingredient_to_db(i, u, q, recipe_id)
    
    # Add data to data_Recipe and redirect to details page
        db_recipe_add.add_new_recipe_to_db(recipe_id, title, description, steps, creation_date, image, user_id, type_id, servings_id, time_id)


        return redirect(url_for('recipe_details', recipe_id=recipe_id))

    return


@app.route('/recipes')
def recipes():
    username = helpers.username_set_or_none()
    
    # Get basic info for all recipes
    data = db_recipes.recipe_short()
    for entry in data:
        entry.description = entry.description.split("\r")
    return render_template('recipes.html', username=username, data=data)

@app.route('/recipes/details/<recipe_id>')
def recipe_details(recipe_id):  
    username = helpers.username_set_or_none()
    # Get all recipe data except ingredients
    data = db_recipes.recipe_details_description(recipe_id)
    # Split description into steps
    for entry in data:
        f_steps = re.split(': |\r|\n', entry.steps)
        entry.steps = f_steps
        f_description = entry.description.split("\r")
        entry.description = f_description
    # Get ingredients for recipe, format floats
    ingredients_data = db_recipes.recipe_ingredients(recipe_id)
    for entry in ingredients_data:
        f_quantity = ('{}'.format(round(fractions.Fraction(entry.quantity), 1)))
        entry.quantity = f_quantity

    return render_template('recipe_details.html', username=username, data=data, ingredients=ingredients_data)

@app.route('/logout')
def logout():
    # Remove username from session storage and redirect
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT', 5000)),
            debug=True)