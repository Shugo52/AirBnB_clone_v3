#!/usr/bin/python3
"""handles reviews for places for Flask app"""

from models import storage
from models.place import Place
from models.state import State
from models.review import Review
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response


@app_views.route('places/<place_id>/reviews', methods=['GET', 'POST'])
def reviewed_by_places(place_id=None):
    """processes reviews for places"""
    place = storage.get('Place', place_id)

    if not place_id:
        abort(404, 'Not found')

    if request.method == 'GET':
        places = storage.all('Place')
        reviews_place = [obj.to_dict() for obj in places.values()
                         if obj.reviews == reviews_place]
        return make_response(jsonify(reviews_place))

    if request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')

        if 'user_id' not in request.json:
            abort(400, 'Missing user_id')

        if 'user_id' not in request.json:
            abort(400, 'Missing user_id')

        if not storage.get('User', request.get_json()['user_id']):
            abort(404, 'Not found')

        if 'text' not in request.json:
            abort(400, 'Missing text')

        new_review = Review(**request.get_json())
        new_review.place_id = place_id
        new_review.save()

        return make_response(jsonify(new_review.to_dict()))


@app_views.route('reviews/<review_id>' methods=['GET', 'DELETE', 'PUT'])
def review(review_id=None):
    """processes a review"""
    review = storage.get('Review')

    if not review:
        abort(404, 'Not found')

    if request.method == 'GET':
        return make_response(jsonify(review.to_dict()))

    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}))

    if request.method == 'PUT':
        if not request.json:
            abort(400, 'Not a JSON')

        for key, value in request.json.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(review, key, value)

        review.save()

        return make_response(jsonify(review.to_dict()), 200)
