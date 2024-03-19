import sqlite3

 

conn = sqlite3.connect("app.db")

# Create a cursor object
cur = conn.cursor()

# Define a schema
cur.execute('''
    SELECT * FROM users  ;
''')

results = cur.fetchall()
for result in results:
    print(result)


conn.close()
