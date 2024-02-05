# routes\liquidaciones.py
from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify
import locale
from .db.db import get_tradicional_collection, get_unique_years, get_unique_months, get_unique_medicion_channels, get_unique_medicion_executive

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
        ejecutivo = request.args.get('ejecutivo')

        # Construir el diccionario de filtros
        filters = {}
        if ano:
            filters['AÑO'] = int(ano)
        if mes:
            filters['MES'] = mes
        if canal_medicion:
            filters['CANAL MEDICIÓN'] = canal_medicion
        if ejecutivo:
            filters['EJECUTIVO'] = ejecutivo
            
        # Set the limit for each page (adjust as needed)
        per_page = 10

        # Get the current page number from the query parameters
        page = request.args.get('page', 1, type=int)

        # Calculate the number of documents to skip based on the page number
        skip = (page - 1) * per_page

        # Sort the participants by 'TOTAL BANDERINES' in descending order
        participantes = tradicional_collection.find(filters, {'_id': 0}).sort('TOTAL BANDERINES', -1).skip(skip).limit(per_page)
        
        # Convierte los resultados de MongoDB a una lista de diccionarios
        participantes = list(participantes)

        # Calcular las sumas totales después de aplicar los filtros
        total_cuotas = sum(participante.get('CUOTA VENTA TOTAL', 0) for participante in participantes)
        total_resultados = sum(participante.get('RESULTADOS VENTA TOTAL', 0) for participante in participantes)
        total_banderines = sum(participante.get('TOTAL BANDERINES', 0) for participante in participantes)

        # Get the total number of documents without pagination
        total_documents = tradicional_collection.count_documents(filters)

        # Calculate the total number of pages
        total_pages = (total_documents + per_page - 1) // per_page

        locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')
        return render_template('liquidacion.html', participantes=participantes,
                               anos=anos, meses=meses, canales_medicion=canales_medicion,
                               total_cuotas=total_cuotas, total_resultados=total_resultados,
                               total_banderines=total_banderines, page=page, per_page=per_page,
                               total_pages=total_pages)

    return redirect(url_for('auth_bp.login'))

@liquidacion_bp.route('/get_months')
def get_months():
    ano = request.args.get('ano')
    meses = get_unique_months(ano)
    return jsonify(meses)

@liquidacion_bp.route('/get_channels')
def get_channels():
    mes = request.args.get('mes')
    channels = get_unique_medicion_channels(mes)
    return jsonify(channels)

@liquidacion_bp.route('/get_executives')
def get_executives():
    canal = request.args.get('canal')
    try:
        executives = get_unique_medicion_executive(canal)
        print(f"Executives found: {executives}")
        return jsonify(executives)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)})


