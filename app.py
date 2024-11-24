from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Імітація бази даних для користувачів
users = {
    "user@example.com": "password123"
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email in users and users[email] == password:
            session['user_email'] = email
            return redirect(url_for('search'))
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
        
        if email in users:
            return render_template('register.html', error="User already exists.")
        
        users[email] = password
        return render_template('login.html', success="Account successfully created! Please log in.")
    
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
    
    # Завантажуємо ігри з JSON-файлу
    with open('static/games.json', 'r') as file:
        games = json.load(file)

    # Фільтруємо ігри за пошуковим запитом
    results = [game for game in games if query in game['name'].lower()]
    
    return {"results": results}

if __name__ == '__main__':
    app.run(debug=True)
