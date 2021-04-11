import json

from flask import jsonify

class SensorStatusReporterInternal:
    def report(self, level):
        with open("sensor.json", "r") as json_file:
            data = json.load(json_file)
        data['moisture'] = level
        with open("sensor.json", "w") as json_file:
            json.dump(data, json_file)
        return jsonify('ok')

