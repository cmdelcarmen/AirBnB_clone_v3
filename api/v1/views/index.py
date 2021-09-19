#!/usr/bin/python3
"""
    Returns the status of the api.
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def index():
    """
        Returns JSON:"status": "OK"
    """
    return jsonify({'status': 'OK'})

@app_views.route('/stats', strict_slashes=False)
def number_of_bytes():
    """retrieves the number of each objects by type"""
    return jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    })
