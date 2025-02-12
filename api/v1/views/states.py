#!/usr/bin/python3
"""handles states page for flask app"""

from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response


@app_views.route('/states', methods=['GET', 'POST'])
def getstates():
    """route to handle http method for requested states"""
    if request.method == 'GET':
        return make_response(jsonify([state.to_dict()for state
                                      in storage.all('State').values()]))

    if request.method == 'POST':
        if request.json is None:
            abort(400, 'Not a JSON')

        if "name" not in request.json:
            abort(400, 'Missing name')

        new_object = State(**request.get_json())
        new_object.save()

        return make_response(jsonify(new_object.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def state(state_id=None):
    """route to handle http method for requested state by id"""
    state = storage.get('State', state_id)

    if state is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return make_response(jsonify(state.to_dict()))

    if request.method == 'DELETE':
        storage.delete(state)
        storage.save()

        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")

        for key, value in request.json.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(state, key, value)

        state.save()

        return make_response(jsonify(state.to_dict()), 200)
