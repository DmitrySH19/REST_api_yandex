import jsonschema
import simplejson as json

class json_vadation():
    def __init__(self,response, code ,path = 'static/openapi.json'):
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
                    jsonschema.validate(self.json_obj['courier_type'],self.schema['properties']['courier_type'])
                if 'regions' in self.json_obj.keys():
                    jsonschema.validate(self.json_obj['regions'],self.schema['properties']['regions'])
                if 'working_hours' in self.json_obj.keys():
                    jsonschema.validate(self.json_obj['working_hours'],self.schema['properties']['working_hours'])
                return True
            except:
                return False

class json_vadation_orders():
    def __init__(self,response ,path = 'static/openapi.json'):
        self.json_obj = response
        with open(path, 'r') as f:
            schema_data = f.read()
        schema = json.loads(schema_data)
        self.schema = schema["components"]["schemas"]["OrderItem"]

    def json_validate(self):
        mis_validate = []
        for data in self.json_obj['data']:
            if float(data['weight'])< 0.01 or float(data['weight']) > 50:
                mis_validate.append({'id': data['order_id']})
                continue
            try:
                jsonschema.validate(data, self.schema)
            except:
                mis_validate.append({'id': data['order_id']})

        return mis_validate


