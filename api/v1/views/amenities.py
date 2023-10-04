#!/usr/bin/python3
"""handles amenities for Flask app"""

from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response


@app_views.route('/amenities', methods=['GET', 'POST'])
def amenities():
    """processes all amenities"""
    if request.method == 'GET':
        return make_response(jsonify([amenity.to_dict() for amenity
                                      in storage.all('Amenity').values()]))

    if request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')

        if 'name' not in request.json:
            abort(400, "Missing name")

        new_amenity = Amenity(**request.get_json())
        new_amenity.save()

        return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def amenity(amenity_id=None):
    """processes amenities by id"""
    amenity = storage.get('Amenity', amenity_id)

    if not amenity:
        abort(404, 'Not found')

    if request.method == 'GET':
        return make_response(jsonify(amenity.to_dict()))

    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        if not request.json:
            abort(400, 'Not a JSON')

        for key, value in request.json.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(amenity, key, value)

        amenity.save()

        return make_response(jsonify(amenity.to_dict(), 200))
