from flask import Flask, render_template, request, send_file
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from io import BytesIO

app = Flask(__name__)

def comparar_archivos(archivo_A, archivo_B):
    datos_A = pd.read_excel(archivo_A)
    datos_B = pd.read_excel(archivo_B, sheet_name='Datos_B')  # Asegúrate de leer la hoja correcta
    
    # Guardar las edades actuales en las columnas 'V - Edad' y 'V - Pago'
    datos_B['V - Edad'] = datos_B['Edad']
    datos_B['V - Pago'] = datos_B['Pago']

    for idx, fila_A in datos_A.iterrows():
        id_persona = fila_A['ID']
        edad_A = fila_A['Edad']
        pago_A = fila_A['Pago']

        if id_persona in datos_B['ID'].values:
            edad_B = datos_B.loc[datos_B['ID'] == id_persona, 'Edad'].values[0]
            pago_B = datos_B.loc[datos_B['ID'] == id_persona, 'Pago'].values[0]

            if edad_A != edad_B:
                datos_B.loc[datos_B['ID'] == id_persona, 'Edad'] = edad_A
            if pago_A != pago_B:
                datos_B.loc[datos_B['ID'] == id_persona, 'Pago'] = pago_A
        else:
            datos_B = pd.concat([datos_B, fila_A.to_frame().T], ignore_index=True)

    datos_B['R - Edad'] = 'Igual'
    datos_B['R - Pago'] = 'Igual'

    datos_B.loc[datos_B['V - Edad'] != datos_B['Edad'], 'R - Edad'] = 'Hubo cambio'
    datos_B.loc[datos_B['V - Pago'] != datos_B['Pago'], 'R - Pago'] = 'Hubo cambio'

    return datos_B

@app.route('/')
def index():
    return render_template('cargar_archivos.html')

@app.route('/procesar_archivos', methods=['POST'])
def procesar_archivos():
    archivo_A = request.files['archivo_A']
    archivo_B = request.files['archivo_B']
    
    datos_modificados = comparar_archivos(archivo_A, archivo_B)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        datos_modificados.to_excel(writer, sheet_name='Datos_B', index=False)
    output.seek(0)
    
    return send_file(output, as_attachment=True, download_name='Libro2_modificado.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == '__main__':
    app.run(debug=True)
