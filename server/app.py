#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db,Bakery,BakedGood)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = []
    
    for bakery in Bakery.query.all():
        baked_goods = [baked_good.to_dict() for baked_good in bakery.baked_goods]
        bakery_dict = {
            "id": bakery.id,
            "name":bakery.name,    
            "baked_goods": baked_goods,
            "created_at": bakery.created_at,
                  
        }
        bakeries.append(bakery_dict)
        response = make_response(
            jsonify(bakeries),
            200,
            {"Content-Type":"application/json"}
            )
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakeries = []
    
    for bakery in Bakery.query.filter(Bakery.id==id).all():
        baked_goods = [baked_good.to_dict() for baked_good in bakery.baked_goods]
        bakery_dict = {
            "id": bakery.id,
            "name":bakery.name,    
            "baked_goods": baked_goods,
            "created_at": bakery.created_at,
                  
        }
        bakeries.append(bakery_dict)
        response = make_response(
            jsonify(bakeries[0]),
            200,
            {"Content-Type":"application/json"}
            )
    return response
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = []
    
    for baked_good in BakedGood.query.order_by(BakedGood.price).all():
        baked_good_dict = {
            "id":baked_good.id,
            "name":baked_good.name,
            "price":baked_good.price,
            "bakery_id":baked_good.bakery_id,
            "created_at":baked_good.created_at,
            "updated_at":baked_good.updated_at
        }
        baked_goods.append(baked_good_dict)
        response = make_response(
            jsonify(baked_goods),
            200,
            {"Content-Type":"application/json"}
        )    
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_goods = []
    
    for baked_good in BakedGood.query.order_by(desc(BakedGood.price)).limit(1).all():
        baked_good_dict = {
            "id":baked_good.id,
            "name":baked_good.name,
            "price":baked_good.price,
            "bakery_id":baked_good.bakery_id,
            "created_at":baked_good.created_at,
            "updated_at":baked_good.updated_at
        }
        baked_goods.append(baked_good_dict)
        response = make_response(
            jsonify(baked_goods[0]),
            200,
            {"Content-Type":"application/json"}
        )    
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
