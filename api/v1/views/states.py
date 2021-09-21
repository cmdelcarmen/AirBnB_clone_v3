#!/usr/bin/python3
'''
View for state objects
'''

from models import storage
from models.state import State
from flask import jsonify, Flask, request, abort
import os
from api.v1.views import app_views


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def all_states():
    '''
    Retrieves the list of all State objects
    '''

    statesList = storage.all(State)
    states_dict = []
    for state in statesList:
        states_dict.append(statesList[state].to_dict())
    return jsonify(states_dict)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    '''
    Retrieve a State object
    '''

    stateObj = storage.get(State, state_id)
    if (stateObj):
        return (jsonify(stateObj.to_dict()))
    else:
        abort(404)


@app_views.route(
        '/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def del_state(state_id=None):
    '''
    Delete a state object
    '''

    stateObj = storage.get(State, state_id)
    if (stateObj):
        storage.delete(stateObj)
        storage.save()
        return (jsonify({}), 200)

    else:
        abort(404)


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def state_create():

        d = request.get_json()

        if isinstance(d, dict):
            pass
        else:
            return (jsonify({"error": "Not a JSON"}), 400)

        if 'name' not in d.keys():
            return jsonify({'error': 'Missing name'}), 400

        if 'id' in d.keys():
            d.pop("id")
        if 'created_at' in d.keys():
            d.pop("created_at")
        if 'updated_at' in d.keys():
            d.pop("updated_at")

        obj = State(**d)

        storage.new(obj)
        storage.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def state_update(state_id=None):

        state = storage.get(State, id)

        if state is None:
                return abort(404)

        d = request.get_json()
        if isinstance(d, dict):
            pass
        else:
            return (jsonify({"error": "Not a JSON"}), 400)

        if 'id' in d.keys():
            d.pop("id")
        if 'created_at' in d.keys():
            d.pop("created_at")
        if 'updated_at' in d.keys():
            d.pop("updated_at")

        for key, value in d.items():
            setattr(state, key, value)

        storage.save()
        return jsonify(state.to_dict())
