#!/usr/bin/python3

import os
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exception):
    storage.close


if __name__ == "__main__":
    app_host = os.getenv("HBNB_API_HOST", default="0.0.0.0")
    app_port = os.getenv("HBNB_API_PORT", default=5000)
    app.run(host=app_host, port=int(app_port), threaded=True)
