#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc


from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    response = make_response(
        jsonify(bakeries),
        200,
        {"Content-Typer": "application/json"}
    )
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery_id = Bakery.query.filter(Bakery.id==id).first()
    bakery_dict = bakery_id.to_dict()
    response = make_response(
        bakery_dict,
        200
    )
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(desc(BakedGood.price)).all()
    return jsonify([bg.to_dict() for bg in baked_goods])

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_expensive = BakedGood.query.order_by(desc(BakedGood.price)).limit(1).first()

    return jsonify(baked_expensive.to_dict())

if __name__ == '__main__':
    app.run(port=5555, debug=True)
