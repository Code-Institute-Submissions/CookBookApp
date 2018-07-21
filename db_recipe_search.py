from cnxn import db_query

# Get types data for dropdown
def get_types():
    data = db_query("SELECT type_id, type_of_food FROM data_Type;")
    return data

# Get recipe IDs for search results
def get_search_titles(keyword):
    data = db_query("""SELECT recipe_id from data_Recipe 
                    WHERE title LIKE ?;""", ("%{}%".format(keyword)))
    return data
    
def get_search_types(type_id):
    data = db_query("SELECT recipe_id from data_Recipe WHERE type_id=?;", type_id)
    return data

def get_search_ingredient(ingred):
    data = db_query("""SELECT recipe_id from data_Ingredients 
                    INNER JOIN dft_Ingredients ON data_Ingredients.ingredient_id = dft_Ingredients.ingredient_id 
                    WHERE dft_Ingredients.ingredient LIKE ?;""", ("%{}%".format(ingred)))
    return data

# Get short description for recipe IDs
def recipe_short(recipe_id):
    data = db_query("""SELECT data_Recipe.recipe_id, title, description, image, type_of_food, minutes FROM data_Recipe 
                    INNER JOIN data_Type ON data_Recipe.type_id = data_Type.type_id 
                    INNER JOIN data_Time ON data_Recipe.time_id = data_Time.time_id 
                    WHERE data_recipe.recipe_id=?;""", recipe_id)
    return data
