"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt_identity
)
import os
from fakePressure import data
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, User, Products, Orders, Magfield, Tempfield, Atmopressure, Axismeasure


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)


# Provide a method to create access tokens. The create_jwt()
# function is used to actually generate the token
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    params = request.get_json()
    email = params.get('email', None)
    password = params.get('password', None)

    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if email != 'test' or password != 'test':
        return jsonify({"msg": "Bad email or password"}), 401

    # Identity can be any data that is json serializable
    ret = {'jwt': create_jwt(identity=email)}
    return jsonify(ret), 200
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['POST', 'GET'])
def handle_user():
    """
    Create user and retrieve all users
    """

    # POST request
    if request.method == 'POST':
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'username' not in body:
            raise APIException('You need to specify the username', status_code=400)
        if 'email' not in body:
            raise APIException('You need to specify the email', status_code=400)
        if 'orders' not in body:
            raise APIException('You need to specify the orders', status_code=400)
        if 'name' not in body:
            raise APIException('You need to specify the name', status_code=400)
        if 'isAdmin' not in body:
            raise APIException('You need to specify the isAdmin', status_code=400)
        if 'country' not in body:
            raise APIException('You need to specify the country', status_code=400)
        if 'state' not in body:
            raise APIException('You need to specify the state', status_code=400)
        if 'city' not in body:
            raise APIException('You need to specify the city', status_code=400)
        if 'address' not in body:
            raise APIException('You need to specify the address', status_code=400)
        if 'zipcode' not in body:
            raise APIException('You need to specify the zipcode', status_code=400)
        if 'password_hash' not in body:
            raise APIException('You need to specify the password_hash', status_code=400)

        user1 = User(username=body['username'], email=body['email'])
        db.session.add(user1)
        db.session.commit()
        return "ok", 200

    # GET request
    if request.method == 'GET':
        all_user= User.query.all()
        all_user = list(map(lambda x: x.serialize(), all_user))
        return jsonify(all_user), 200

    return "Invalid Method", 404


@app.route('/Orders', methods=['POST', 'GET'])
def handle_orders():

    if request.method == 'POST':
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'username' not in body:
            raise APIException('You need to specify the username', status_code=400)
        if 'purchase_date' not in body:
            raise APIException('You need to specify the purchase_date', status_code=400)
        if 'confirmation_number' not in body:
            raise APIException('You need to specify the confirmation_number', status_code=400)
        if 'user_id' not in body:
            raise APIException('You need to specify the user_id', status_code=400)
        if 'products' not in body:
            raise APIException('You need to specify the products', status_code=400)
    return "Invalid Method", 404

@app.route('/products', methods=[ 'GET', 'POST'])
def handle_products():

    if request.method == 'POST':
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'plan_name' not in body:
            raise APIException('You need to specify the plan_name', status_code=400)
        if 'price' not in body:
            raise APIException('You need to specify the price', status_code=400)
        if 'orders_id' not in body:
            raise APIException('You need to specify the orders_id', status_code=400)
        if 'mag_f' not in body:
            raise APIException('You need to specify the mag_f', status_code=400)
        if 'temp' not in body:
            raise APIException('You need to specify the temp', status_code=400)
        if 'atmo_pressure' not in body:
            raise APIException('You need to specify the atmo_pressure', status_code=400)
        if 'axis_measure' not in body:
            raise APIException('You need to specify the axis_measure', status_code=400)
        return "Invalid Method", 404

    if request.method == 'GET':
        all_products = Products.query.all()
        all_products = list(map(lambda x: x.serialize(), all_products))
    return jsonify(all_products), 200






@app.route('/products/<int:products_id>', methods=['PUT', 'GET', 'DELETE'])
def get_single_user(products_id):
    """
    Single products
    """

    # PUT request
    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)

        user1 = User.query.get(products_id)
        if user1 is None:
            raise APIException('Products not found', status_code=404)

        if "username" in body:
            user1.username = body["username"]
        if "email" in body:
            user1.email = body["email"]
        db.session.commit()

        return jsonify(user1.serialize()), 200

    # GET request
    if request.method == 'GET':
        products1 = Products.query.get(products_id)
        if user1 is None:
            raise APIException('Products not found', status_code=404)
        return jsonify(products1.serialize()), 200

    # DELETE request
    if request.method == 'DELETE':
        products1 = Products.query.get(products_id)
        if products1 is None:
            raise APIException('Product not found', status_code=404)
        db.session.delete(products1)
        db.session.commit()
        return "ok", 200

    return "Invalid Method", 404



@app.route('/pressure', methods=['GET'])
@jwt_required
def get_single_all_data():

    return jsonify(data)

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT)
