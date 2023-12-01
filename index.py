import pandas as pd
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Variable global para guardar los datos del archivo .xlsx
datos = None

@app.route('/upload_file', methods=['POST'])
def upload_file():
    global datos
    file = request.files['file']
    if file and file.filename.endswith('.xlsx'):
        datos = pd.read_excel(file)
        return jsonify({'success': 'Archivo cargado correctamente'})
    else:
        return jsonify({'error': 'Archivo no válido'})

@app.route('/ver_datos', methods=['GET'])
def ver_datos():
    global datos
    if datos is not None:
        return datos.to_json(orient='records')
    else:
        return jsonify({'error': 'No hay datos para mostrar'})
        
# Ruta para manejar la carga inicial de datos
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
