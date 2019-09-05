"""
Schemas for SocialWorkers
"""

from app.common import ma
from app.modules.socialWorkers.models import SocialWorker


class SocialWorkerSchema(ma.ModelSchema):  # pylint: disable=too-few-public-methods
    """
    Schema for social workers
    """

    class Meta:
        model = SocialWorker
