from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask_swagger_ui import get_swaggerui_blueprint
import simplejson as json
from flask_api import status
from json_tool import json_vadation ,json_vadation_orders

from sqlalchemy import *
from sqlalchemy.orm import create_session
from sqlalchemy.schema import Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sql_alc import sql_insert,sql_patch,inset_orders, assign_orders,complete_orders,valid_id_courier,validate_order_courier
from db_conf import Base,engine


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




def loadSession():
    """"""
    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


@app.route('/couriers', methods=['POST'])
def post_couriers():
    validation_res = json_vadation(request.json,code = 'POST').json_validate()
    if len(validation_res) == 0:
        ins_ids = sql_insert(request.json['data'],session=loadSession())
        return make_response(jsonify({'couriers':ins_ids}),201)
    else:
        return make_response(jsonify({'validation_error': {'couriers':validation_res}}), 400)



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/orders', methods=['POST'])
def post_orders():

    validation_res = json_vadation_orders(request.json).json_validate()
    if len(validation_res) == 0:
        ins_id = inset_orders(request.json['data'],session=loadSession())
        return make_response(jsonify({'orders':ins_id}),201)
    else:
        return make_response(jsonify({'validation_error': {'couriers':validation_res}}), 400)

@app.route('/orders/assign', methods=['POST'])
def orders_assign():
    if valid_id_courier(request.json["courier_id"],session=loadSession()):
        ans = assign_orders(request.json,session=loadSession())
        return make_response(jsonify(ans),200)
    else:
        return abort(400)

@app.route('/orders/complete', methods=['POST'])
def orders_complete():
    print(request.json)
    if validate_order_courier(request.json,session=loadSession()):
        return make_response(jsonify({"order_id":request.json['order_id']}))
    else:
    #complete_orders(request.json,session=loadSession())
        return abort(400)
    


@app.route('/couriers/<int:courier_id>', methods=['PATCH'])
def patch_courier(courier_id):
    if json_vadation(request.json,code = 'PATCH').json_validate():
        res = sql_patch(request.json,courier_id,session=loadSession())
        return jsonify(res), 200   
    return  abort(400)


if __name__ == '__main__':
    app.run(debug=True)
