import math
import os

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from waitress import serve

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///predictions.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class PredictionRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sepal_length = db.Column(db.Float, nullable=False)
    sepal_width = db.Column(db.Float, nullable=False)
    petal_length = db.Column(db.Float, nullable=False)
    petal_width = db.Column(db.Float, nullable=False)
    prediction = db.Column(db.String(100), nullable=False)

    def as_dict(self):
        return {
            'id': self.id,
            'sepal_length': self.sepal_length,
            'sepal_width': self.sepal_width,
            'petal_length': self.petal_length,
            'petal_width': self.petal_width,
            'prediction': self.prediction,
        }


with app.app_context():
    db.create_all()


@app.get('/')
def health():
    return jsonify(status='ok')


@app.route('/records', methods=['GET', 'POST'])
def records():
    if request.method == 'GET':
        saved_records = PredictionRecord.query.order_by(PredictionRecord.id.desc()).all()
        return jsonify([record.as_dict() for record in saved_records])

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error='A JSON object is required'), 400

    fields = ('sepal_length', 'sepal_width', 'petal_length', 'petal_width')
    try:
        measurements = {field: float(payload[field]) for field in fields}
    except (KeyError, TypeError, ValueError):
        return jsonify(error='All four measurements must be numeric'), 400
    if not all(math.isfinite(value) for value in measurements.values()):
        return jsonify(error='Measurements must be finite numbers'), 400

    prediction = payload.get('prediction')
    if not isinstance(prediction, str) or not prediction:
        return jsonify(error='A prediction string is required'), 400

    record = PredictionRecord(**measurements, prediction=prediction)
    db.session.add(record)
    db.session.commit()
    return jsonify(record.as_dict()), 201


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    serve(app, host='0.0.0.0', port=5002)