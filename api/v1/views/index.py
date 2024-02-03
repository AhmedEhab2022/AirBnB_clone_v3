#!/usr/bin/python3

"""
Module contain index.py file
"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """Returns a JSON: "status": "OK" """
    return jsonify({"status": "OK"})
