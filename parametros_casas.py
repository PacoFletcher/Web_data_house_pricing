import requests

url = "http://127.0.0.1:5000/predict"
data = {
    "bathrooms": 4,
    "bedrooms": 3,
    "sqft_living": 1800,
    "sqft_lot": 5000,
    "floors": 3,
    "view": 4,
    "grade": 12,
    "sqft_above": 1800,
    "sqft_basement": 2000,
    "yr_built": 1990,
    "lat": 47.55,
    "long": -122.3,
    "sqft_living15": 1500,
    "sqft_lot15": 4000,
    "Average": 0,
    "Fair": 0,
    "Good": 0,
    "VeryGood": 1,
    "Poor": 0
}

response = requests.post(url, json=data)
print(response.json())