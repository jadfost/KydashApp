# routes/dashboard.py
from flask import Blueprint, render_template, redirect, url_for, session
import locale
from .db.db import get_tradicional_collection

liquidacion_bp = Blueprint('liquidacion_bp', __name__)

# routes/liquidaciones.py
@liquidacion_bp.route('/')
def liquidacion():
    if 'username' in session:
        tradicional_collection = get_tradicional_collection()
        participantes = tradicional_collection.find({}, {'_id': 0})

        # Convierte los resultados de MongoDB a una lista de diccionarios
        participantes = list(participantes)

        locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')
        return render_template('liquidacion.html', participantes=participantes)

    return redirect(url_for('auth_bp.login'))


