import os
import json

from flask import jsonify


class SensorStatusInternal:
    def get_moisture_level(self):
        try:
            from redis import StrictRedis
            r = StrictRedis(host='localhost', port=6379, db=0)
            return jsonify({'moisture_level': str(r.get('moist').decode("utf-8"))})
        except ModuleNotFoundError:
            if os.path.isfile('sensor.json'):
                with open('sensor.json', 'r') as json_file:
                    data = json.load(json_file)
                    return jsonify({'moisture_level': data['moisture']})

