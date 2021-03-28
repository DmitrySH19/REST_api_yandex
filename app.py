from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask_swagger_ui import get_swaggerui_blueprint
import simplejson as json
from flask_api import status
from json_tool import json_vadation, json_vadation_orders, json_validate
from db_conf import MyDatabase
#from sql_alc import sql_insert,sql_patch,inset_orders, assign_orders,complete_orders,valid_id_courier,validate_order_courier
from config import databaseFile, SQLITE
from sql_alc import sqlite_connector
from flask_expects_json import expects_json
app = Flask(__name__)
# app.config.from_object(Config)

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
database = MyDatabase(SQLITE, dbname=databaseFile)
sql_conn = sqlite_connector(db_obj=database)
json_validator = json_validate()


@app.route('/couriers', methods=['POST'])
def post_couriers():
    print('complete')
    validation_res = json_validator.validate(request)
    if not validation_res:
        insert_ids = sql_conn.insert_couers(json_response=request.json)
        return make_response(jsonify({'couriers': insert_ids}), 201)
    else:
        return make_response(jsonify({'validation_error': {'couriers': validation_res}}), 400)
    return abort(400)


@app.route('/couriers/<int:courier_id>', methods=['PATCH'])
@expects_json(json_validator.get_schema('/couriers/'))
def patch_courier(courier_id):

    result = sql_conn.patch_courier(request.json, courier_id)
    if result:
        return jsonify(result), 200
    else:
        return abort(400)


@app.route('/orders', methods=['POST'])
def post_orders():

    validation_res = json_validator.validate(request)
    if not validation_res:
        ins_ids = sql_conn.insert_orders(request.json)
        return make_response(jsonify({'orders': ins_ids}), 201)
    else:
        return make_response(jsonify({'validation_error': {'orders': validation_res}}), 400)


@app.route('/orders/assign', methods=['POST'])
def orders_assign():

    answer = sql_conn.assign_orders(request.json)
    print(answer)
    if answer:
        return make_response(jsonify(answer), 200)
    else:
        return abort(400)


@app.route('/orders/complete', methods=['POST'])
def orders_complete():

    answer = sql_conn.complete_orders(request.json)
    if answer:
        return make_response(jsonify(answer), 200)
    else:
        return abort(400)


@app.route('/couriers/<int:courier_id>', methods=['GET'])
def get_courier(courier_id):
    courier = sql_conn.get_courier(courier_id)
    return make_response(jsonify(courier))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
