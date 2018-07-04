import pyodbc
import creds

server = creds.server
database = creds.database
username = creds.username
password = creds.password
cnxn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

cursor = cnxn.cursor()

def db_query(query, *kwargs):
    cursor.execute(query, *kwargs)
    results = cursor.fetchall()
    return results