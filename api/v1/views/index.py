#!/usr/bin/python3
"""
    Returns the status of the api.
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def index():
    """
        Returns JSON:"status": "OK"
    """
    return jsonify({'status': 'OK'})
