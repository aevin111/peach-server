import flask_restful

from internal.sensor_status_reporter_internal import SensorStatusReporterInternal


class SensorStatusReporter(flask_restful.Resource):
    def __init__(self):
        self._sensor_status_reporter_internal = SensorStatusReporterInternal()

    def post(self):
        return self._sensor_status_reporter_internal.report(flask_restful.request.headers['level'])

