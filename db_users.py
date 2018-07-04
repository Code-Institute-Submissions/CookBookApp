from cnxn import db_query

# Check if username and password exist in DB for login
def check_username_password(username, password):
    data = db_query("SELECT username, password FROM data_User WHERE username=? AND password=?;", username, password)
    print(data)
    return True if data else False