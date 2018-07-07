import os
from flask import Flask, render_template, redirect, request, url_for, session, flash
from validate import RegistrationForm
import fractions
from natsort import natsorted
from operator import itemgetter
from datetime import datetime
import uuid
import db_users
import db_recipes
import db_recipe_add

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
    
    # Create random recipe_id
    recipe_id = uuid.uuid4()

    # Get data for dropdown selection from DB, sort numerical values
    types = db_recipes.get_food_types()
    servings_data = db_recipes.get_number_of_servings()
    servings = []
    for entry in natsorted(servings_data, key=itemgetter(1), reverse=False):
        servings.append(entry)
    minutes_data = db_recipes.get_preparation_time()
    minutes = []
    for entry in natsorted(minutes_data, key=itemgetter(1), reverse=False):
        minutes.append(entry)
    if request.method == 'POST':
        """ Get data from form """
        
    # Get all ingredients data from form - list of sorted tuples
        quantities = request.form.getlist('quantity[]')
        quantities.append(request.form['quantity'])
        q_list = []
        for q in quantities:
            q2 = q.replace(",", ".")
            q3 = float(q2)
            q_list.append(q3)
        units = request.form.getlist('unit[]')
        units.append(request.form['unit'])
        ingredients = request.form.getlist('ingredient[]')
        ingredients.append(request.form['ingredient'])
        
        input_data = zip(q_list, units, ingredients)
        formatted_input_data = list(input_data)
        print(formatted_input_data)
    # Check if ingredients data exists in DB
        for entry in formatted_input_data:
            quantity = entry[0]
            unit = entry[1]
            ingredient = entry[2]
            q_data = db_recipe_add.check_if_quantity_in_db(quantity)
            u_data = db_recipe_add.check_if_unit_in_db(unit)
            i_data = db_recipe_add.check_if_ingredient_in_db(ingredient)
            print(q_data, u_data, i_data)
            
        ### 3 lists: quantity_ids, unit_ids and ingredient_ids; zip them and add each tuple + recipe_id to data_Ingredients
        # If ingredients data exists, get their ID, else create them and add new record to each dft_table
            quantity_ids = []
            if q_data:
                q_id_data = db_recipe_add.get_quantity_id(quantity)
                for data in q_id_data:
                    quantity_id = data.quantity_id
                    quantity_ids.append(quantity_id)
            else:
                quantity_id = uuid.uuid4()
                quantity_ids.append(quantity_id)
                db_recipe_add.add_new_quantity(quantity_id, quantity)
                
            unit_ids = []
            if u_data:
                u_id_data = db_recipe_add.get_unit_id(unit)
                for data in u_id_data:
                    unit_id = data.unit_id
                    unit_ids.append(unit_id)
            else:
                unit_id = uuid.uuid4()
                unit_ids.append(unit_id)
                db_recipe_add.add_new_unit(unit_id, unit)
                
            ingredient_ids = []
            if i_data:
                i_id_data = db_recipe_add.get_ingredient_id(ingredient)
                for data in i_id_data:
                    ingredient_id = data.ingredient_id
                    ingredient_ids.append(ingredient_id)
            else:
                ingredient_id = uuid.uuid4()
                ingredient_ids.append(ingredient_id)
                db_recipe_add.add_new_ingredient(ingredient_id, ingredient)
            
            # Zip lists and add add records to data_Ingredients
            for i,u,q in zip(ingredient_ids, unit_ids, quantity_ids):
                db_recipe_add.add_new_ingredient_to_db(i, u, q, recipe_id)
            
            # zipped_ingredients = zip(ingredient_ids, unit_ids, quantity_ids)
            # list_ingredients = list(zipped_ingredients)
            # for i, u, q in zipped_ingredients:
            #     db_recipe_add.add_new_ingredient_to_db(i.ingredient_id, u.unit_id, q.quantity_id, recipe_id)
    
    
    # Get IDs of selected dropdown data, converted to UUIDs
        type_selected = uuid.UUID(request.form.get('type_option'))
        servings_selected = uuid.UUID(request.form.get('servings_option'))
        minutes_selected = uuid.UUID(request.form.get('minutes_option'))
        
    # Get all other recipe data
        title = request.form['title']
        description = request.form['description']
        image = request.form['image']
        steps = request.form['steps']

    # Get user_id converted to UUID, creation_date
        user_id = uuid.UUID(session['user_id'])
        creation_date = datetime.now()

    # Add data to data_Recipe and redirect to details page
        db_recipe_add.add_new_recipe_to_db(recipe_id, title, description, steps, creation_date, image, user_id, type_selected, servings_selected, minutes_selected)
        return redirect(url_for('recipe_details', recipe_id=recipe_id))
    
    return render_template('recipe_add.html', username=username, types=types, n_servings=servings, n_minutes=minutes)

@app.route('/recipes')
def recipes():
    if 'username' in session:
        username = session['username']
    else:
        username = None
    # Get basic info for all recipes
    recipes = db_recipes.recipe_short()
    for entry in recipes:
        description = entry.description.split("\r")
    return render_template('recipes.html', username=username, recipes=recipes, description=description)

@app.route('/recipes/details/<recipe_id>')
def recipe_details(recipe_id):
    if 'username' in session:
        username = session['username']
    else:
        username = None
    # Get all recipe data except ingredients
    data = db_recipes.recipe_details_description(recipe_id)
    # Split description into steps
    for entry in data:
        f_steps = entry.steps.split("\r")
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