# routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == '123456':
            session['username'] = username
            return redirect(url_for('dashboard_bp.dashboard'))
        else:
            flash("Credenciales inválidas. Inténtalo de nuevo.", 'error')
    return render_template('login.html')

@auth_bp.route('/register', methods=['POST'])
def register():
    # Simulación de lógica para verificar los permisos para crear una cuenta
    # Si no tiene permisos, muestra un mensaje de error
    flash('No tiene permisos para hacer esto', 'error')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))