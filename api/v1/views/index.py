#!/usr/bin/python3
"""index page for flask app"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def getstatus():
    return jsonify({"status": "OK"})
