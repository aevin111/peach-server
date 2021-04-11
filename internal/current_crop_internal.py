import json
import os

from flask import jsonify
import flask_restful

from lib.sqlite_database import SQLiteDatabase
from lib.sqlite_data_fetcher import SQLiteDataFetcher


class CurrentCropInternal:
    def _get_plant_data(self, plant_id):
        fetcher = SQLiteDataFetcher('db')
        statement = """SELECT image_url, name, category, maturity_integer FROM plants WHERE plant_id = ?"""
        parameters = (plant_id)
        data = fetcher.fetch_data(statement, parameters)
        if data == None:
            return None
        else:
            return jsonify(data)     

    def _get_plant_data_json(self, plant_id):
        plant_data = self._get_plant_data(plant_id)
        return json.loads(plant_data.get_data().decode("utf-8"))[0]

    def _get_crop_data_json(self, crop_id):
        fetcher = SQLiteDataFetcher('db')
        statement = """SELECT plant_id, name, plant_date FROM crops WHERE crop_id = ?"""
        parameters = (crop_id)
        crop_data = jsonify(fetcher.fetch_data(statement, parameters))
        return json.loads(crop_data.get_data().decode("utf-8"))[0]

    def _create_current_crop_json(self, crop_id, crop_data_json, plant_data_json):
        plant_id = crop_data_json['plant_id']
        name = plant_data_json['name']
        crop_name = crop_data_json['name']
        category = plant_data_json['category']
        plant_date = crop_data_json['plant_date']
        maturity_integer = plant_data_json['maturity_integer']
        info = {'crop_id': int(crop_id), 'plant_id': int(plant_id), 'crop_name': str(crop_name), 'name': str(name), 'category': str(category), 'plant_date': str(plant_date), 'maturity_integer': int(maturity_integer)}
        with open('ccrop.json', 'w') as json_file:
            json.dump(info, json_file)

    def delete_current_crop(self):
        if os.path.isfile('ccrop.json'):
            os.remove('ccrop.json')
            return jsonify({"message": 'Primary crop removed!'})
        else:
            return flask.abort(404, message='No crop currently set!')

    def get_current_crop(self):
        if os.path.isfile('ccrop.json'):
            with open('ccrop.json', 'r') as json_file:
                data = json.load(json_file)
                return data
        else:
            return jsonify({'crop_id': -1, 'plant_id': -1, 'crop_name': "not set", 'name': "not set", 'category': "not set", 'plant_date': "n/a", 'maturity_integer': -1})

    def create_current_crop(self, headers):
        if os.path.isfile('ccrop.json'):
            return jsonify({"message": 'A crop is currently set. Delete that one first.'})
        else:
            crop_id = headers['crop_id']
            crop_data_json = self._get_crop_data_json(crop_id)
            plant_id = str(crop_data_json['plant_id'])
            plant_data_json = self._get_plant_data_json(plant_id)
            self._create_current_crop_json(crop_id, crop_data_json, plant_data_json)
            return jsonify({"message": 'Crop successfully set!'})

