#!/usr/bin/python3
"""users api rest"""
from flask import jsonify, abort, request, make_response

import models
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def all_users():
    """retrieve all users"""
    all_list = []
    for user in storage.all(User).values():
        all_list.append(user.to_dict())
    return jsonify(all_list), 200


@app_views.route("/users/<string:user_id>", methods=["GET"],
                 strict_slashes=False)
def user_by_id(user_id):
    """find by id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict()), 200


@app_views.route("/users/<string:user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user_by_id(user_id):
    """delete one user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users/", methods=["POST"], strict_slashes=False)
def create_user():
    """save one user"""
    json = request.get_json()
    if not json:
        abort(400, "Not a JSON")
    email = json.get("email", None)
    if not email:
        abort(400, "Missing email")
    password = json.get("password", None)
    if not password:
        abort(400, "Missing password")

    new_user = User()
    new_user.email = email
    new_user.password = password
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<string:user_id>", methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    """update one user"""

    user_obj = models.storage.get(User, user_id)
    if not user_obj:
        return abort(404)
    json = request.get_json()
    if not json:
        abort(400, "Not a JSON")
    ignore = ['id', 'email', 'created_at', 'updated_at']
    for key, value in json.items():
        if key not in ignore:
            setattr(user_obj, key, value)
    models.storage.save()
    return jsonify(user_obj.to_dict())
