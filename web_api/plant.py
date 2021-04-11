
import flask_restful

from internal.plant_internal import PlantInternal


class Plant(flask_restful.Resource):
    def __init__(self):
        self._action = flask_restful.request.args.get('action')
        self._plant_internal = PlantInternal()

    def get(self):
        if self._action == 'get_plants_list':
            return self._plant_internal.get_plants_list()
        elif self._action == 'get_plant_info':
            return self._plant_internal.get_plant_info(flask_restful.request.args.get('plant_id'))
        elif self._action == 'search_for_plant':
            return self._plant_internal.search_for_plant(flask_restful.request.args.get('search_string'))
        elif self._action == 'get_summarized_plants_list':
            return self._plant_internal.get_summarized_plants_list()
        else:
            return flask_restful.abort(400, message='Invalid request')

