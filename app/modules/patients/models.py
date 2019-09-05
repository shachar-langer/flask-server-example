"""
Models for Patients
"""

from app.common import db
from app.common.models import User


class Patient(User):  # pylint: disable=too-few-public-methods
    """
    Model for patients
    """

    __tablename__ = "patient"
    social_worker_id = db.Column(db.Integer,
                                 db.ForeignKey('social_worker.user_id'))
