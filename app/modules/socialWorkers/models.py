"""
Models for SocialWorkers
"""

from app.common import db
from app.common.models import User


class SocialWorker(User):  # pylint: disable=too-few-public-methods
    """
    Model for social workers
    """

    __tablename__ = "social_worker"
    patients = db.relationship('Patient', backref='social_worker')
