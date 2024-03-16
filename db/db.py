import sqlite3

# Connect to SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect('app.db')

# Create a cursor object
cur = conn.cursor()

# Create table for subscribers
cur.execute('''
CREATE TABLE IF NOT EXISTS subscribers (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL UNIQUE
)
''')

# Create table for suggested quotes
cur.execute('''
CREATE TABLE IF NOT EXISTS suggested_quotes (
    id INTEGER PRIMARY KEY,
    quote_link TEXT,
    quote_text TEXT NOT NULL,
    author TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')



# Commit changes and close the connection
conn.commit()
conn.close()

print("Database setup completed.")
