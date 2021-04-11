import flask_restful

from internal.diseases_internal import DiseasesInternal


class Diseases(flask_restful.Resource):
    def __init__(self):
        self._action = flask_restful.request.args.get('action')
        self._diseases_internal = DiseasesInternal()

    def get(self):
        if self._action == 'get_symptoms':
            plant_id = flask_restful.request.args.get('plant_id')
            return self._diseases_internal.get_symptoms(plant_id)
        if self._action == 'get_disease':
            symptoms = flask_restful.request.args.get('symptoms')
            plant = flask_restful.request.args.get('plant_id')
            return self._diseases_internal.get_disease(symptoms, plant)

