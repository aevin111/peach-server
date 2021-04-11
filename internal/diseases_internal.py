import json
import os
import subprocess

from flask import jsonify
from flask_restful import abort

from lib.sqlite_database import SQLiteDatabase
from lib.sqlite_data_fetcher import SQLiteDataFetcher


class DiseasesInternal:
    def __init__(self):
        self._fetcher = SQLiteDataFetcher('db')

    def get_symptoms(self, plant_id):
        statement = """SELECT DISTINCT symptom FROM diseases WHERE plant_id = ?"""
        parameters = (str(plant_id))
        data = self._fetcher.fetch_data(statement, parameters)
        return jsonify(data)

    def get_disease(self, symptoms, plant_id):
        file_name =  'datasets' + '/' + plant_id + '.py'
        output = subprocess.run(['python2', file_name, symptoms], stdout=subprocess.PIPE).stdout
        json_string = json.loads(output.decode('utf8'))
        return jsonify(json_string)

