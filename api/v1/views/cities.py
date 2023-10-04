#!/usr/bin/python3
"""handles cities page for flask app"""

from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response


@app_views.route('states/<state_id>/cities', methods=['GET', 'POST'])
def city_linked_by_state(state_id=None):
    """processes request on cities linked to a state"""
    state = storage.get('State', state_id)

    if not state:
        abort(404, 'Not found')

    if request.method == 'GET':
        return make_response(jsonify([city.to_dict()
                                      for city in state.cities]))

    if request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')

        if 'name' not in request.json:
            abort(400, "Missing name")

        request_data = request.get_json()
        
        request_data['state_id'] = state_id
        new_city = City(**request_data)
        new_city.save()

        return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def city(city_id=None):
    """process request on a city object"""
    city = storage.get('City', city_id)

    if not city:
        abort(404, 'Not found')

    if request.method == 'GET':
        return make_response(jsonify(city.to_dict()))

    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")

        for key, value in request.json.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(city, key, value)

        city.save()

        return make_response(jsonify(city.to_dict()), 200)
