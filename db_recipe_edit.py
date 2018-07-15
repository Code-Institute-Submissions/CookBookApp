from cnxn import db_query, db_write

# Get data from data_Recipe
def recipe_details_description(recipe_id):
    data = db_query("""SELECT recipe_id, title, description, steps, image, 
                    data_Recipe.type_id, type_of_food, data_Recipe.servings_id, servings, data_Recipe.time_id, minutes 
                    FROM data_Recipe 
                    INNER JOIN data_Type ON data_Recipe.type_id = data_Type.type_id 
                    INNER JOIN data_Servings ON data_Recipe.servings_id = data_Servings.servings_id 
                    INNER JOIN data_Time ON data_Recipe.time_id = data_Time.time_id 
                    WHERE recipe_id=?;""", recipe_id)
    return data

# get data from data_Ingredients
def recipe_ingredients(recipe_id):
    ingredients = db_query("""SELECT id, recipe_id, quantity, unit, ingredient FROM data_ingredients 
                            INNER JOIN dft_Quantity ON data_Ingredients.quantity_id = dft_Quantity.quantity_id 
                            INNER JOIN dft_Units ON data_Ingredients.unit_id = dft_Units.unit_id 
                            INNER JOIN dft_Ingredients ON data_Ingredients.ingredient_id = dft_Ingredients.ingredient_id 
                            WHERE recipe_id=?;""", recipe_id)
    return ingredients
    
def update_recipe_data(recipe_id, title, description, steps, image, type_id, servings_id, time_id):
    db_write("""UPDATE data_Recipe 
    SET title=?, description=?, steps=?, image=?, type_id=?, servings_id=?, time_id=? 
    WHERE recipe_id=?;""", title, description, steps, image, type_id, servings_id, time_id, recipe_id)
    return

# Delete row in data_Ingredients
def delete_row_ingredient_data(i_data_id):
    db_write("DELETE FROM data_Ingredients WHERE id=?;", i_data_id)
    return