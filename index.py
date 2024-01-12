from flask import Flask, render_template, request, redirect, url_for, session, flash
from routes.novedad import novedad_bp
from routes.tradicional.diciembre_2023 import novedad_dic2023
from routes.auth import auth_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Cambia esto por una clave segura

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
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

# Blueprint aplicación
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(novedad_bp, url_prefix='/novedad')
app.register_blueprint(novedad_dic2023, url_prefix='/tradicional/diciembre')

if __name__ == '__main__':
    app.run(debug=True)