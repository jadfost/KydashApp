# routes/mecanica.py
from flask import Blueprint, render_template, redirect, url_for, session

mecanica_bp = Blueprint('mecanica_bp', __name__)

@mecanica_bp.route('/')
def mecanica():
    if 'username' in session:
        return render_template('mecanica.html')
    return redirect(url_for('auth_bp.login'))
