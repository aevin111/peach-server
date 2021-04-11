import json
import os

import flask_restful

from internal.sensor_internal import SensorInternal


class Sensor(flask_restful.Resource):
    def get(self):
        action = flask_restful.request.args.get('action')
        if action == 'get_field_capacity':
            if os.path.isfile('sensor_val.json'):
                with open('sensor_val.json', 'r') as json_file:
                    data = json.load(json_file)
                    return data

    def put(self):
        action = flask_restful.request.args.get('action')
        if action == 'set_field_capacity':
            internal = SensorInternal()
            headers = flask_restful.request.headers
            return internal.set_field_capacity(int(headers['field_capacity']))

