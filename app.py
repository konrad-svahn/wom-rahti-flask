from crypt import methods
import os
import requests
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

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return {
            'method': request.method,
            'msg': 'webhoks work',
            'env': os.environ.get('ENV_VAR', 'Cannot find variable ENV_VAR')
        }
        
@app.route('/cabins', methods=['GET'])
def cabin():
    if request.method == 'GET':
        req = requests.get('https://wom-konrad-p1.azurewebsites.net/cottages/owned', headers = {'Authorization': str(request.headers.get('Authorization'))})
        return req.content

@app.route("/orders/<int:id>", methods=['PATCH', 'DELETE'])
def orderid(id):
    orde = db.get_or_404(Order, id)
    
    if request.method == "PATCH":
        body = request.get_json()
        orde.service=body['service']
        orde.cottage=body['cottage']
        orde.duration=body['duration']
        db.session.commit()
        return { 'msg': 'order modified', 'id': id}
    
    if request.method == "DELETE":
        db.session.delete(orde)
        db.session.commit()
        return { 'msg': 'order deleted', 'id': id}

@app.route('/orders', methods=['GET', 'POST'])
def order():        
    if request.method == 'GET':
        orders = []
        for orde in Order.query.all():
            orders.append({
                'id': orde.id,
                'service': orde.service,
                'cottage': orde.cottage,
                'duration': orde.duration
            })
        return orders
        
    if request.method == 'POST':
        body = request.get_json()
        new_order = Order(
            service=body['service'],
            cottage=body['cottage'],
            duration=body['duration']
        )
        db.session.add(new_order)
        db.session.commit()
        return { 'msg': 'order created', 'id': new_order.id}
    


@app.route('/services', methods=['GET', 'POST'])
def service():
    if request.method == 'GET':
        services = []
        for serv in Service.query.all():
            services.append({
                'id': serv.id,
                'name': serv.name,
                'cottage': serv.cottage,
                'hourly_cost': serv.hourly_cost
            })
        return services

    if request.method == 'POST':
        body = request.get_json()
        new_service = Service(
            name=body['name'],
            cottage=body['cottage'],
            hourly_cost=body['hourly_cost']
        )
        db.session.add(new_service)
        db.session.commit()
        return { 'msg': 'service created', 'id': new_service.id}

@app.route("/services/<int:id>", methods=['PATCH', 'DELETE'])
def serviceid(id):
    serv = db.get_or_404(Service, id)
    
    if request.method == "PATCH":
        body = request.get_json()
        serv.name=body['name']
        serv.cottage=body['cottage']
        serv.hourly_cost=body['hourly_cost']
        db.session.commit()
        return { 'msg': 'service modified', 'id': id}
    
    if request.method == "DELETE":
        db.session.delete(serv)
        db.session.commit()
        return { 'msg': 'service deleted', 'id': id}

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
