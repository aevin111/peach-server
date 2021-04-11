from datetime import datetime
import json
import os

import flask
from flask import jsonify
import flask_restful

from lib.sqlite_database import SQLiteDatabase
from lib.sqlite_data_fetcher import SQLiteDataFetcher


class CropInternal:
    def _is_current_crop(self, crop_id):
        if os.path.isfile('ccrop.json'):
            with open('ccrop.json', 'r') as json_file:
                data = json.load(json_file)
            if str(data['crop_id']) == str(crop_id):
                return True
            else:
                return False
        else:
            return flask_restful.abort(404, message='No crop currently set')

    def create_crop(self, headers):
        statement = """INSERT INTO crops VALUES (?, ?, ?, ?)"""
        now = datetime.now()
        parameters = (None, int(headers['plant_id']), str(headers['name']), str(now))
        database = SQLiteDatabase('db')
        success = database.execute_update(statement, parameters)
        if success:
            return jsonify({"message": 'Successfully added new crop'})
        else:
            return flask_restful.abort(500, message='Failed to perform request due to a database error')

    def get_crops(self):
        statement = """SELECT * FROM crops"""
        fetcher = SQLiteDataFetcher('db')
        data = fetcher.fetch_data(statement, ())
        return jsonify(data)

    def search_for_crop(self, search_string):
        statement = """SELECT * FROM crops WHERE name LIKE ?"""
        parameters = ('%' + str(search_string) + '%',)
        fetcher = SQLiteDataFetcher('db')
        data = fetcher.fetch_data(statement, parameters)
        if data == None:
            return flask_restful.abort(404, message='Crop not found')
        else:
            return jsonify(data)

    def delete_crop(self, crop_id):
        if self._is_current_crop(crop_id):
            return flask.abort(400, 'Crop is set as current crop')
        else:
            statement = """DELETE FROM crops WHERE crop_id = ?"""
            parameters = (crop_id)
            database = SQLiteDatabase('db')
            success = database.execute_update(statement, parameters)
            if success:
                return jsonify({"message": 'Successfully deleted crop!'})
            else:
                return flask.abort(500, message='Failed to perform request due to a database error')

