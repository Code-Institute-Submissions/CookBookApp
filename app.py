import os
from flask import Flask, render_template, redirect, request, url_for, session, flash
from validate import RegistrationForm
import fractions
from datetime import datetime
import re
import uuid
import helpers
import check_ingr_data
import db_users
import db_recipes
import db_recipe_add
import db_recipe_edit
import db_recipe_search

app = Flask(__name__)
app.secret_key = "fhkjashgdfkhakjdfgkjasdgf"

@app.route('/')
def index():
    # If user is logged in, logout button will be displayed
    username = helpers.username_set_or_none()
    
    # Get all types of food
    data_types = db_recipes.get_all_types()
    categories = []
    for entry in data_types:
        categories.append(entry[1])
    
    # Get one recipe for each category
    data = []
    for category in categories:
        data.append(db_recipes.get_one_in_each_category(category))
    
    return render_template('index.html', username=username, data=data)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        # If entered data exist in DB, user will be logged in else error message is displayed
        login_data = db_users.check_username_password(username, password)
        if login_data:
            # get user_id from DB, save user_id and username to session storage,
            session['username'] = request.form['username']
            session['user_id'] = helpers.user_id_for_session(username)
            flash('Welcome back!')  
            return redirect(url_for('account'))
        else:
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
            if username_availible:
                # User data added to DB, user_id and username saved to session storage
                db_users.add_new_user_to_db(first, last, username, password)
                session['username'] = form.username.data
                session['user_id'] = helpers.user_id_for_session(username)
                flash('Welcome to your new account!')
                return redirect(url_for('account'))
            else:
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
        return redirect(url_for('login'))
    
    # Get all recipes from user
    data = db_recipes.recipes_from_user(username)
    
    return render_template('account.html', username=username, data=data)

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
        description = request.form['description'].strip()
        image = request.form['image'].strip()
        steps = request.form['steps'].strip()
        
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
        
    # Check data, get IDs, add to DB if not there, ... return list of IDs
        quantity_ids = check_ingr_data.check_data_quantities(quantities)
        unit_ids = check_ingr_data.check_data_units(units)
        ingredient_ids = check_ingr_data.check_data_ingredients(ingredients)

    # Merge lists with IDs and add each group + recipe_id to data_Ingredients
        for i,u,q in zip(ingredient_ids, unit_ids, quantity_ids):
                db_recipe_add.add_new_ingredient_to_db(i, u, q, recipe_id)
    
    # Add data to data_Recipe and redirect to details page
        db_recipe_add.add_new_recipe_to_db(recipe_id, title, description, steps, creation_date, image, user_id, type_id, servings_id, time_id)


        return redirect(url_for('recipe_details', recipe_id=recipe_id))

    return

