# routes/profile.py
from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from routes.db.db import get_users_collection
from werkzeug.security import generate_password_hash, check_password_hash

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


@profile_bp.route('/change_password', methods=['POST'])
def change_password():
    if 'username' in session:
        # Fetch user data from the database
        user_data = users_collection.find_one({'username': session['username']})

        if user_data:
            # Check if the provided current password matches the stored hashed password
            current_password = request.form.get('current_password')
            if check_password_hash(user_data['password'], current_password):
                # Check if the new password and the confirmation match
                new_password = request.form.get('new_password')
                confirm_password = request.form.get('confirm_password')

                if new_password == confirm_password:
                    # Hash and update the user's password in the database
                    hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
                    user_data['password'] = hashed_password
                    users_collection.update_one({'username': session['username']}, {'$set': user_data})

                    # Flash a success message
                    flash('Contraseña cambiada exitosamente!', 'success')
                else:
                    # Flash an error message if the new password and confirmation don't match
                    flash('Las nuevas contraseñas no coinciden', 'danger')
            else:
                # Flash an error message if the current password is incorrect
                flash('Contraseña actual incorrecta', 'danger')

    # Redirect to the profile page after updating
    return redirect(url_for('profile_bp.profile'))