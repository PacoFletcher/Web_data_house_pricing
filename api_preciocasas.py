import pandas as pd
from flask import Flask, jsonify,request
import os
from sklearn.model_selection import train_test_split
from flask import render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "<h1>API para la predicción de precios de viviendas</h1><p>Ésta es una API que va a intentar predecir los precios de una vivienda en función de los parámetros que introduzca el usuario.</p>"

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return render_template('index.html')  # Muestra el formulario
    if request.method == 'POST':
        try:
            with open('xgb_model', 'rb') as f:
                model = pd.read_pickle(f)
            # Recoger los datos del formulario
            bathrooms = int(request.form.get('bathrooms'))
            bedrooms = int(request.form.get('bedrooms'))
            sqft_living = int(request.form.get('sqft_living'))
            sqft_lot = int(request.form.get('sqft_lot'))
            floors = int(request.form.get('floors'))
            view = int(request.form.get('view'))
            grade = int(request.form.get('grade'))
            sqft_above = int(request.form.get('sqft_above'))
            sqft_basement = int(request.form.get('sqft_basement'))
            yr_built = int(request.form.get('yr_built'))
            lat = float(request.form.get('lat'))
            long = float(request.form.get('long'))
            sqft_living15 = int(request.form.get('sqft_living15'))
            sqft_lot15 = int(request.form.get('sqft_lot15'))
            Average = int(request.form.get('Average', 0))
            Fair = int(request.form.get('Fair', 0))
            Good = int(request.form.get('Good', 0))
            Poor = int(request.form.get('Poor', 0))
            VeryGood = int(request.form.get('VeryGood', 0))
            
            if bathrooms < 0 or bedrooms < 0 or sqft_living <= 0 or sqft_lot <= 0 or floors <= 0 or view < 0 or view > 4 or grade < 1 or grade > 13 or sqft_above < 0 or sqft_basement < 0 or yr_built < 1934 or yr_built > 2014 or sqft_living15 <= 0 or sqft_lot15 <= 0:
                 return jsonify({'Error': 'Los valores no pueden ser negativos.'}), 400

            # Preparar los datos
            input_data = [[bathrooms, bedrooms, sqft_living, sqft_lot, floors, view, grade,
                           sqft_above, sqft_basement, yr_built, lat, long, sqft_living15,
                           sqft_lot15, Average, Fair, Good, VeryGood, Poor]]
            prediction = model.predict(input_data)
            precio_real = 10 ** prediction
            return jsonify({'resultado': f"El precio estimado de tu vivienda es: ${precio_real[0]:,.2f}"})
        except Exception as e:
            return jsonify({'Error': f"Ocurrió un error: {str(e)}"}), 500
if __name__ == '__main__':
    app.run(debug=True)