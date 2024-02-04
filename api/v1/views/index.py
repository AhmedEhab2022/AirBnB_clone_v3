#!/usr/bin/python3

"""
Module contain index.py file
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """Returns a JSON: "status": "OK" """
    return jsonify({"status": "OK"})


@app_views.route('/api/v1/stats', methods=['GET'])
def stats():
    """Return a JSON with the number of each class"""
    amenities = storage.count("Amenity")
    cities = storage.count("City")
    places = storage.count("Place")
    reviews = storage.count("Review")
    states = storage.count("State")
    users = storage.count("User")

    return jsonify({
        "amenities": amenities,
        "cities": cities,
        "places": places,
        "reviews": reviews,
        "states": states,
        "users": users
    })
