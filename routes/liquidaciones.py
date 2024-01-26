# routes/dashboard.py
from flask import Blueprint, render_template, redirect, url_for, session, request
import locale
from .db.db import get_tradicional_collection, get_unique_years, get_unique_months, get_unique_medicion_channels

liquidacion_bp = Blueprint('liquidacion_bp', __name__)


@liquidacion_bp.route('/')
def liquidacion():
    if 'username' in session:
        tradicional_collection = get_tradicional_collection()

        # Obtener opciones únicas para los filtros
        anos = get_unique_years()
        meses = get_unique_months()
        canales_medicion = get_unique_medicion_channels()

        # Obtener los valores de los filtros desde la solicitud del usuario
        ano = request.args.get('ano')
        mes = request.args.get('mes')
        canal_medicion = request.args.get('canal_medicion')

        # Construir el diccionario de filtros
        filters = {}
        if ano:
            filters['AÑO'] = int(ano)
        if mes:
            filters['MES'] = mes
        if canal_medicion:
            filters['CANAL MEDICIÓN'] = canal_medicion

        # Filtrar la colección según los criterios
        participantes = tradicional_collection.find(filters, {'_id': 0})

        # Convierte los resultados de MongoDB a una lista de diccionarios
        participantes = list(participantes)

        # Calcular las sumas totales después de aplicar los filtros
        total_cuotas = sum(participante.get('CUOTA VENTA TOTAL', 0) for participante in participantes)
        total_resultados = sum(participante.get('RESULTADOS VENTA TOTAL', 0) for participante in participantes)
        total_banderines = sum(participante.get('TOTAL BANDERINES', 0) for participante in participantes)

        locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')
        return render_template('liquidacion.html', participantes=participantes,
                               anos=anos, meses=meses, canales_medicion=canales_medicion,
                               total_cuotas=total_cuotas, total_resultados=total_resultados, total_banderines=total_banderines)

    return redirect(url_for('auth_bp.login'))
