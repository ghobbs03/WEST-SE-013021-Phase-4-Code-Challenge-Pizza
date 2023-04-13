#!/usr/bin/env python3
from random import choice as rc
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

with app.app_context():

# This will delete any existing rows
# so you can run the seed file multiple times without having duplicate entries in your database
    print("Deleting data...")
    Pizza.query.delete()
    Restaurant.query.delete()
    RestaurantPizza.query.delete()

    print("Creating restaurants...")
    shack = Restaurant(name = "Karen's Pizza Shack", address = 'address1')
    bistro = Restaurant(name = "Sanjay's Pizza", address = 'address2')
    palace = Restaurant(name = "Kiki's Pizza", address = 'address3')
    restaurants = [shack, bistro, palace]

    print("Creating pizzas...")
    db.session.add_all(restaurants)
    db.session.commit()


    cheese = Pizza(name = "Emma", ingredients = "Dough, Tomato Sauce, Cheese")
    pepperoni = Pizza(name = "Geri", ingredients = "Dough, Tomato Sauce, Cheese, Pepperoni")
    california = Pizza(name = "Melanie", ingredients = "Dough, Sauce, Ricotta, Red peppers, Mustard")
    pizzas = [cheese, pepperoni, california]

    db.session.add_all(pizzas)
    db.session.commit()

    print("Creating RestaurantPizza...")

    pr1 = RestaurantPizza(restaurant_id = shack.id, pizza_id = cheese.id, price = 1)
    pr2 = RestaurantPizza(restaurant_id = bistro.id, pizza_id  = pepperoni.id, price = 4)
    pr3 = RestaurantPizza(restaurant_id = palace.id, pizza_id = california.id, price = 5)
    restaurantPizzas = [pr1, pr2, pr3]
   
    
    db.session.add_all(restaurantPizzas)
    db.session.commit()
    

    print("Seeding done!")