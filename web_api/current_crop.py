import flask_restful

from internal.current_crop_internal import CurrentCropInternal


class CurrentCrop(flask_restful.Resource):
    def __init__(self):
        self._current_crop_internal = CurrentCropInternal()

    def delete(self):
        return self._current_crop_internal.delete_current_crop()

    def get(self):
        return self._current_crop_internal.get_current_crop()

    def post(self):
        return self._current_crop_internal.create_current_crop(flask_restful.request.headers)

