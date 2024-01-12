# routes/profile.py
from flask import Blueprint, render_template, redirect, url_for, session

profile_bp = Blueprint('profile_bp', __name__)

@profile_bp.route('/profile')
def profile():
    if 'username' in session:
        return render_template('profile.html')
    return redirect(url_for('auth_bp.login'))
