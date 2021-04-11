import flask_restful

from internal.current_task_internal import CurrentTaskInternal


class CurrentTask(flask_restful.Resource):
    def __init__(self):
        self._current_task_internal = CurrentTaskInternal()

    def get(self):
        return self._current_task_internal.get_current_task(flask_restful.request.args.get('date'))

