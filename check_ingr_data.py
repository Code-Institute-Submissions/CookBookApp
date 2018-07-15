import db_recipe_add
import helpers
import uuid


def check_data_quantities(quantities):
    quantity_ids = []
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
    return quantity_ids
    
def check_data_units(units):
    unit_ids = []
# If units data exists in DB, get their ID, else create it and add new record to dft_table
    for u in units:
            u = u.strip().lower()
            u_data = db_recipe_add.check_if_unit_in_db(u)
            if u_data:
                u_id_data = db_recipe_add.get_unit_id(u)
                for data in u_id_data:
                    u_id = data.unit_id
                    unit_ids.append(u_id)
            else:
                u_id = uuid.uuid4()
                unit_ids.append(u_id)
                db_recipe_add.add_new_unit(u_id, u)
    return unit_ids
    
def check_data_ingredients(ingredients):
    ingredient_ids = []
# If ingredients data exists in DB, get their ID, else create it and add new record to dft_table
    for i in ingredients:
            i = i.strip().lower()
            i_data = db_recipe_add.check_if_ingredient_in_db(i)
            if i_data:
                i_id_data = db_recipe_add.get_ingredient_id(i)
                for data in i_id_data:
                    i_id = data.ingredient_id
                    ingredient_ids.append(i_id)
            else:
                i_id = uuid.uuid4()
                ingredient_ids.append(i_id)
                db_recipe_add.add_new_ingredient(i_id, i)
    return ingredient_ids