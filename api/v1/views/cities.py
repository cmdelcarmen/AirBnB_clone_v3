#!/usr/bin/python3
'''
View for state objects
'''

from models import storage
from models.state import State
from models.city import City
from flask import jsonify, make_response, abort, request
from api.v1.views import app_views

@app_views.route('/cities/<id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def view_city_id(id):
    city = storage.get(City, id)

    if city is None:
        return abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        d = request.get_json()
        if isinstance(d, dict):
            pass
        else:
            return jsonify({"error": "Not a JSON"}), 400

        if 'id' in d.keys():
            d.pop("id")
        if 'created_at' in d.keys():
            d.pop("created_at")
        if 'updated_at' in d.keys():
            d.pop("updated_at")

        for key, value in d.items():
            setattr(city, key, value)

        storage.save()
        return jsonify(city.to_dict())


@app_views.route('/states/<id>/cities',
            methods=['GET', 'POST'], strict_slashes=False)
def cities_all_state(id):
    state = storage.get(State, id)

    if state is None:
        return abort(404)

    if request.method == 'GET':
        all_cities = []
        for city in state.cities:
            all_cities.append(city.to_dict())
        return jsonify(all_cities)

    if request.method == 'POST':
        d = request.get_json()

        if isinstance(d, dict):
            pass
        else:
            return jsonify({"error": "Not a JSON"}), 400

        if 'name' not in d.keys():
            return jsonify({'error': 'Missing name'}), 400

        if 'id' in d.keys():
            d.pop("id")
        if 'created_at' in d.keys():
            d.pop("created_at")
        if 'updated_at' in d.keys():
            d.pop("updated_at")

        d.update({"state_id": id})
        obj = City(**d)
        storage.new(obj)
        storage.save()
        return jsonify(obj.to_dict()), 201
