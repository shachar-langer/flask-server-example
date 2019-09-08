"""
RESTful API resources for Patients
"""

from flask_restplus import Resource, fields, abort, Namespace
from app.common import db
from app.modules.patients.models import Patient
from app.modules.patients.schemas import PatientSchema

api = Namespace('patients',
                description="Patients API")

# TODO - make this model strict. Don't allow additional attributes
patient_model = api.model('Patient', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    })


@api.route('')
class Patients(Resource):
    """
    REST API for patients
    """

    def get(self):  # pylint: disable=no-self-use
        """
        Get all patients
        """
        schema = PatientSchema()
        list_of_patients = Patient.query.all()
        return schema.dump(list_of_patients, many=True), 200

    @api.expect(patient_model, validate=True)
    def post(self):  # pylint: disable=no-self-use
        """
        Create a new patient
        """
        schema = PatientSchema()
        load_res = schema.load(api.payload)
        if load_res.errors:
            abort(400, ",".join(
                ["{} - {}".format(attr, err_msg)
                 for attr, err_msg in load_res.errors.items()]))
        new_patient = load_res.data
        db.session.add(new_patient)
        db.session.commit()
        return schema.dump(new_patient).data, 201


@api.route('/<int:patient_id>')
class PatientById(Resource):
    """
    REST API for specific patient
    """

    def getPatientObject(self, patient_id):
        patient = Patient.query.filter_by(
            user_id=patient_id).first()
        if patient is None:
            abort(404,
                  'Patient ID {} was not found'.format(patient_id))
        return patient

    def get(self, patient_id):
        """
        Get a patient
        """
        patient = self.getPatientObject(patient_id)
        schema = PatientSchema()
        return schema.dump(patient).data, 200

    def delete(self, patient_id):
        """
        Delete a patient
        """
        patient = self.getPatientObject(patient_id)
        db.session.delete(patient)
        db.session.commit()
        return '', 204
