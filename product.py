# Importing modules
from flask import Flask, render_template, request, jsonify, redirect, session
from flask import abort
from flask_cors import CORS, cross_origin
from flask import make_response, url_for
import json
import random
from pymongo import MongoClient
from time import gmtime, strftime


# Object creation
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'w6d4w654d6w1d8we1rt63561fwe1fe165'
CORS(app)

# connection to MongoDB Database
connection = MongoClient("mongodb://localhost:27017/")

def create_mongodatabase():
    try:
        dbnames = connection.database_names()
        if 'Products_Application' not in dbnames:
            db = connection.Products_Application.users
            db_products = connection.Products_Application.products
            db_ratings = connection.Products_Application.ratings
            db_api = connection.Products_Application.apirelease

            db.insert({
            "email": "eric.strom@google.com",
            "id": 33,
            "name": "Eric stromberg",
            "password": "eric@123",
            "username": "eric.strom"
            })

            db_products.insert({
            "id":18,
            "name":"Skittles",
            "category":"confectionery",
            "rrp":1.00,
            "description":"Just skittles init",
            "weight":200,
            "image":"https://assets.sainsburys-groceries.co.uk/gol/2765334/1/640x640.jpg"
            })

            db_products.insert({
            "id":17,
            "name":"Oreo",
            "category":"confectionery",
            "rrp":0.98,
            "description":"Just oreos init",
            "weight":125,
            "image":"https://target.scene7.com/is/image/Target/GUEST_0679b9d3-9a7f-4ddb-a957-6f7eb5f7d63f?wid=488&hei=488&fmt=pjpeg"
            })

            db_ratings.insert({
            "id":1,
            "rating":5,
            "comment":"Good product, taste like a rainbow",
            "product_id":18
            })

            db_ratings.insert({
            "id":2,
            "rating":4,
            "comment":"Good product, i like the cream",
            "product_id":17
            })

            db_api.insert( {
              "buildtime": "2017-01-01 10:00:00",
              "links": "/api/v1/products",
              "methods": "get, post, put, delete",
              "version": "v1"
            })

            print ("Database Initialize completed!")
        else:
            print ("Database already Initialized!")
    except:
        print ("Database creation failed!!")

#List products function and handler
def list_products():
    api_list=[]
    db = connection.Products_Application.products
    for row in db.find({},{'_id':0}):
        api_list.append(row)
    # print (api_list)
    return jsonify({'products_list': api_list})

# List specific product
def list_product(product_id):
    db = connection.Products_Application.products
    api_list=[]
    product = db.find({'id':product_id})
    for i in product:
        api_list.append(str(i))
    if api_list == []:
        abort(404)
    return jsonify({'product': api_list})

#list products by category
def list_product_category(product_categroy):
    db = connection.Products_Application.products
    api_list=[]
    for row in db.find({'category':product_categroy}):
        api_list.append(str(row))
    return jsonify({'products_list':api_list})

@app.route('/api/v1/products', methods=['GET'])
def get_products():
    return list_products()

@app.route('/api/v1/products/<int:id>', methods=['GET'])
def get_product(id):
    return list_product(id)

@app.route('/api/v1/products/<string:category>', methods=['GET'])
def get_product_category(category):
    return list_product_category(category)

#List ratings function and handler
def list_ratings():
    api_list=[]
    db = connection.Products_Application.ratings
    for row in db.find():
        api_list.append(str(row))
    # print (api_list)
    return jsonify({'ratings_list': api_list})

@app.route('/api/v1/ratings', methods=['GET'])
def get_ratings():
    return list_ratings()

@app.route('/api/v1/ratings', methods=['POST'])
def create_rating():
    print(request.json)
    if not request.json or not 'product_id' in request.json or not 'rating' in request.json:
        abort(400)
    print(request.json)
    rating = {
        'product_id': int(request.json['product_id']),
        'rating': int(request.json['rating']),
        'comment': request.json.get('comment',""),
        'id': random.randint(1,1000)
    }
    return jsonify({'status': add_rating(rating)}), 201

def add_rating(new_rating):
    db = connection.Products_Application.ratings
    db.insert(new_rating)
    return "Success"

#list ratings by product
def list_ratings_product(product_id):
    db = connection.Products_Application.ratings
    api_list=[]
    for row in db.find({'product_id':product_id},{'_id':0}):
        api_list.append(str(row))
    return jsonify({'ratings_list':api_list})

@app.route('/api/v1/ratings/<int:product_id>')
def get_ratings_by_product(product_id):
    return list_ratings_product(product_id)

#List releases function and handler
def list_versions():
    api_list=[]
    db = connection.Products_Application.apirelease
    for row in db.find():
        api_list.append(str(row))
    # print (api_list)
    return jsonify({'info_list': api_list})

@app.route('/api/v1/info', methods=['GET'])
def get_versions():
    return list_versions()

# Error handling
@app.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({'error': 'Resource not found!'}), 404)

@app.errorhandler(409)
def user_found(error):
    return make_response(jsonify({'error': 'Conflict! Record exist'}), 409)

@app.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@app.route('/products')
def load_product():
    return render_template('products.html')

@app.route('/review/<int:id>')
def load_review(id):
    db = connection.Products_Application.products
    api_list=[]
    product = db.find({'id':id})
    return render_template('review.html',id=id,name=product[0]['name'])

# Main Function
if __name__ == '__main__':
    create_mongodatabase()
    app.run(host='0.0.0.0', port=5000, debug=True)
