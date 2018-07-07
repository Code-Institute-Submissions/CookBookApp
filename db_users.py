from cnxn import db_query, db_write

# Check if username and password exist in DB for login
def check_username_password(username, password):
    data = db_query("SELECT username, password FROM data_User WHERE username=? AND password=?;", username, password)
    # print(data)
    return True if data else False
    
# Check if username dont exist yet for registration
def check_username_dont_exists(username):
    data = db_query("SELECT username FROM data_User WHERE username=?;", username)
    return False if data else True

# Add new user to DB  
def add_new_user_to_db(first, last, username, password):
    db_write("INSERT INTO data_User(first, last, username, password) VALUES (?, ?, ?, ?);", first, last, username, password)
    return

# Get user_id for username
def get_user_id(username):
    data = db_query("SELECT user_id FROM data_User WHERE username=?;", username)
    # print(data)
    return data