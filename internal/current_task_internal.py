from datetime import datetime
import json
from os import path

from flask import jsonify
import flask_restful

from lib.sqlite_data_fetcher import SQLiteDataFetcher


class CurrentTaskInternal:
    def _get_tasks(self, day, plant_id):
        fetcher = SQLiteDataFetcher('db')
        statement = """SELECT time, description, time_frame FROM tasks WHERE plant_id = ? AND day = ?"""
        parameters = (plant_id, day)
        task_data = jsonify(fetcher.fetch_data(statement, parameters))
        return json.loads(task_data.get_data().decode("utf-8"))

    def _open_current_crop_json(self):
        if path.isfile('ccrop.json'):
            with open('ccrop.json', 'r') as json_file:
                data = json.load(json_file)
            return data
        else:
            return None      

    def get_current_task(self, date):
        crop_json = self._open_current_crop_json()
        plant_date = datetime.strptime(crop_json['plant_date'], '%Y-%m-%d %H:%M:%S.%f')
        if date == 'today':
            requested_date = datetime.now()
        else:
            requested_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
        day = int((requested_date - plant_date).days)
        task_data = self._get_tasks(day, crop_json['plant_id'])
        if task_data == None:
            return flask_restful.abort(404, message='No tasks found')
        else:
            return jsonify(task_data)

