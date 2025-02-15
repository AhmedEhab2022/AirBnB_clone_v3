#!/usr/bin/python3

"""
Module contain reviews blueprint
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort
from models.review import Review


@app_views.route(
    "/places/<string:place_id>/reviews", methods=["GET"], strict_slashes=False
)
def get_reviews(place_id):
    """Retrieves the list of all Review objects"""
    noplace = True
    for place in storage.all("Place").values():
        if place.id == place_id:
            noplace = False
    if noplace:
        abort(404)
    reviews_list = []
    for review in storage.all("Review").values():
        if review.place_id == place_id:
            reviews_list.append(review.to_dict())
    if reviews_list is None:
        abort(404)
    return jsonify(reviews_list)


@app_views.route("/reviews/<string:review_id>", methods=["GET"],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object by id"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
    "/reviews/<string:review_id>", methods=["DELETE"],
    strict_slashes=False
)
def delete_review(review_id):
    """Deletes a Review object by id"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)

    review.delete()
    storage.save()

    return jsonify({}, 200)


@app_views.route(
    "places/<string:place_id>/reviews", methods=["POST"],
    strict_slashes=False
)
def create_review(place_id):
    """Creates a Review"""
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    if "text" not in data:
        return jsonify({"error": "Missing text"}), 400
    if "user_id" not in data:
        abort(400, "Missing user_id")

    noplace = True
    for place in storage.all("Place").values():
        if place.id == place_id:
            noplace = False
    if noplace:
        abort(404)

    user_id = data["user_id"]
    nouser = True
    for user in storage.all("User").values():
        if user.id == user_id:
            nouser = False
    if nouser:
        abort(404, "useeeeeeeeeeeeeeee")

    data["place_id"] = place_id
    new_review = Review(**data)
    new_review.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<string:review_id>", methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a Review by id"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict())
