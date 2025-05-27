import pandas as pd
from flask import Flask, jsonify,request
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({'Bienvenido al portal de prediccion de casas! Introduzca los parámetros para conocer qué precio tendra su vivienda.'})

model = pd.read_pickle(open('modelo_casas.pkl'))
@app.route('/predict', methods=['POST'])
def predict():
    
    data = request.get_json()
    
    try:
        
        surface = int(data['surface'])
        bedrooms = int(data['bedrooms'])
        restrooms = int(data['restrooms'])
        
        if surface < 0 or bedrooms < 0 or restrooms < 0:
                return jsonify({'Error': 'Los valores no pueden ser negativos.'}), 400
    

        input_data = [[surface, bedrooms, restrooms]]
        prediction = model.predict(input_data)
        precio_real = np.exp(prediction)

        return jsonify({'El precio de tu vivienda es de': float(precio_real[0])})
    
    except (KeyError, ValueError, TypeError):
        return jsonify({'Error': 'Datos de entrada inválidos.'}), 400

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")