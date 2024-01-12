from flask import Flask, render_template, request, redirect, url_for, session, flash
from routes.novedad import novedad_bp
from routes.tradicional.diciembre_2023 import novedad_dic2023
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.profile import profile_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard_bp.dashboard'))
    return render_template('login.html')

# Blueprint aplicación
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(novedad_bp, url_prefix='/novedad')
app.register_blueprint(novedad_dic2023, url_prefix='/tradicional/diciembre')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(profile_bp, url_prefix='/profile')

if __name__ == '__main__':
    app.run(debug=True)