import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


'''
uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

# ROUTES

# public endpoint returning all drinks
@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        drinks = Drink.query.all()
        return jsonify({
            'success': True,
            'drinks': [drink.short() for drink in drinks]
        })
    except Exception as e:
        print(e)
        abort(404)


# endpoint returning drinks that requires authorization
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    try:
        drinks = Drink.query.all()
        return jsonify({
            'success': True,
            'drinks': [drink.long() for drink in drinks]
        })
    except Exception as e:
        print(e)
        abort(404)


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(payload):
    try:
        recipe = request.get_json()
        drink = Drink(title=recipe['title'], recipe=json.dumps(recipe['recipe']))
        drink.insert()
        return jsonify({
            'success': True,
            'drink': [drink.long()]
        })
    except Exception as e:
        print(e)
        abort(400)


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):
    try:
        updated_drink = request.get_json()
        updated_title = updated_drink.get('title')
        updated_recipe = updated_drink.get('recipe')
        drink = Drink.query.filter_by(id=id).first()
        if drink:
            if updated_title:
                drink.title = updated_title
            if updated_recipe:
                drink.recipe = json.dumps(updated_recipe)
            drink.update()
        else:
            print(id)
            abort(404)
        return jsonify({
            'success': True,
            'drink': [drink.long()]
        })
    except Exception as e:
        print(e)
        abort(400)


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('patch:drinks')
def delete_drink(payload, id):
    try:
        drink = Drink.query.filter_by(id=id).first()

        if drink:
            drink.delete()
        else:
            print(id)
            abort(404)
        return jsonify({
            'success': True,
            'drink': [drink.long()]
        })
    except Exception as e:
        print(e)
        abort(400)

# Error Handling
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
                    "success": False,
                    "error": 400,
                    "message": "bad request"
                    }), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
                    "success": False,
                    "error": 401,
                    "message": "unauthorized"
                    }), 401


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify(error.error), error.status_code


