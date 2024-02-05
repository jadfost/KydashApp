# routes/mecanica.py
from flask import Blueprint, render_template, redirect, url_for, session

catalogo_bp = Blueprint('catalogo_bp', __name__)

@catalogo_bp.route('/')
def catalogo():
    if 'username' in session:
        return render_template('coltabaco/catalogo.html')
    return redirect(url_for('auth_bp.login'))
