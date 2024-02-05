#!/usr/bin/python3

"""
Module that contain the Main App
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teadown(exeption):
    """Call in this method storage.close() to remove db session"""
    storage.close()


@app.errorhandler(404)
def error404(e):
    """Return a JSON-formatted 404 status code response"""
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


if __name__ == "__main__":

    host = os.environ.get("HBNB_API_HOST")
    port = os.environ.get("HBNB_API_PORT")

    if host is None:
        host = "0.0.0.0"

    if port is None:
        port = 5000
    app.run(host=host, port=port, threaded=True)
