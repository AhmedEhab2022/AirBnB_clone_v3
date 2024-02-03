#!/usr/bin/python3

"""
Module contain index.py file
"""

from api.v1.views import app_views
import json


@app_views.route('/status')
def status():
    """Returns a JSON: "status": "OK" """
    return json.dumps({"status": "OK"})
