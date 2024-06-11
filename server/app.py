#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

class Restaurants(Resource):
    def get(self):
        restaurants = [restaurant.to_dict(rules=('-restaurant_pizzas',)) for restaurant in Restaurant.query.all()]
        return make_response(restaurants)
    
api.add_resource(Restaurants,'/restaurants')

class RestaurantById(Resource):
    def get(self, id):
        restaurant = db.session.get(Restaurant, id)
        if not restaurant:
            return make_response({"error": "Restaurant not found"}, 404)
        return(restaurant.to_dict())
    
    def delete(self, id):
        restaurant = db.session.get(Restaurant, id)
        if not restaurant:
            return make_response({"error": "Restaurant not found"}, 404)
        
        db.session.delete(restaurant)
        db.session.commit()
        return make_response({},204)
    
api.add_resource(RestaurantById,'/restaurants/<int:id>')

class Pizzas(Resource):
    def get(self):
        pizzas = [pizza.to_dict() for pizza in Pizza.query.all()]
        return make_response(pizzas)       
    
api.add_resource(Pizzas,'/pizzas')

class RestaurantPizzas(Resource):
      def post(self):
        data=request.json  
        try:
            pizza= RestaurantPizza(price=data['price'], pizza_id=data['pizza_id'], restaurant_id=data['restaurant_id'])
            db.session.add(pizza)
            db.session.commit()
            return make_response(pizza.to_dict(), 201)
        except ValueError:
            return make_response({"errors": ["validation errors"]}, 400)
                  
api.add_resource(RestaurantPizzas,'/restaurant_pizzas')


if __name__ == "__main__":
    app.run(port=5555, debug=True)
