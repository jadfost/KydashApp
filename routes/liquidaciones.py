# routes/dashboard.py
from flask import Blueprint, render_template, redirect, url_for, session

liquidacion_bp = Blueprint('liquidacion_bp', __name__)

@liquidacion_bp.route('/')
def liquidacion():
    if 'username' in session:
        return render_template('liquidacion.html')
    return redirect(url_for('auth_bp.login'))
