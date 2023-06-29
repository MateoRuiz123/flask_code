from flask import Flask, render_template, request
import pandas as pd
import numpy as np

app = Flask(__name__)

# Leer el archivo de Excel
df = pd.read_excel('Registros.xlsx')

# Rellenar valores no finitos (NaN, inf) en la columna 'Calorias' con 0
df['Calorias'].fillna(0, inplace=True)
df['Calorias'].replace([np.inf, -np.inf], 0, inplace=True)

# Convertir la columna 'Calorias' a tipo float
df['Calorias'] = df['Calorias'].astype(float)

# Diccionario de productos con información de sabor y calorías
productos = {}

# Iterar sobre cada fila del DataFrame y actualizar el diccionario de productos
for index, row in df.iterrows():
    producto = row['Producto']
    sabor = row['Sabor']
    calorias = row['Calorias']
    
    productos[producto] = {'sabor': sabor, 'calorias': calorias}


@app.route('/', methods=['POST','GET'])
def index():
    # Obtener el sabor y las calorías proporcionadas por el usuario desde la solicitud POST
    if request.method == "POST":
        sabor = request.form['sabor']
        calorias = float(request.form['calorias'])

    # Filtrar los registros basados en el sabor y las calorías
        # filtered_df = df[(df['Sabor'] == sabor) & (df['Calorias'] <= calorias)]
        filtered_df = df[(df['Sabor'].str.lower() == sabor.lower()) & (df['Calorias'] == calorias)]

        # Obtener la lista de recomendaciones
        recommendations = filtered_df['Producto'].tolist()
        
        if len(recommendations) == 0:
            mensaje = "No hay recomendaciones disponibles para los criterios seleccionados."
            return render_template('index.html', mensaje=mensaje)
        
    
        else:
            return render_template('index.html', recommendations=recommendations)
    
    
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    # Obtener el sabor y las calorías proporcionadas por el usuario desde la solicitud POST
    sabor = request.form['sabor']
    calorias = float(request.form['calorias'])

    # Filtrar los registros basados en el sabor y las calorías
    # filtered_df = df[(df['Sabor'] == sabor) & (df['Calorias'] <= calorias)]
    filtered_df = df[(df['Sabor'].str.lower() == sabor.lower()) & (df['Calorias'] == calorias)]

    # Obtener la lista de recomendaciones
    recommendations = filtered_df['Producto'].tolist()

    if len(recommendations) == 0:
        mensaje = "No hay recomendaciones disponibles para los criterios seleccionados."
        return render_template('no_recommendations.html', mensaje=mensaje)
    else:
        return render_template('recommendations.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
