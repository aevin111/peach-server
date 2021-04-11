import os
import json

from flask import jsonify


class SensorInternal:
    def set_field_capacity(self, field_capacity):
        try:
            from redis import StrictRedis
            r = StrictRedis(host='localhost', port=6379, db=0)
            r.set('field_capacity', int(field_capacity))
            return jsonify({"message": 'Successfully set new field capacity'})
        except ModuleNotFoundError:
            with open('sensor_val.json', 'w') as json_file:
                json.dump({'field_capacity': int(field_capacity)}, json_file)
                return jsonify({"message": 'Successfully set new field capacity'})

