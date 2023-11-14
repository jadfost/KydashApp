import os
import csv
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Directorio que contiene los archivos CSV
DIRS_DIR = 'Datos/DIRS/'

# Función para cargar datos desde archivos CSV
def cargar_datos(tabla):
    archivo_csv = os.path.join(DIRS_DIR, f'{tabla}.csv')
    with open(archivo_csv, 'r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data

# Ruta para manejar la solicitud de actualización del dropdown
@app.route('/update_dropdown', methods=['POST'])
def update_dropdown():
    tabla_seleccionada = request.form['tabla']
    data_seleccionada = cargar_datos(tabla_seleccionada)
    columnas = data_seleccionada[0].keys()
    opciones = [{'label': columna, 'value': columna} for columna in columnas]
    return jsonify({'columnas': opciones})

# Ruta para manejar la solicitud de actualización del gráfico
@app.route('/update_graph', methods=['POST'])
def update_graph():
    tabla_seleccionada = request.form['tabla']
    campo_seleccionado = request.form['campo']
    data_seleccionada = cargar_datos(tabla_seleccionada)

    # Verifica que la columna seleccionada esté en los datos
    if campo_seleccionado not in data_seleccionada[0]:
        return jsonify({'error': 'Columna no encontrada'})

    # Prepara los datos para el gráfico
    data = {
        'x': [row[campo_seleccionado] for row in data_seleccionada],
        'type': 'bar',
        'marker': {'color': 'blue'}
    }

    return jsonify(data)

# Función principal para obtener el DataFrame según la tabla seleccionada
def obtener_datos_segun_tabla(tabla):
    if tabla in ['DIRS 1', 'DIRS 2', 'DIRS 3', 'DIRS 4']:
        return cargar_datos(tabla)
    return []

# Ruta para manejar la carga inicial de datos
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
