"""
RESTful API resources for SocialWorkers
"""

from flask_restplus import Resource, fields, abort, Namespace
from app.modules.socialWorkers.models import SocialWorker
from app.modules.patients.models import Patient
from app.modules.socialWorkers.schemas import SocialWorkerSchema
from app.modules.patients.schemas import PatientSchema
from app.common import db

api = Namespace('socialWorkers',
                description="Social Workers API")

# TODO - make this model strict. Don't allow additional attributes
social_worker_model = api.model('Social Worker', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    })


@api.route('')
class SocialWorkers(Resource):
    """
    REST API for social workers
    """

    def get(self):  # pylint: disable=no-self-use
        """
        Get all social workers
        """
        schema = SocialWorkerSchema()
        list_of_social_workers = SocialWorker.query.all()
        return schema.dump(list_of_social_workers, many=True), 200

    @api.expect(social_worker_model, validate=True)
    def post(self):  # pylint: disable=no-self-use
        """
        Create a new social worker
        """
        schema = SocialWorkerSchema()
        load_res = schema.load(api.payload)
        if load_res.errors:
            abort(400,
                  ",".join(["{} - {}".format(attr, err_msg)
                            for attr, err_msg in load_res.errors.items()]))
        new_social_worker = load_res.data
        db.session.add(new_social_worker)
        db.session.commit()
        return schema.dump(new_social_worker).data, 201


@api.route('/<int:social_worker_id>')
class SocialWorkerById(Resource):
    """
    REST API for specific social worker
    """

    def getSocialWorkerObject(self, social_worker_id):
        social_worker = SocialWorker.query.filter_by(
            user_id=social_worker_id).first()
        if social_worker is None:
            abort(404,
                  'Social Worker ID {} was not found'.format(social_worker_id))
        return social_worker

    def get(self, social_worker_id):
        """
        Get a social worker
        """
        social_worker = self.getSocialWorkerObject(social_worker_id)
        schema = SocialWorkerSchema()
        return schema.dump(social_worker).data, 200

    def delete(self, social_worker_id):
        """
        Delete a social worker
        """
        social_worker = self.getSocialWorkerObject(social_worker_id)
        db.session.delete(social_worker)
        db.session.commit()
        return '', 204


@api.route('/<int:social_worker_id>/patients')
class GetAllPatients(Resource):
    """
    REST API for patients of a spcific social worker
    """

    def get(self, social_worker_id):  # pylint: disable=no-self-use
        """
        Get all the patients of a social worker
        """
        # Checking if the social worker ID exists
        social_worker = SocialWorker.query.filter_by(
            user_id=social_worker_id).first()
        if social_worker is None:
            abort(404,
                  'Social Worker ID {} was not found'.format(social_worker_id))
        schema = PatientSchema()
        return schema.dump(social_worker.patients, many=True), 200


@api.route('/<int:social_worker_id>/patients/<int:patient_id>')
class PatientsOfSocialWorkers(Resource):
    """
    REST API for specific patient of a specific social worker
    """

    def getPatientObject(self, social_worker_id, patient_id):
        # Checking if the social worker ID exists
        social_worker = SocialWorker.query.filter_by(
            user_id=social_worker_id).first()
        if social_worker is None:
            abort(404,
                  'Social Worker ID {} was not found'.format(social_worker_id))

        patient = Patient.query.filter_by(
            user_id=patient_id).first()

        # Checking if the patient ID exists in general and if it's related
        # to the social worker ID
        if patient is None or patient.social_worker_id != social_worker_id:
            abort(404,
                  'Patient ID {} was not found for social worker ID {}'
                  .format(patient_id, social_worker_id))

        return patient

    def get(self, social_worker_id, patient_id):
        """
        Get a patient of a social workers
        """
        patient = self.getPatientObject(social_worker_id, patient_id)
        schema = PatientSchema()
        return schema.dump(patient).data, 200

    def put(self, social_worker_id, patient_id):  # pylint: disable=no-self-use
        """
        Add a patient to a social worker
        """
        patient = Patient.query.filter_by(
            user_id=patient_id).first()
        if patient is None:
            abort(404,
                  'Patient ID {} was not found'.format(patient_id))
        patient.social_worker_id = social_worker_id
        db.session.commit()
        return '', 204

    def delete(self, social_worker_id, patient_id):
        """
        Remove a patient from a social worker
        """
        patient = self.getPatientObject(social_worker_id, patient_id)
        db.session.delete(patient)
        db.session.commit()
        return '', 204
