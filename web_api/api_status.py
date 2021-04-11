import flask_restful

from internal.api_status_internal import APIStatusInternal


class APIStatus(flask_restful.Resource):
    def __init__(self):
        self._api_status_internal = APIStatusInternal()

    def get(self):
        return self._api_status_internal.get_status(flask_restful.request.headers['password'])

