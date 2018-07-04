import pyodbc
import creds

server = creds.server
database = creds.database
username = creds.username
password = creds.password
cnxn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

cursor = cnxn.cursor()

# Read from DB
def db_query(query, *kwargs):
    cursor.execute(query, *kwargs)
    results = cursor.fetchall()
    return results

# Write to DB
def db_write(query, *kwargs):
    cursor.execute(query, *kwargs)
    cnxn.commit()
    return