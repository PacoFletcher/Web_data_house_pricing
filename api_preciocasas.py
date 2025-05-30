import pandas as pd
from flask import Flask, jsonify,request
from flask import render_template
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
import os
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pickle

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
            with open('randforest_model_def', 'rb') as f:
                model = pd.read_pickle(f)
            with open('imput_living15', 'rb') as f:
                modeliv = pd.read_pickle(f)
            with open('imput_lot15', 'rb') as f:
                modelot = pd.read_pickle(f)

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

            input_dataliv = [[lat, long]]
            predictionliv = modeliv.predict(input_dataliv)
            predictionlot = modelot.predict(input_dataliv)

            # Asegúrate de que sean arrays y extrae el valor
            if hasattr(predictionliv, '__getitem__'):
                predictionliv = predictionliv[0]
            if hasattr(predictionlot, '__getitem__'):
                predictionlot = predictionlot[0]

            if bathrooms < 0 or bedrooms < 0 or sqft_living <= 0 or sqft_lot <= 0 or floors <= 0 or view < 0 or view > 4 or grade < 1 or grade > 13 or sqft_above < 0 or sqft_basement < 0 or yr_built < 1934 or yr_built > 2014:
                 return jsonify({'Error': 'Los valores que has introducido son erróneos.'}), 400

            # Preparar los datos
            input_data = [[bathrooms, bedrooms, sqft_living, sqft_lot, floors, view, grade,
                           sqft_above, sqft_basement, yr_built, lat, long, predictionliv,
                           predictionlot]]

            prediction = model.predict(input_data)
            precio_real = 10 ** prediction
            return jsonify({
                'resultado': f"El precio estimado de tu vivienda es: ${precio_real[0]:,.2f}",
                'superficie15': f"Superficie habitable media de las 15 viviendas más cercanas: {predictionliv:,.0f} ft²",
                'lote15': f"Superficie media de la parcela de las 15 viviendas más cercanas: {predictionlot:,.0f} ft²",
            })
        except Exception as e:
            return jsonify({'Error': f"Ocurrió un error: {str(e)}"}), 500

@app.route('/retrain', methods=['GET'])
def retrain():
    if os.path.exists("data/house_prices_retrain.csv"):
        data = pd.read_csv('data/house_prices_retrain.csv')

        X_train, X_test, y_train, y_test = train_test_split(data.drop(columns=['Unnamed: 0','log_price','price','waterfront']),
                                                        data['log_price'],
                                                        test_size = 0.20,
                                                        random_state=42)

        model = RandomForestRegressor(max_depth = 7, n_estimators = 200, random_state = 42)
        model.fit(X_train, y_train)
        rmse = np.sqrt(mean_squared_error(y_test, model.predict(X_test)))
        mape = mean_absolute_percentage_error(y_test, model.predict(X_test))
        model.fit(data.drop(columns=['log_price']), data['log_price'])  
        pickle.dump(model, open('randforest_model_def.pkl', 'wb'))

        return f"Model retrained. New evaluation metric RMSE: {str(rmse)}, MAPE: {str(mape)}"
    else:
        return f"<h2>New data for retrain NOT FOUND. Nothing done!</h2>"


if __name__ == '__main__':
    app.run(debug=True)