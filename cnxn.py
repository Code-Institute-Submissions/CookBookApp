import pyodbc
from creds import conn_str


# Read from DB
def db_query(query, *kwargs):
    cnxn = pyodbc.connect(conn_str)
    cursor = cnxn.cursor()
    cursor.execute(query, *kwargs)
    results = cursor.fetchall()
    
    cursor.close()
    cnxn.close()
    return results

# Read from separate tables, get all
def db_query_many(query1, query2, query3):
    cnxn = pyodbc.connect(conn_str)
    cursor = cnxn.cursor()
    
    cursor.execute(query1)
    data1 = cursor.fetchall()
    cursor.execute(query2)
    data2 = cursor.fetchall()
    cursor.execute(query3)
    data3 = cursor.fetchall()
    results = [data1, data2, data3]

    cursor.close()
    cnxn.close()
    return results

# Write to DB
def db_write(query, *kwargs):
    cnxn = pyodbc.connect(conn_str)
    cursor = cnxn.cursor()
    cursor.execute(query, *kwargs)
    
    cnxn.commit()
    cursor.close()
    cnxn.close()
    return

