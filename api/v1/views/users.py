#!/usr/bin/python3

"""
Module contain user view
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    users_list = []
    for user in storage.all("User").values():
        users_list.append(user.to_dict())

    return jsonify(users_list)


@app_views.route(
        "/users/<string:user_id>",
        methods=["GET"],
        strict_slashes=False
    )
def get_user(user_id):
    """Retrieves a User object by id"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route(
        "/users/<string:user_id>",
        methods=["DELETE"],
        strict_slashes=False
    )
def delete_user(user_id):
    """Deletes a User object by id"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)

    user.delete()
    storage.save()

    return jsonify({})


@app_views.route(
        "/users/",
        methods=["POST"],
        strict_slashes=False
    )
def create_user():
    """Creates a User"""
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    if "email" not in data:
        return jsonify({"error": "Missing email"}), 400

    if "password" not in data:
        return jsonify({"error": "Missing password"}), 400

    new_user = User(**data)
    new_user.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route(
        "/users/<string:user_id>",
        methods=["PUT"],
        strict_slashes=False
    )
def update_user(user_id):
    """Updates a User by id"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, 'Not a JSON')

    for key, value in data.items():
        if key not in ["id", "email", "created_at", "ubdated_at"]:
            setattr(user, key, value)

    user.save()
    return jsonify(user.to_dict())
