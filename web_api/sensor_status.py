from flask_restful import Resource

from internal.sensor_status_internal import SensorStatusInternal


class SensorStatus(Resource):
    def __init__(self):
        self._sensor_status_internal = SensorStatusInternal()
        
    def get(self):
        return self._sensor_status_internal.get_moisture_level()

