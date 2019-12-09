from flask_restplus import Namespace, Resource, fields, reqparse
from .initialize.academy import addCourse
from app_controllers.firestore.firestore_academy import FirestoreAcademy

api = Namespace('challenges', description='Challenge related operations')

apps_parser = reqparse.RequestParser()
apps_parser.add_argument('challenge', help='{error_msg}', type=dict, location='json')

step_overview_fields = api.model('Step', {
    'id': fields.String(required=True, description='Step identifier'),
    'title': fields.String(required=True, description='Step title'),
    'content': fields.String(required=True, description='Step content'),
})

resource_fields = api.model('Challenge', {
    'title': fields.String(required=True, description='Title of challenge'),
    'description': fields.String(required=True, description='Short description of challenge'),
    'category': fields.String(required=True, description='Category of challenge'),
    'length': fields.Integer(required=True, description='Time limit of challenge'),
    'steps': fields.List(fields.Nested(step_overview_fields)),
    'totalSteps': fields.Integer(required=True, description='Total steps for challenge'),
    'activeStep': fields.Integer(required=True, description='Starting step number'),
})

fa = FirestoreAcademy()

@api.route('')
class ChallengeCreate(Resource):
    @api.doc('create_challenge')
    @api.expect(resource_fields)
    def post(self):
        args = apps_parser.parse_args()
        print(args['challenge'])
        fa.addCourse(args['challenge'])
        # addCourse()
        try:
            return args['challenge'], 201 ,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "POST"} 
        except:
            return args, 404