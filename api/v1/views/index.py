#!/usr/bin/python3
"""index page for flask app"""

from flask import jsonify, request
from models import storage
from api.v1.views import app_views


@app_views.route('/status')
def getstatus():
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def getcount():
    if request.method == 'GET':
        response = {}
        models = {
            "Amenity": "amenities",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
        }
        for key, value in models.items():
            response[value] = storage.count(key)
        return jsonify(response)