@app.route('/account/editrecipe/<recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
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
    
    # Get all recipe data from DB, format quantity
    rec_data = db_recipe_edit.recipe_details_description(recipe_id)
    ing_data = db_recipe_edit.recipe_ingredients(recipe_id)
    for entry in ing_data:
        f_quantity = ('{}'.format(round(fractions.Fraction(entry.quantity), 1)))
        entry.quantity = f_quantity
    
    return render_template('recipe_edit.html', username=username, recipe_id=recipe_id, rec_data=rec_data, ing_data=ing_data, types=types, n_servings=servings, n_minutes=minutes)

@app.route('/account/editrecipe/check_data/<recipe_id>', methods=['GET', 'POST'])
def compare_data(recipe_id):
    if request.method == 'POST':
        recipe_id = uuid.UUID(recipe_id)
    # Get updated data from form
        title = request.form['title'].strip().title()
        description = request.form['description'].strip()
        image = request.form['image'].strip()
        steps = request.form['steps'].strip()
        type_id = uuid.UUID(request.form.get('type_option'))
        servings_id = uuid.UUID(request.form.get('servings_option'))
        time_id = uuid.UUID(request.form.get('minutes_option'))
    
    # Get checked ingredients IDs for delete, delete row in data_Ingredients
        i_del_ids = request.form.getlist('old-ingredient[]')
        for i in i_del_ids:
            db_recipe_edit.delete_row_ingredient_data(i)
    
    # Get new ingredients data from form
        quantities = request.form.getlist('quantity[]')
        if request.form['quantity'] != "":
            quantities.append(request.form['quantity'])
        units = request.form.getlist('unit[]')
        if request.form['unit'] != "":
            units.append(request.form['unit'])
        ingredients = request.form.getlist('ingredient[]')
        if request.form['ingredient'] != "":
            ingredients.append(request.form['ingredient'])
        
    # Check new data, get IDs, add to DB if not there, ... return list of IDs
        quantity_ids = check_ingr_data.check_data_quantities(quantities)
        unit_ids = check_ingr_data.check_data_units(units)
        ingredient_ids = check_ingr_data.check_data_ingredients(ingredients)
        
    # Merge lists with IDs and add each group + recipe_id to data_Ingredients
        for i,u,q in zip(ingredient_ids, unit_ids, quantity_ids):
                db_recipe_add.add_new_ingredient_to_db(i, u, q, recipe_id)
    
    # Update data_Recipe
        db_recipe_edit.update_recipe_data(recipe_id, title, description, steps, image, type_id, servings_id, time_id)

    return redirect(url_for('recipe_details', recipe_id=recipe_id))

@app.route('/recipes')
def recipes():
    username = helpers.username_set_or_none()
    
    # Get basic info for all recipes
    data = db_recipes.recipe_short()
    for entry in data:
        entry.description = entry.description.split("\r")
    return render_template('recipes.html', username=username, data=data)

@app.route('/recipes/search', defaults={'category': ''}, methods=['GET', 'POST'])
@app.route('/recipes/search/<category>', methods=['GET', 'POST'])
def search_recipes(category):
    username = helpers.username_set_or_none()
    data_types = db_recipe_search.get_types()
    data = []
    keyw_title = ""
    type_id = ""
    ingred = ""
    type_name = ""
    
    if request.method == 'GET':
        type_name = category
        print(type_name)
        # Get type ID from name
        get_type_id = db_recipe_search.get_type_id(type_name)
        for entry in get_type_id:
            type_id = entry[0]
        # Get recipe IDs for selected type
        r_ids = []
        for r_id in db_recipe_search.get_search_types(type_id):
            r_ids.append(r_id[0])
        # Get recipe data for IDs
        data = []
        for r_id in r_ids:
            data.append(db_recipe_search.recipe_short(r_id)[0])
        # Format decription for display
        for entry in data:
            entry.description = entry.description.split("\r")

    if request.method == 'POST':
        data = []
        r_ids = []
        # Get recipe IDs for title keyword
        if request.form['keyw-title'] != "":
            keyw_title = request.form['keyw-title'].strip().title()
            for r_id in db_recipe_search.get_search_titles(keyw_title):
                r_ids.append(r_id[0])
        # Get recipe IDs for selected type
        if request.form.get('type_option') != "":
            type_id = request.form.get('type_option')
            # Get type name from ID
            for entry in data_types:
                if entry[0] == type_id:
                    type_name = entry[1]
            for r_id in db_recipe_search.get_search_types(type_id):
                r_ids.append(r_id[0])
        # Get recipe IDs for selected ingredient
        if request.form['keyw-ingr'] != "":
            ingred = request.form['keyw-ingr'].strip().lower()
            for r_id in db_recipe_search.get_search_ingredient(ingred):
                r_ids.append(r_id[0])
        
        # Remove duplicate IDs
        rec_ids = helpers.remove_duplicates(r_ids)
        # Get recipe data for IDs
        for r_id in rec_ids:
            data.append(db_recipe_search.recipe_short(r_id)[0])
        
        # Format decription for display
        for entry in data:
            entry.description = entry.description.split("\r")

    return render_template('recipe_search.html', username=username, types=data_types, data=data, keyw_title=keyw_title, sel_type_id=type_id, sel_type_name=type_name, keyw_ingr=ingred)

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

    return render_template('recipe_details.html', username=username, recipe_id=recipe_id, data=data, ingredients=ingredients_data)

@app.route('/logout')
def logout():
    # Remove username and user_id from session storage and redirect
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT', 5000)),
            debug=True)