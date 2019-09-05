"""
Schemas for Patients
"""

from app.common import ma
from .models import Patient


class PatientSchema(ma.ModelSchema):  # pylint: disable=too-few-public-methods
    """
    Schema for patients
    """

    class Meta:
        model = Patient
