import os
import pickle
from pathlib import Path

import numpy as np
import requests
from flask import Flask, render_template, request
from waitress import serve

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / 'iris_model.pkl'
DB_API_URL = os.getenv('DB_API_URL', 'http://127.0.0.1:5002').rstrip('/')

with MODEL_PATH.open('rb') as model_file:
    model = pickle.load(model_file)

app = Flask(__name__, template_folder=str(BASE_DIR / 'templates'))


@app.route('/', methods=['GET'])
def home():
    if request.host == 'api.abcd.com':
        return 'API is running'
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return render_template('index.html')

    try:
        values = [
            float(request.form['sl']),
            float(request.form['sw']),
            float(request.form['pl']),
            float(request.form['pw']),
        ]
    except (KeyError, TypeError, ValueError):
        return 'Invalid flower measurements provided', 400

    if not all(np.isfinite(values)):
        return 'Measurements must be finite numbers', 400

    sepal_length, sepal_width, petal_length, petal_width = values
    input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
    prediction = model.predict(input_data)
    record = {
        'sepal_length': sepal_length,
        'sepal_width': sepal_width,
        'petal_length': petal_length,
        'petal_width': petal_width,
        'prediction': str(prediction[0]),
    }

    try:
        response = requests.post(f'{DB_API_URL}/records', json=record, timeout=5)
        response.raise_for_status()
    except requests.RequestException:
        return 'Database service unavailable', 503

    return render_template('prediction.html', prediction_text=f'Predicted Iris Species: {prediction[0]}')


@app.route('/show_records', methods=['GET'])
def show_records():
    try:
        response = requests.get(f'{DB_API_URL}/records', timeout=5)
        response.raise_for_status()
    except requests.RequestException:
        return 'Database service unavailable', 503

    return render_template('records.html', records=response.json())


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5001)
