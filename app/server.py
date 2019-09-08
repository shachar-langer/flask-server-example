"""
RESTful server initialization
"""

import logging
from flask import Flask
from flask_restplus import Api
from app.common.logs import init_log
from app.common import db, ma
from app.modules.socialWorkers.resources import api as social_workers_api
from app.modules.patients.resources import api as patients_api

APP_DEBUG_MODE = False

init_log()
logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

app = Flask(__name__)  # pylint: disable=invalid-name
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///server_db.db'
app.config['SQLALCHEMY_ECHO'] = APP_DEBUG_MODE

api = Api(app,  # pylint: disable=invalid-name
          version='1.0',
          title='Flask Server Example API',
          description='RESTful API for Flask Server Example')
api.add_namespace(social_workers_api)
api.add_namespace(patients_api)

if __name__ == '__main__':
    logger.info("Initializing Flask server example")
    ma.init_app(app)
    db.init_app(app)
    logger.info("Creating database")
    with app.app_context():
        db.create_all()
    logger.info("Running Flask server example")
    app.run(debug=APP_DEBUG_MODE)
