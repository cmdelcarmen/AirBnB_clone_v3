#!/usr/bin/python3

import json
from werkzeug.exceptions import NotFound
from flask import request, jsonify, make_response
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states/', methods=['GET'])
def state_all():
    all_states = storage.all(State)
    states = []

    for key, value in all_states.items():
        states.append(value.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'])
def state_retrieve(state_id):
    state = storage.get(State, state_id)

    if state is None:
        raise NotFound
    return (jsonify(state.to_dict()))


@app_views.route('/states/<state_id>', methods=['DELETE'])
def state_delete(state_id):
    state = storage.get(State, state_id)

    if state is None:
        raise NotFound

    state.delete()
    storage.save()

    return ({}, 200)

@app_views.route('/states/', methods=['POST'])
def state_create():
    if not request.json:
        return make_response('Not a JSON', 400)

    if 'name' not in request.get_json().keys():
        return make_response('Missing name', 400)

    state = State(**request.get_json())
    state.save()
    return (jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def state_update(state_id=None):
    state = storage.get(State, state_id)

    if state is None:
        raise NotFound

    if not request.json:
        return make_response('Not a JSON', 400)

    for key, value in request.get_json().items():
        setattr(state, key, value)

    state.save()
    return (jsonify(state.to_dict()), 200)
