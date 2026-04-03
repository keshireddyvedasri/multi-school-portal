from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- DATABASE ---------------- #

def get_db():
    return sqlite3.connect('database.db')

# Initialize database (important for deployment)
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        role TEXT
    )''')

    # Schools table
    cursor.execute('''CREATE TABLE IF NOT EXISTS schools (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        location TEXT
    )''')

    # Finance table
    cursor.execute('''CREATE TABLE IF NOT EXISTS finance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        amount INTEGER,
        description TEXT
    )''')

    # Default users
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password, role) VALUES ('admin','123','admin')")

    cursor.execute("SELECT * FROM users WHERE username='incharge'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password, role) VALUES ('incharge','123','incharge')")

    conn.commit()
    conn.close()

# Call DB init
init_db()

# ---------------- ROUTES ---------------- #

# Login page
@app.route('/')
def login():
    return render_template('login.html')

# Handle login
@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form['username']
    password = request.form['password']

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()

    if user:
        session['user'] = username
        session['role'] = user[3]

        if user[3] == 'admin':
            return redirect('/admin')
        else:
            return redirect('/incharge')
    else:
        return "Invalid Credentials"

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ---------------- ADMIN ---------------- #

@app.route('/admin')
def admin():
    if 'user' not in session or session['role'] != 'admin':
        return redirect('/')

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM schools")
    schools = cursor.fetchall()

    return render_template('admin.html', schools=schools)

@app.route('/add_school', methods=['POST'])
def add_school():
    if 'user' not in session:
        return redirect('/')

    name = request.form['school_name']
    location = request.form['location']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO schools (name, location) VALUES (?, ?)", (name, location))
    conn.commit()

    return redirect('/admin')

# ---------------- INCHARGE ---------------- #

@app.route('/incharge')
def incharge():
    if 'user' not in session or session['role'] != 'incharge':
        return redirect('/')

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM finance")
    records = cursor.fetchall()

    total_income = sum(r[2] for r in records if r[1] == 'income')
    total_expense = sum(r[2] for r in records if r[1] == 'expense')

    return render_template('incharge.html',
                           records=records,
                           total_income=total_income,
                           total_expense=total_expense)

@app.route('/add_record', methods=['POST'])
def add_record():
    if 'user' not in session:
        return redirect('/')

    type_ = request.form['type']
    amount = int(request.form['amount'])
    description = request.form['description']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO finance (type, amount, description) VALUES (?, ?, ?)",
                   (type_, amount, description))
    conn.commit()

    return redirect('/incharge')

# ---------------- RUN ---------------- #

if __name__ == '__main__':
    app.run(debug=True)