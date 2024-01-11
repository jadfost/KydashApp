from flask import Flask, render_template, request, redirect, url_for, session, flash
from routes import novedad_bp
from routes.tradicional.diciembre_2023 import novedad_dic2023

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Cambia esto por una clave segura

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == '123456':
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash("Credenciales inválidas. Inténtalo de nuevo.", 'error')
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    # Simulación de lógica para verificar los permisos para crear una cuenta
    # Si no tiene permisos, muestra un mensaje de error
    flash('No tiene permisos para hacer esto', 'error')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'username' in session:
        return render_template('profile.html')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# Registra el blueprint en tu aplicación
app.register_blueprint(novedad_bp, url_prefix='/novedad')
app.register_blueprint(novedad_dic2023, url_prefix='/tradicional/diciembre')

if __name__ == '__main__':
    app.run(debug=True)