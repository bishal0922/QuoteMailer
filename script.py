import sqlite3
import json

def create_quotes_table(db_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    
    # Create the quotes table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quote TEXT NOT NULL,
        source TEXT NOT NULL,
        philosophy TEXT
    )
    ''')
    conn.commit()
    conn.close()
    print("Quotes table created or already exists.")

def import_quotes_to_db(json_file, db_file):
    # Open and read the JSON file
    with open(json_file, 'r', encoding='utf-8') as file:
        quotes = json.load(file)

    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    for quote in quotes:
        try:
            cur.execute('INSERT INTO quotes (quote, source, philosophy) VALUES (?, ?, ?)',
                        (quote['quote'], quote['source'], quote.get('philosophy', '')))
            print(f"Imported: {quote['quote'][:30]}...")
        except sqlite3.IntegrityError as e:
            print(f"Error inserting quote: {e}")

    conn.commit()
    conn.close()
    print(f"Successfully imported {len(quotes)} quotes into the database.")

# Adjust the file paths as needed
db_file = 'app.db'
json_file = 'quotes.json'

# Create the quotes table
# create_quotes_table(db_file)

# Import quotes into the database
# import_quotes_to_db(json_file, db_file)


