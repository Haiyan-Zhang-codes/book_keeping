
import sqlite3

# Connect to the database. This will create the file if it doesn't exist
conn = sqlite3.connect('app.db')

# Create a cursor object
cur = conn.cursor()

# Define a schema
# cur.execute('''CREATE TABLE IF NOT EXISTS users (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#                 username TEXT NOT NULL,
#                 hash TEXT NOT NULL,
#                 balance NUMERIC)''')

# cur.execute('''
# CREATE UNIQUE INDEX IF NOT EXISTS username ON users (username)
# ''')

cur.execute('''CREATE TABLE IF NOT EXISTS book_keeping(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            user_id INTEGER NOT NULL,
            amount NUMERIC NOT NULL,
            category TEXT,
            type TEXT NOT NULL,
            year INTEGER NOT NULL,
            month INTEGER NOT NULL,
            date INTEGER NOT NULL)''')



# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database initialized successfully.")


