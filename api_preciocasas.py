import pandas as pd
from flask import Flask, jsonify,request
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
    'mensaje': 'Bienvenido al portal de prediccion de casas. Introduzca los parametros para conocer que precio tendra su vivienda.'
})

@app.route('/predict', methods=['POST'])
def predict():
    with open('linear_model', 'rb') as f:
        model = pd.read_pickle(f)
    data = request.get_json()
    
    try:
        
        bathrooms = int(data['bathrooms'])
        bedrooms = int(data['bedrooms'])
        sqft_living = int(data['sqft_living'])
        sqft_lot = int(data['sqft_lot'])
        floors = int(data['floors'])
        view = int(data['view'])
        grade = int(data['grade'])
        sqft_above = int(data['sqft_above'])
        sqft_basement = int(data['sqft_basement'])
        yr_built = int(data['yr_built'])
        lat = float(data['lat'])
        long = float(data['long'])
        sqft_living15 = int(data['sqft_living15'])
        sqft_lot15 = int(data['sqft_lot15'])
        Average = int(data['Average'])
        Fair = int(data['Fair'])
        Good = int(data['Good'])
        Poor = int(data['Poor'])
        VeryGood = int(data['VeryGood'])
        
        
        
        if bathrooms < 0 or bedrooms < 0 or sqft_living <= 0 or sqft_lot <= 0 or floors <= 0 or view < 0 or view > 4 or grade < 1 or grade > 13 or sqft_above < 0 or sqft_basement < 0 or yr_built < 1934 or yr_built > 2014 or sqft_living15 <= 0 or sqft_lot15 <= 0:
                return jsonify({'Error': 'Los valores no pueden ser negativos.'}), 400
    

        input_data = [[bathrooms, bedrooms, sqft_living, sqft_lot, floors, view, grade, sqft_above, sqft_basement, yr_built, lat, long, sqft_living15, sqft_lot15, Average, Fair, Good, VeryGood, Poor]]
        prediction = model.predict(input_data)
        precio_real = 10 ** prediction

        return jsonify({'El precio de tu vivienda es de': float(precio_real[0])})
    
    except (KeyError, ValueError, TypeError):
        return jsonify({'Error': 'Datos de entrada inválidos.'}), 400

if __name__ == '__main__':
    app.run(debug=True)