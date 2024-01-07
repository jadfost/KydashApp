from flask import Flask, Blueprint, render_template, request, send_file
import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from io import BytesIO

novedad_dic2023 = Blueprint("novedad_dic2023", __name__)
app = Flask(__name__)  # Definir la instancia de Flask


def comparar_archivos(archivo_A, archivo_B):
    datos_A = pd.read_excel(archivo_A, sheet_name="Datos_A")
    datos_B = pd.read_excel(archivo_B, sheet_name="Datos_B")
    datos_X = pd.read_excel(archivo_A, sheet_name="Datos_X")
    datos_Z = pd.read_excel(archivo_B, sheet_name="Datos_Z")

    # Guardar las edades actuales en las columnas 'V - Edad' y 'V - Pago'
    datos_B["V - Edad"] = datos_B["Edad"]
    datos_B["V - Pago"] = datos_B["Pago"]
    datos_Z["V - Edad"] = datos_Z["Edad"]
    datos_Z["V - Pago"] = datos_Z["Pago"]

     # Logica para Datos_A y Datos_B
    for idx, fila_A in datos_A.iterrows():
        id_persona = fila_A["ID"]
        edad_A = fila_A["Edad"]
        pago_A = fila_A["Pago"]

        if id_persona in datos_B["ID"].values:
            edad_B = datos_B.loc[datos_B["ID"] == id_persona, "Edad"].values[0]
            pago_B = datos_B.loc[datos_B["ID"] == id_persona, "Pago"].values[0]

            if edad_A != edad_B:
                datos_B.loc[datos_B["ID"] == id_persona, "Edad"] = edad_A
            if pago_A != pago_B:
                datos_B.loc[datos_B["ID"] == id_persona, "Pago"] = pago_A
        else:
            datos_B = pd.concat([datos_B, fila_A.to_frame().T], ignore_index=True)

    datos_B["R - Edad"] = "Igual"
    datos_B["R - Pago"] = "Igual"

    datos_B.loc[datos_B["V - Edad"] != datos_B["Edad"], "R - Edad"] = "Hubo cambio"
    datos_B.loc[datos_B["V - Pago"] != datos_B["Pago"], "R - Pago"] = "Hubo cambio"

    # Logica para Datos_X y Datos_Z
    for idx, fila_X in datos_X.iterrows():
        id_persona = fila_X["ID"]
        edad_X = fila_X["Edad"]
        pago_X = fila_X["Pago"]

        if id_persona in datos_Z["ID"].values:
            edad_Z = datos_Z.loc[datos_Z["ID"] == id_persona, "Edad"].values[0]
            pago_Z = datos_Z.loc[datos_Z["ID"] == id_persona, "Pago"].values[0]

            if edad_X != edad_Z:
                datos_Z.loc[datos_Z["ID"] == id_persona, "Edad"] = edad_X
            if pago_X != pago_Z:
                datos_Z.loc[datos_Z["ID"] == id_persona, "Pago"] = pago_X
        else:
            datos_Z = pd.concat([datos_Z, fila_X.to_frame().T], ignore_index=True)

    datos_Z["R - Edad"] = "Igual"
    datos_Z["R - Pago"] = "Igual"

    datos_Z.loc[datos_Z["V - Edad"] != datos_Z["Edad"], "R - Edad"] = "Hubo cambio"
    datos_Z.loc[datos_Z["V - Pago"] != datos_Z["Pago"], "R - Pago"] = "Hubo cambio"

    return datos_B, datos_Z

@novedad_dic2023.route("/")
def novedades():
    return render_template("/novedades/novedades.html")


@novedad_dic2023.route("/procesar_archivos", methods=["POST"])
def procesar_archivos():
    archivo_A = request.files["archivo_A"]
    archivo_B = request.files["archivo_B"]

    datos_B, datos_Z = comparar_archivos(archivo_A, archivo_B)

    # Leer el archivo existente para conservar las fórmulas para Datos_B
    wb = load_workbook(archivo_B)
    ws_B = wb["Datos_B"]

    # Obtener las fórmulas en la columna '% Pago' para Datos_B
    formulas_B = {cell.coordinate: cell for cell in ws_B["K"][1:] if cell.data_type == "f"}
    formulas_B.update({cell.coordinate: cell for cell in ws_B["L"][1:] if cell.data_type == "f"})

    # Convertir los datos modificados de Datos_B a un dataframe de Pandas
    df_B = pd.DataFrame(datos_B)

    # Iterar sobre el DataFrame de Datos_B y escribir en el archivo respetando las fórmulas
    for r_idx, row in enumerate(dataframe_to_rows(df_B, index=False, header=True), 1):
        for c_idx, value in enumerate(row, 1):
            cell = ws_B.cell(row=r_idx, column=c_idx)
            if cell.coordinate in formulas_B:
                ws_B[cell.coordinate] = formulas_B[cell.coordinate].value
            else:
                cell.value = value

    # Leer el archivo existente para conservar las fórmulas para Datos_Z
    ws_Z = wb["Datos_Z"]

    # Obtener las fórmulas en la columna '% Pago' para Datos_Z
    formulas_Z = {cell.coordinate: cell for cell in ws_Z["K"][1:] if cell.data_type == "f"}
    formulas_Z.update({cell.coordinate: cell for cell in ws_Z["L"][1:] if cell.data_type == "f"})
    
    # Convertir los datos modificados de Datos_Z a un dataframe de Pandas
    df_Z = pd.DataFrame(datos_Z)

    # Iterar sobre el DataFrame de Datos_Z y escribir en el archivo respetando las fórmulas
    for r_idx, row in enumerate(dataframe_to_rows(df_Z, index=False, header=True), 1):
        for c_idx, value in enumerate(row, 1):
            cell = ws_Z.cell(row=r_idx, column=c_idx)
            if cell.coordinate in formulas_Z:
                ws_Z[cell.coordinate] = formulas_Z[cell.coordinate].value
            else:
                cell.value = value

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="añañayy_modificado.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


if __name__ == "__main__":
    app.register_blueprint(novedad_dic2023, url_prefix="/novedad")
    app.run(debug=True)
