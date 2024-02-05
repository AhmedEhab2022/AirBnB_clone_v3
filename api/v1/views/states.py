#!/usr/bin/python3

"""
Module contain states blueprint
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    states_list = []
    for state in storage.all("State").values():
        states_list.append(state.to_dict())

    return jsonify(states_list)


@app_views.route(
        "/states/<string:state_id>",
        methods=["GET"],
        strict_slashes=False
    )
def get_state(state_id):
    """Retrieves a State object by id"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route(
        "/states/<string:state_id>",
        methods=["DELETE"],
        strict_slashes=False
    )
def delete_state(state_id):
    """Deletes a State object by id"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    state.delete()
    storage.save()

    return jsonify({})


@app_views.route(
        "/states/",
        methods=["POST"],
        strict_slashes=False
    )
def create_state():
    """Creates a State"""
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    new_state = State(**data)
    state.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route(
        "/states/<string:state_id>",
        methods=["PUT"],
        strict_slashes=False
    )
def update_state(state_id):
    """Updates a State by id"""
    state = storage.get("State". state_id)
    if state is None:
        abort(404)

    data = request.get_json()

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in data.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            setattr(state, key, value)

    state.save()
    return jsonify(state.to_dict())
