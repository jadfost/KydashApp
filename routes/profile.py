# routes/profile.py
from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from routes.db.db import get_users_collection

profile_bp = Blueprint('profile_bp', __name__)

users_collection = get_users_collection()

@profile_bp.route('/')
def profile():
    if 'username' in session:
        # Fetch user data from the database
        user_data = users_collection.find_one({'username': session['username']})

        if user_data:
            # Pass user data to the template
            return render_template('profile.html', user=user_data)
    
    # Redirect to login if user data is not found or user is not logged in
    return redirect(url_for('auth_bp.login'))

@profile_bp.route('/edit_profile', methods=['POST'])
def edit_profile():
    if 'username' in session:
        # Fetch user data from the database
        user_data = users_collection.find_one({'username': session['username']})

        if user_data:
            # Update user information
            new_name = request.form.get('new_name')
            new_lastname = request.form.get('new_lastname')
            new_email = request.form.get('new_email')

            # Check if the updated information is different from the current information
            if (new_name != user_data['name'] or
                new_lastname != user_data['lastname'] or
                new_email != user_data['email']):

                # Save the updated user data to the database
                user_data['name'] = new_name
                user_data['lastname'] = new_lastname
                user_data['email'] = new_email
                users_collection.update_one({'username': session['username']}, {'$set': user_data})

                # Flash a success message
                flash('Perfil actualizado exitosamente!', 'success')
            else:
                # Flash an error message
                flash('No se han realizado cambios en el Perfil', 'danger')

    # Redirect to the profile page after updating
    return redirect(url_for('profile_bp.profile'))
