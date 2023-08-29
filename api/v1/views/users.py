#!/usr/bin/python3
"""handles users for Flask app"""

from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response


@app_views.route('/users', methods=['GET', 'POST'])
def users():
    """processes all users"""
    if request.method == 'GET':
        return make_response(jsonify(user.to_dict() for user
                                     in storage.all('User').values()))

    if request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')

        if 'email' not in request.json:
            abort(400, "Missing email")

        if 'password' not in request.json:
            abort(400, 'Missing password')

        new_user = User(**request.get_json())
        new_user.save()

        return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def user(user_id=None):
    """processes user by id"""
    user = storage.get('User', user_id)

    if not user:
        abort(404, 'Not found')

    if request.method == 'GET':
        return make_response(jsonify(user.to_dict()))

    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}))

    if request.method == 'PUT':
        if not request.json:
            abort(400, 'Not a JSON')

        for key, value in request.json.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(user, key, value)

        user.save()

        return make_response(jsonify(user.to_dict()), 200)
