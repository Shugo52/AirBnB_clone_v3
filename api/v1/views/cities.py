#!/usr/bin/python3
"""handles cities page for flask app"""

from models import storage
from models.state import City
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response


@app_views.route('states/<state_id>/cities', methods=['GET', 'POST'])
def city_linked_by_state(state_id=None):
    """processes request on cities linked to a state"""
    state = storage.get('State', state_id)

    if not state:
        abort(404)

    if request.method == 'GET':
        return jsonify([city.to_dict() for city in state.cities])

    if request.method == 'POST':
        if request.json is None:
            abort(400, 'Not a JSON')
        if 'name' not in request.json:
            abort(400, "Missing name")
        new_city = City(**request.get_json())
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def city(city_id=None):
    """process request on a city object"""
    city = storage.get('City', city_id)

    if not city:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        for key, value in request.json.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
