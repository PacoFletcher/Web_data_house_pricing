import requests

url = "http://127.0.0.1:5000/predict"
data = {
    "bathrooms": 2,
    "bedrooms": 3,
    "sqft_living": 1800,
    "sqft_lot": 5000,
    "floors": 1,
    "view": 0,
    "grade": 7,
    "sqft_above": 1800,
    "sqft_basement": 0,
    "yr_built": 1990,
    "lat": 47.55,
    "long": -122.3,
    "sqft_living15": 1500,
    "sqft_lot15": 4000,
    "Average": 0,
    "Fair": 1,
    "Good": 0,
    "VeryGood": 0,
    "Poor": 0
}

response = requests.post(url, json=data)
print(response.json())