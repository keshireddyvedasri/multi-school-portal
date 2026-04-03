import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT
)
''')

# Schools table
cursor.execute('''
CREATE TABLE IF NOT EXISTS schools (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    location TEXT
)
''')

# Finance table
cursor.execute('''
CREATE TABLE IF NOT EXISTS finance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    amount INTEGER,
    description TEXT
)
''')

# Insert users safely
cursor.execute("SELECT * FROM users WHERE username='admin'")
if not cursor.fetchone():
    cursor.execute("INSERT INTO users (username, password, role) VALUES ('admin', '123', 'admin')")

cursor.execute("SELECT * FROM users WHERE username='incharge'")
if not cursor.fetchone():
    cursor.execute("INSERT INTO users (username, password, role) VALUES ('incharge', '123', 'incharge')")

conn.commit()
conn.close()

print("Database initialized successfully!")