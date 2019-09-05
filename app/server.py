"""
RESTful server initialization
"""

from flask import Flask
from flask_restplus import Api
from app.common import db
from app.common import ma
from app.modules.socialWorkers.resources import api as social_workers_api
from app.modules.patients.resources import api as patients_api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///server_db.db'

api = Api(app)
api.add_namespace(social_workers_api)
api.add_namespace(patients_api)

if __name__ == '__main__':
    ma.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
