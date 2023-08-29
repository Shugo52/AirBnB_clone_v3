#!/usr/bin/python3
"""handles places for Flask app"""

from models import storage
from models.city import City
from models.place import Place
from models.state import State
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def places_in_city(city_id=None):
    """processes places in a city"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        all_places = storage.all('Place')
        city_places = [obj.to_dict() for obj in all_places.values()
                       if obj.city_id == city_id]
        return make_response(jsonify(city_places))

    if request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')

        if 'user_id' not in request.json:
            abort(400, 'Missing user_id')

        if 'name' not in request.json:
            abort(400, 'Missing name')

        new_place = Place(**request.get_json())
        new_place.save()


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def place(place_id=None):
    """processes a place"""
    place = storage.get('Place', place_id)

    if not place:
        abort(404, 'Not found')

    if request.method == 'GET':
        return make_response(jsonify(place.to_dict()))

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        if not request.json:
            abort(400, 'Not a JSON')

        for key, value in request.json.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(place, key, value)

        place.save()

        return make_response(jsonify(place.to_dict()), 200)
