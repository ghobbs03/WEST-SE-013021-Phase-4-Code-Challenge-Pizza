#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api

from models import db, Restaurant, RestaurantPizza, Pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/restaurants')
def restaurants():
    restaurants = Restaurant.query.all()
    
    restaurants_dict = [restaurant.to_dict() for restaurant in restaurants]

    return make_response(restaurants_dict, 200)


@app.route('/restaurants/<int:id>', methods= ['GET', 'DELETE'])
def restaurants_by_id(id):
    restaurant = Restaurant.query.filter(Restaurant.id == id).first()

    if request.method == 'GET':

       
        if restaurant:
            response = make_response(restaurant.to_dict(rules=('pizzas',)), 200)
        else:
            response = make_response({"error": "Restaurant not found"}, 404)

    elif request.method == 'DELETE':
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
        else:
            response = make_response({"error": "Restaurant not found"}, 404)
    
    return response

@app.route('/pizzas')
def get_pizzas():
    pizzas = Pizza.query.all()
    pizza_dict = [pizza.to_dict() for pizza in pizzas]

    return make_response(pizza_dict, 201)


@app.route('/restaurant_pizzas', methods=['POST'])
def post_pizza():
    if request.method == 'POST':
        data = request.get_json()

        try:

            new_restaurant_pizza = RestaurantPizza(price=data['price'], pizza_id=data['pizza_id'], restaurant_id=data['restaurant_id'])
            db.session.add(new_restaurant_pizza)
            db.session.commit()

            response = make_response(new_restaurant_pizza.to_dict(rules=('-id', '-pizza_id', '-price','-restaurant','-restaurant_id')), 201)

        except Exception as e:
            response = make_response({"error": "Invalid input"}, 400)

    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
