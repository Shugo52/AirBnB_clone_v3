#!/usr/bin/python3
"""index page for flask app"""

from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status')
def getstatus():
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def getcount():
    count_dict = {"amenities": 'Amenity',
                  "cities": 'City',
                  "places": 'Place',
                  "reviews": 'Review',
                  "states": 'State',
                  "users": 'User'}

    for k in count_dict.keys():
        count_dict[k] = storage.count(count_dict.get(k))
    return jsonify(count_dict)
