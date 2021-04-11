from flask import jsonify
import flask_restful

from lib.sqlite_database import SQLiteDatabase
from lib.sqlite_data_fetcher import SQLiteDataFetcher


class PlantInternal:
    def __init__(self):
        self._fetcher = SQLiteDataFetcher('db')

    def get_plants_list(self):
        statement = """SELECT * FROM plants"""
        data = self._fetcher.fetch_data(statement, ())
        return jsonify(data)

    def get_plant_info(self, plant_id):
        statement = """SELECT * FROM plants WHERE plant_id = ?"""
        parameters = (str(plant_id))
        data = self._fetcher.fetch_data(statement, parameters)
        if data == None:
            flask_restful.abort(404, message='Plant not found. Maybe you should plant it?')
        else:
            return jsonify(data)

    def search_for_plant(self, search_string):
        statement = """SELECT * FROM plants WHERE name LIKE ?"""
        parameters = ('%' + str(search_string) + '%',)
        data = self._fetcher.fetch_data(statement, parameters)
        if data == None:
            flask_restful.abort(404, message='Plant not found. Maybe you should plant it?')
        else:
            return jsonify(data)

    def get_summarized_plants_list(self):
        statement = """SELECT plant_id, name, category, time_planting FROM plants"""
        data = self._fetcher.fetch_data(statement, ())
        return jsonify(data)

