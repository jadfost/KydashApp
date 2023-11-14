import os
import pandas as pd
from flask import Flask, render_template, jsonify, request


app = Flask(__name__)

# Cargar los datos desde los archivos CSV
df1 = pd.read_csv('Datos/DIRS/DIRS 1.csv')
df2 = pd.read_csv('Datos/DIRS/DIRS 2.csv')
df3 = pd.read_csv('Datos/DIRS/DIRS 3.csv')
df4 = pd.read_csv('Datos/DIRS/DIRS 4.csv')

@app.route('/')
def index():
    return render_template('index.html')

# Ruta para manejar la solicitud de actualización del dropdown
@app.route('/update_dropdown', methods=['POST'])
def update_dropdown():
    tabla_seleccionada = request.form['tabla']
    df_seleccionado = obtener_dataframe_segun_tabla(tabla_seleccionada)
    columnas = df_seleccionado.columns
    opciones = [{'label': columna, 'value': columna} for columna in columnas]
    return jsonify({'columnas': opciones})

# Ruta para manejar la solicitud de actualización del gráfico
@app.route('/update_graph', methods=['POST'])
def update_graph():
    tabla_seleccionada = request.form['tabla']
    campo_seleccionado = request.form['campo']
    df_seleccionado = obtener_dataframe_segun_tabla(tabla_seleccionada)
    
    # Verifica que la columna seleccionada esté en el DataFrame
    if campo_seleccionado not in df_seleccionado.columns:
        return jsonify({'error': 'Columna no encontrada'})

    # Prepara los datos para el gráfico
    data = {
        'x': df_seleccionado[campo_seleccionado].tolist(),
        'type': 'bar',
        'marker': {'color': 'blue'}
    }

    return jsonify(data)

# Función para obtener el DataFrame según la tabla seleccionada
def obtener_dataframe_segun_tabla(tabla):
    if tabla == 'DIRS 1':
        return df1
    elif tabla == 'DIRS 2':
        return df2
    elif tabla == 'DIRS 3':
        return df3
    elif tabla == 'DIRS 4':
        return df4
    
if __name__ == '__main__':
    app.run(debug=True)