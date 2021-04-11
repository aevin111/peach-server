import flask_restful

from internal.crop_internal import CropInternal


class Crop(flask_restful.Resource):
    def __init__(self):
        self._crop_internal = CropInternal()

    def post(self):
        return self._crop_internal.create_crop(flask_restful.request.headers)

    def get(self):
        action = flask_restful.request.args.get('action')
        if action == 'get_all_crops':
            return self._crop_internal.get_crops()
        elif action == 'search_for_crop':
            return self._crop_internal.search_for_crop(flask_restful.request.args.get('search_string'))
        else:
            return flask_restful.abort(400, message='Invalid request')

    def delete(self):
        return self._crop_internal.delete_crop(flask_restful.request.headers['crop_id'])

