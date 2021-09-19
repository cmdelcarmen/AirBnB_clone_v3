#!/usr/bin/python3
"""
    API for HBNB
"""
from os import getenv
from flask import Flask
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
        Closes current SQLAlchemy session.
    """
    storage.close()

if __name__ == '__main__':
    app.run(getenv('HBNB_API_HOST', '0.0.0.0'),
            int(getenv('HBNB_API_PORT', '5000')), threaded=True)
