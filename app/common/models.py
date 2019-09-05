"""
Common models
"""

from app.common import db


class User(db.Model):  # pylint: disable=too-few-public-methods
    """
    Abstract model for users
    """

    __abstract__ = True
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
