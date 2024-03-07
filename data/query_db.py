import sqlite3

 

conn = sqlite3.connect("app.db")

# Create a cursor object
cur = conn.cursor()

# Define a schema
cur.execute('''
    SELECT sql FROM sqlite_master WHERE type='table' AND name='users';
''')

schema_result = cur.fetchone()
if schema_result:
    schema_sql = schema_result[0]
    print("Schema of 'users' table:")
    print(schema_sql)
else:
    print("Table 'users' does not exist in the database.")


conn.close()
