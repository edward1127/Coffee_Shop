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
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()


'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks')
def drinks_short_form():
    short_form = [drink.short() for drink in Drink.query.all()]
    if len(short_form) == 0:
      abort(404)
    return jsonify({
        "success": True,
        "status_code": 200,
        "status_message": 'OK',
        "drinks": short_form
      }) 

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def drinks_long_form():
    long_form = [drink.long() for drink in Drink.query.all()]
    if len(long_form) == 0:
      abort(404)
    return jsonify({
        "success": True,
        "status_code": 200,
        "status_message": 'OK',
        "drinks": long_form
      }) 

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks():

    title = request.json.get('title', None)
    recipe = request.json.get('recipe', None)

    if (title is None) or (recipe is None): 
        abort(422)
    else:
        try: 
            new_drink = Drink(title=title, recipe=json.dumps(recipe))
            new_drink.insert()

            return jsonify({
                'success': True, 
                "status_code": 200,
                "status_message": 'OK',
                'drinks': [new_drink.long()]
            })

        except: 
            abort(500)

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drinks(id):

    title = request.json.get('title', None)
    recipe = request.json.get('recipe', None)
    target_drink = Drink.query.filter(Drink.id == id).one_or_none()

    if (target_drink is None): 
        abort(404)
    elif (title is None) and (recipe is None):
        abort(422)
    else:
        try: 
            target_drink.title = title
            target_drink.recipe = json.dumps(recipe) 
            target_drink.update()
            return jsonify({
                'success': True, 
                "status_code": 200,
                "status_message": 'OK',
                'drinks': [target_drink.long()]
            })

        except: 
            abort(500)

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''

@app.route("/drinks/<int:id>", methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(id):

    target_drink = Drink.query.filter(Drink.id == id).one_or_none()

    if (target_drink is None): 
        abort(404)
    else: 
        try: 
            target_drink.delete()

            return jsonify({
                'success': True, 
                "status_code": 200,
                "status_message": 'OK',
                "delete": id,
            })
        except: 
            abort(500)

## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource Not found"
    }), 404

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server Error"
    }), 500
'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def auth_error(e):
    return jsonify(e.error), e.status_code