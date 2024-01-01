from flask import Flask, render_template, request, redirect, url_for, session
from api.db import get_user, create_user
from novedad import novedad_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Cambia esto por una clave segura

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username)
        if user and user['password'] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Credenciales inválidas. Inténtalo de nuevo."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if create_user(username, password):
            return redirect(url_for('login'))
        else:
            return "El usuario ya existe."
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')
    return redirect(url_for('login'))


@app.route('/calculadora', methods=['GET', 'POST'])
def calculadora():
    if request.method == 'POST':
        num1 = float(request.form['num1'])
        num2 = float(request.form['num2'])
        resultado = num1 + num2
        return render_template('calculadora.html', resultado=resultado)
    return render_template('calculadora.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# Registra el blueprint en tu aplicación
app.register_blueprint(novedad_bp, url_prefix='/novedad')

if __name__ == '__main__':
    app.run(debug=True)