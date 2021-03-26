from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask_swagger_ui import get_swaggerui_blueprint
import simplejson as json
from flask_api import status
from json_tool import json_vadation ,json_vadation_orders
from db_conf import MyDatabase
#from sql_alc import sql_insert,sql_patch,inset_orders, assign_orders,complete_orders,valid_id_courier,validate_order_courier
from config import databaseFile, SQLITE
from sql_alc import sqlite_connector

app = Flask(__name__)
#app.config.from_object(Config)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/openapi.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Seans-Python-Flask-REST-Boilerplate"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
# loads database obj 
database  =  MyDatabase(SQLITE, dbname=databaseFile)
sql_conn = sqlite_connector(db_obj = database)

@app.route('/couriers', methods=['POST'])
def post_couriers():
    validation_res = json_vadation(request.json,code = 'POST').json_validate()
    if len(validation_res) == 0:
        insert_ids = sql_conn.insert_couers(json_response = request.json)
        return make_response(jsonify({'couriers':insert_ids}),201)
    else:
        return make_response(jsonify({'validation_error': {'couriers':validation_res}}), 400)

@app.route('/couriers/<int:courier_id>', methods=['PATCH'])
def patch_courier(courier_id):
    if json_vadation(request.json,code = 'PATCH').json_validate():
        result = sql_conn.patch_courier(request.json,courier_id)
        if result:
            return jsonify(result), 200   
        else:
            return  abort(400)
    else:
        return abort(400)

@app.route('/orders', methods=['POST'])
def post_orders():

    validation_res = json_vadation_orders(request.json).json_validate()
    if len(validation_res) == 0:
        ins_ids = sql_conn.insert_orders(request.json)
        return make_response(jsonify({'orders':ins_ids}),201)
    else:
        return make_response(jsonify({'validation_error': {'orders':validation_res}}), 400)

@app.route('/orders/assign', methods=['POST'])
def orders_assign():
    
    answer = sql_conn.assign_orders(request.json)
    print(answer)
    if answer:
        return make_response(jsonify(answer),200)
    else:
        return abort(400)
    
@app.route('/orders/complete', methods=['POST'])
def orders_complete():


    answer = sql_conn.complete_orders(request.json)
    if answer:
        return make_response(jsonify(answer),200)
    else:
        return abort(400)
    # print(request.json)
    # if validate_order_courier(request.json,session=loadSession()):
    #     return make_response(jsonify({"order_id":request.json['order_id']}))
    # else:
    # #complete_orders(request.json,session=loadSession())
    #     return abort(400)



# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)



# @app.route('/orders/assign', methods=['POST'])
# def orders_assign():
#     if valid_id_courier(request.json["courier_id"],session=loadSession()):
#         ans = assign_orders(request.json,session=loadSession())
#         return make_response(jsonify(ans),200)
#     else:
#         return abort(400)

# @app.route('/orders/complete', methods=['POST'])
# def orders_complete():
#     print(request.json)
#     if validate_order_courier(request.json,session=loadSession()):
#         return make_response(jsonify({"order_id":request.json['order_id']}))
#     else:
#     #complete_orders(request.json,session=loadSession())
#         return abort(400)
    


# @app.route('/couriers/<int:courier_id>', methods=['PATCH'])
# def patch_courier(courier_id):
#     if json_vadation(request.json,code = 'PATCH').json_validate():
#         res = sql_patch(request.json,courier_id,session=loadSession())
#         return jsonify(res), 200   
#     return  abort(400)


if __name__ == '__main__':
    app.run(debug=True)
