#!/usr/bin/python3
"""Flask app Module"""

import os
from models import storage
from flask_cors import CORS
from api.v1.views import app_views
from flask import Flask, jsonify, make_response

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def close(exception):
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app_host = os.getenv("HBNB_API_HOST", default="0.0.0.0")
    app_port = os.getenv("HBNB_API_PORT", default=5000)
    app.run(host=app_host, port=int(app_port), threaded=True)
