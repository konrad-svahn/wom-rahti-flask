from crypt import methods
import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')

db = SQLAlchemy()
db.init_app(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String(120), nullable=False)
    cottage = db.Column(db.String(120), nullable=False)
    duration = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    cottage = db.Column(db.String(120), nullable=False)
    hourly_cost = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return {
            'method': request.method,
            'msg': 'webhoks work',
            'env': os.environ.get('ENV_VAR', 'Cannot find variable ENV_VAR')
        }

    if request.method == 'POST':
        body = request.get_json()
        return {
            'msg': 'POST',
            'request_body': body
        }

@app.route('/orders', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def order():
    if request.method == 'GET':
        return {
            'method': request.method,
            'msg': 'webhoks work',
            'env': os.environ.get('ENV_VAR', 'Cannot find variable ENV_VAR')
        }

    if request.method == 'POST':
        body = request.get_json()
        return {
            'msg': 'POST',
            'request_body': body
        }

@app.route('/services', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def service():
    if request.method == 'GET':
        services = []
        for service in Service.query.all():
            services.append({
                'id': service.id,
                'name': service.name,
                'cotage': service.cottage,
                'hourly cost': service.hourly_cost
            })
        return services

    if request.method == 'POST':
        body = request.get_json()
        new_service = Service(name=body['name'])
        db.session.add(new_service)
        db.session.commit()
        return { 'msg': 'service created', 'id': new_service.id}

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
