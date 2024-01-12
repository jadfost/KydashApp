# routes/dashboard.py
from flask import Blueprint, render_template, redirect, url_for, session

dashboard_bp = Blueprint('dashboard_bp', __name__)

@dashboard_bp.route('/')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')
    return redirect(url_for('auth_bp.login'))
