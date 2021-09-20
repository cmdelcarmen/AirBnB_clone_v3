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


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
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
    if not request.json:
        return make_response('Not a JSON', 400)

    if 'name' not in request.get_json().keys():
        return make_response('Missing name', 400)

    state = State(**request.get_json())
    state.save()
    return (jsonify(state.to_dict()), 201)
