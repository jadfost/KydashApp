# routes/profile.py
from flask import Blueprint, render_template, redirect, url_for, session
from routes.db.db import get_users_collection

profile_bp = Blueprint('profile_bp', __name__)

users_collection = get_users_collection()

@profile_bp.route('/')
def profile():
    if 'username' in session:
        print("Session username:", session['username'])
        # Fetch user data from the database
        user_data = users_collection.find_one({'username': session['username']})
        print("User data:", user_data)

        if user_data:
            # Pass user data to the template
            return render_template('profile.html', user=user_data)
        
    # Redirect to login if user data is not found or user is not logged in
    return redirect(url_for('auth_bp.login'))
