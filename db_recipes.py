from cnxn import db_query, db_query_many

# Get title and image of all recipes
def recipe_short():
    data = db_query("""SELECT data_Recipe.recipe_id, title, description, image, type_of_food, minutes FROM data_Recipe 
                    INNER JOIN data_Type ON data_Recipe.type_id = data_Type.type_id 
                    INNER JOIN data_Time ON data_Recipe.time_id = data_Time.time_id ;""")
    return data

# Get recipe details
def recipe_details_description(recipe_id):
    data = db_query("""SELECT recipe_id, title, description, steps, creation_date, image, 
                    type_of_food, servings, minutes, username FROM data_Recipe 
                    INNER JOIN data_Type ON data_Recipe.type_id = data_Type.type_id 
                    INNER JOIN data_Servings ON data_Recipe.servings_id = data_Servings.servings_id 
                    INNER JOIN data_Time ON data_Recipe.time_id = data_Time.time_id 
                    INNER JOIN data_User ON data_Recipe.user_id = data_User.user_id 
                    WHERE recipe_id=?;""", recipe_id)
    return data


def recipe_ingredients(recipe_id):
    ingredients = db_query("""SELECT recipe_id, quantity, unit, ingredient FROM data_ingredients 
                            INNER JOIN dft_Quantity ON data_Ingredients.quantity_id = dft_Quantity.quantity_id 
                            INNER JOIN dft_Units ON data_Ingredients.unit_id = dft_Units.unit_id 
                            INNER JOIN dft_Ingredients ON data_Ingredients.ingredient_id = dft_Ingredients.ingredient_id 
                            WHERE recipe_id=?;""", recipe_id)
    return ingredients

    
# Get data for dropdown fields
def get_types_servings_time():
    data = db_query_many(("SELECT type_id, type_of_food FROM data_Type AS table_types;"), 
                    ("SELECT servings_id, servings FROM data_Servings AS table_servings;"), 
                    ("SELECT time_id, minutes FROM data_Time AS table_time;"))
    return data
