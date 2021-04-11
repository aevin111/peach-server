import json
import os

from flask import jsonify


class APIStatusInternal:
    def get_status(self, supplied_password):
        if os.path.isfile('password.json'):
            with open('password.json', 'r') as json_data:
                data = json.load(json_data)
                password = data['password']
                if password == supplied_password:
                    return jsonify({'response': 200})
                else:
                    return jsonify({'response': 403})

