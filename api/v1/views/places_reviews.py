#!/usr/bin/python3
"""amenities api rest"""
from flask import Blueprint, jsonify, abort, request, make_response
from flask_cors import cross_origin

import models 
from api.v1.views import app_views 
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
@cross_origin()
def all_amenities():
    """retrieve all amenities"""
    all_list = []
    for city_all in storage.all(City).values():
        all_list.append(city_all.to_dict())
    return jsonify(all_list)


@app_views.route("/cities/<city_id>/places", methods=["GET"])
@cross_origin()
def city_by_id(city_id):
    """find by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
@cross_origin()
def place_by_id(place_id):
    """find by id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
@cross_origin()
def delete_place_id(place_id):
    """delete one place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
@cross_origin()
def create_place():
    """save one amenity"""
    try:
        json = request.get_json()
        name = json.get("name", None)
        if not name:
            return abort(400, "Missing name")
        new_place = Place()
        new_place.name = name
        new_place.save()
        return jsonify(new_place.to_dict()), 201
    except Exception as error:
        abort(400, "Not a JSON")


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
@cross_origin()
def update_reviews(place_id):
    """update one place"""
    place_obj = models.storage.get(Place, place_id)

    if not place_obj:
        return abort(404)

    try:
        json = request.get_json()
        name = json.get("name", None)
        if not name:
            return abort(400, "Missing name")
        ignore = ['id', 'created_at', 'updated_at']
        data = request.get_json()
        for key, value in data.items():
            if key not in ignore:
                setattr(place_obj, key, value)
        place_obj.save()
        return jsonify(place_obj.to_dict()), 201

    except Exception as error:
        abort(400, "Not a JSON")
