from flask import Flask
from flask_restful import Api

from web_api.api_status import APIStatus
from web_api.crop import Crop
from web_api.current_crop import CurrentCrop
from web_api.current_task import CurrentTask
from web_api.diseases import Diseases
from web_api.plant import Plant
from web_api.sensor_status import SensorStatus
from web_api.sensor_status_reporter import SensorStatusReporter
from web_api.sensor import Sensor


class Main:
    def _load_apis(self, api):
        api.add_resource(APIStatus, '/api_status')
        api.add_resource(Crop, '/crop')
        api.add_resource(Plant, '/plant')
        api.add_resource(CurrentCrop, '/current_crop')
        api.add_resource(CurrentTask, '/current_task')
        api.add_resource(SensorStatus, '/sensor_status')
        api.add_resource(Diseases, '/diseases')
        api.add_resource(SensorStatusReporter, '/sensor_status_reporter')
        api.add_resource(Sensor, '/sensor')

    def main(self):
        app = Flask(__name__)
        api = Api(app)
        self._load_apis(api)
        app.run(debug=True, host='0.0.0.0', port=50001)


if __name__ == '__main__':
    main = Main()
    main.main()
