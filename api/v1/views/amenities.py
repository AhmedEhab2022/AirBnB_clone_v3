#!/usr/bin/python3

"""
Module contain amenities view
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities_list = []
    for amenity in storage.all("Amenity").values():
        amenities_list.append(amenity.to_dict())

    return jsonify(amenities_list)


@app_views.route(
    "/amenities/<string:amenity_id>", methods=["GET"], strict_slashes=False
)
def get_amenity(amenity_id):
    """Retrieves a Amenity object by id"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route(
    "/amenities/<string:amenity_id>", methods=["DELETE"], strict_slashes=False
)
def delete_amenity(amenity_id):
    """Deletes a Amenity object by id"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    amenity.delete()
    storage.save()

    return jsonify({})


@app_views.route("/amenities/", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Creates a Amenity"""
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    new_amenity = Amenity(**data)
    new_amenity.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route(
    "/amenities/<string:amenity_id>", methods=["PUT"], strict_slashes=False
)
def update_amenity(amenity_id):
    """Updates a Amenity by id"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            setattr(amenity, key, value)

    amenity.save()
    return jsonify(amenity.to_dict())
