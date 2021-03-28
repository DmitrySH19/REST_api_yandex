import jsonschema
import simplejson as json
import json
from openapi_schema_validator import oas30_format_checker


class json_validate():
    def __init__(self, path='static/openapi.json'):
        with open(path, 'r') as f:
            self.schema = json.loads(f.read())

    def validate(self, request):
        code = request.url[19:]
        # json_obj = request.

        if 'data' in request.json.keys():
            json_obj = request.json['data']

        schema = self.get_schema(code)
        print('code:', code)
        print('json:', json_obj)
        print('schema:', schema)
        mis_validate = []
        val_res = False
        for data in json_obj:
            try:
                jsonschema.validate(data, schema)
            except:
                val_res = True
                if code == '/couriers' or code == '/orders':
                    mis_validate.append({'id': tuple(data.values())[0]})
        print("mis_va", mis_validate)
        if mis_validate:
            return mis_validate
        else:
            return val_res

    def get_schema(self, code):
        if code == '/couriers':
            return self.schema["components"]["schemas"]["CourierItem"]
        elif code == ('/couriers/'):
            return self.schema["components"]["schemas"]["CourierUpdateRequest"]
        elif code == '/orders':
            return self.schema["components"]["schemas"]["OrderItem"]


class json_vadation():
    def __init__(self, response, code, path='static/openapi.json'):
        self.code = code
        self.json_obj = response
        with open(path, 'r') as f:
            schema_data = f.read()
        schema = json.loads(schema_data)
        self.schema = schema["components"]["schemas"]["CourierItem"]

    def json_validate(self):
        if self.code == 'POST':
            mis_validate = []
            for data in self.json_obj['data']:
                try:
                    jsonschema.validate(data, self.schema)
                except:
                    mis_validate.append({'id': data['courier_id']})

            return mis_validate
        elif self.code == 'PATCH':
            try:
                if 'courier_type' in self.json_obj.keys():
                    jsonschema.validate(
                        self.json_obj['courier_type'], self.schema['properties']['courier_type'])
                if 'regions' in self.json_obj.keys():
                    jsonschema.validate(
                        self.json_obj['regions'], self.schema['properties']['regions'])
                if 'working_hours' in self.json_obj.keys():
                    jsonschema.validate(
                        self.json_obj['working_hours'], self.schema['properties']['working_hours'])
                return True
            except:
                return False


class json_vadation_orders():
    def __init__(self, response, path='static/openapi.json'):
        self.json_obj = response
        with open(path, 'r') as f:
            schema_data = f.read()
        schema = json.loads(schema_data)
        self.schema = schema["components"]["schemas"]["OrderItem"]

    def json_validate(self):
        mis_validate = []
        for data in self.json_obj['data']:
            if float(data['weight']) < 0.01 or float(data['weight']) > 50:
                mis_validate.append({'id': data['order_id']})
                continue
            try:
                jsonschema.validate(data, self.schema)
            except:
                mis_validate.append({'id': data['order_id']})

        return mis_validate
