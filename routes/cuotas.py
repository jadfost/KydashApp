# routes/cuotas.py
from flask import Blueprint, render_template, redirect, url_for, session

cuotas_bp = Blueprint('cuotas_bp', __name__)

@cuotas_bp.route('/')
def cuotas():
    if 'username' in session:
        return render_template('cuotas.html')
    return redirect(url_for('auth_bp.login'))
