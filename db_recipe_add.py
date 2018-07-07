from cnxn import db_query, db_write

# Add data from form to data_Recipe
def add_new_recipe_to_db(recipe_id, title, description, steps, creation_date, image, user_id, type_selected, servings_selected, minutes_selected):
    db_write("""INSERT INTO data_Recipe(recipe_id, title, description, steps, creation_date, image, user_id, type_id, servings_id, time_id) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""", recipe_id, title, description, steps, creation_date, image, user_id, type_selected, servings_selected, minutes_selected)
    return


# Check if ingredient, unit and quantity exists in DB
def check_if_ingredient_in_db(ingredient):
    data = db_query("SELECT ingredient_id FROM dft_Ingredients WHERE ingredient=?;", ingredient)
    return True if data else False

def check_if_unit_in_db(unit):
    data = db_query("SELECT unit_id FROM dft_Units WHERE unit=?;", unit)
    return True if data else False

def check_if_quantity_in_db(quantity):
    data = db_query("SELECT quantity_id FROM dft_Quantity WHERE quantity=?;", quantity)
    return True if data else False


# Get ID of ingredient, unit, quantity
def get_ingredient_id(ingredient):
    data = db_query("SELECT ingredient_id FROM dft_Ingredients WHERE ingredient=?;", ingredient)
    return data

def get_unit_id(unit):
    data = db_query("SELECT unit_id FROM dft_Units WHERE unit=?;", unit)
    return data

def get_quantity_id(quantity):
    data = db_query("SELECT quantity_id FROM dft_Quantity WHERE quantity=?;", quantity)
    return data


# Add data to dft_Tables
def add_new_ingredient(ingredient_id, ingredient):
    db_write("INSERT INTO dft_Ingredients(ingredient_id, ingredient) VALUES (?, ?);", ingredient_id, ingredient)
    return

def add_new_unit(unit_id, unit):
    db_write("INSERT INTO dft_Units(unit_id, unit) VALUES (?, ?);", unit_id, unit)
    return

def add_new_quantity(quantity_id, quantity):
    db_write("INSERT INTO dft_Quantity(quantity_id, quantity) VALUES (?, ?);", quantity_id, quantity)
    return

# Add data to data_Ingredients
def add_new_ingredient_to_db(ingredient_id, unit_id, quantity_id, recipe_id):
    db_write("""INSERT INTO data_Ingredients(ingredient_id, unit_id, quantity_id, recipe_id) 
                VALUES (?, ?, ?, ?);""", ingredient_id, unit_id, quantity_id, recipe_id)
    return