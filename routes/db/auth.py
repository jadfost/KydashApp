# routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
from datetime import timedelta
from routes.db.db import get_users_collection

auth_bp = Blueprint('auth_bp', __name__)
SESSION_TYPE = 'filesystem'

# Configuración de la extensión de sesión
auth_bp.config = dict(
    SESSION_PERMANENT=True,
    SESSION_USE_SIGNER=True,
    SESSION_KEY_PREFIX='kydash_',
    PERMANENT_SESSION_LIFETIME=timedelta(hours=3),
)

# Inicializar la extensión de sesión
Session(auth_bp)

users_collection = get_users_collection()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'username': username})

        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('dashboard_bp.dashboard'))
        else:
            flash("Credenciales inválidas. Inténtalo de nuevo.", 'error')
    return render_template('login.html')

@auth_bp.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    admin_code = request.form['admin_code']

    # Verificar si el código de administrador es correcto
    if admin_code != 'Dorothy1ove@':  # Reemplaza 'tu_codigo_admin' con tu código real
        flash('Sin permisos. Inténtalo de nuevo.', 'error')
        return render_template('login.html')

    # Verificar si el nombre de usuario ya está en uso
    if users_collection.find_one({'username': username}):
        flash('El nombre de usuario ya está en uso. Elija otro.', 'error')
    else:
        # Hashear la contraseña antes de almacenarla en la base de datos
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        user_data = {'username': username, 'password': hashed_password}
        users_collection.insert_one(user_data)
        flash('Registro exitoso. Ahora puede iniciar sesión.', 'success')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    # Limpiar la sesión y redirigir al usuario a la página de inicio
    session.pop('username', None)
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('auth_bp.login'))