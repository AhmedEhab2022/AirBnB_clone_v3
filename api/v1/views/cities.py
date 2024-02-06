#!/usr/bin/python3

"""
Module contain cities blueprint
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort
from models.city import City


@app_views.route(
        "/states/<string:state_id>/cities",
        methods=["GET"],
        strict_slashes=False
    )
def get_cities(state_id):
    """Retrieves the list of all City objects"""
    nostate = True
    for state in storage.all("State").values():
        if state.id == state_id:
            nostate = False
    if nostate:
        abort(404)
    cities_list = []
    for city in storage.all("City").values():
        if city.state_id == state_id:
            cities_list.append(city.to_dict())
    if cities_list is None:
        abort(404)
    return jsonify(cities_list)


@app_views.route(
        "/cities/<string:city_id>",
        methods=["GET"],
        strict_slashes=False
    )
def get_city(city_id):
    """Retrieves a City object by id"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route(
        "/cities/<string:city_id>",
        methods=["DELETE"],
        strict_slashes=False
    )
def delete_city(city_id):
    """Deletes a City object by id"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    city.delete()
    storage.save()

    return jsonify({}, 200)


@app_views.route(
        "states/<string:state_id>/cities",
        methods=["POST"],
        strict_slashes=False
    )
def create_city(state_id):
    """Creates a City"""
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    nostate = True
    for state in storage.all("State").values():
        if state.id == state_id:
            nostate = False
    if nostate:
        abort(404)

    data["state_id"] = state_id
    new_city = City(**data)
    new_city.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route(
        "/cities/<string:city_id>",
        methods=["PUT"],
        strict_slashes=False
    )
def update_city(city_id):
    """Updates a City by id"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, 'Not a JSON')

    for key, value in data.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            setattr(city, key, value)

    city.save()
    return jsonify(city.to_dict())
