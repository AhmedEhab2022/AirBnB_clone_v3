#!/usr/bin/python3

"""
Module contain places blueprint
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort
from models.place import Place


@app_views.route(
    "/cities/<string:city_id>/places", methods=["GET"], strict_slashes=False
)
def get_places(city_id):
    """Retrieves the list of all Place objects"""
    nocity = True
    for city in storage.all("City").values():
        if city.id == city_id:
            nocity = False
    if nocity:
        abort(404)
    places_list = []
    for place in storage.all("Place").values():
        if place.city_id == city_id:
            places_list.append(place.to_dict())
    if places_list is None:
        abort(404)
    return jsonify(places_list)


@app_views.route("/places/<string:place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object by id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<string:place_id>", methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object by id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    place.delete()
    storage.save()

    return jsonify({}, 200)


@app_views.route(
    "cities/<string:city_id>/places", methods=["POST"], strict_slashes=False
)
def create_place(city_id):
    """Creates a Place"""
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    nocity = True
    for city in storage.all("City").values():
        if city.id == city_id:
            nocity = False
    if nocity:
        abort(404)

    data["city_id"] = city_id
    new_place = Place(**data)
    new_place.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<string:place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Updates a Place by id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict())
