from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Ініціалізація бази даних
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Пошук користувача в базі даних
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['user_email'] = email
            return redirect(url_for('search'))
        else:
            return render_template('login.html', error="Invalid email or password.")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return render_template('register.html', error="Passwords do not match.")

        hashed_password = generate_password_hash(password)

        try:
            # Додавання нового користувача до бази даних
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed_password))
            conn.commit()
            conn.close()
            return render_template('login.html', success="Account successfully created! Please log in.")
        except sqlite3.IntegrityError:
            return render_template('register.html', error="User already exists.")
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    return redirect(url_for('home'))

@app.route('/search')
def search():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    return render_template('search.html')

@app.route('/search_query')
def search_query():
    query = request.args.get('query', '').lower()
    
    # Завантаження ігор із JSON-файлу
    with open('static/games.json', 'r') as file:
        games = json.load(file)

    # Фільтрація ігор за пошуковим запитом
    results = [game for game in games if query in game['name'].lower()]
    
    return {"results": results}

if __name__ == '__main__':
    app.run(debug=True)
