from flask_restplus import Namespace, Resource, fields, reqparse

from app_controllers.infrastructure.kubernetes import (
    kubernetesGetPodId
)
from app_controllers.infrastructure.docker import (
    dockerGetContainerId
)
from app_controllers.challenges.challenges import (
    challengesManageChallenge1
)

kubernetes_parser = reqparse.RequestParser()
kubernetes_parser.add_argument('action', choices=('apply','delete'), help='{error_msg}')
kubernetes_parser.add_argument('userName', help='{error_msg}')
kubernetes_parser.add_argument('clusterName', choices=('us-west1-a'), help='{error_msg}')
kubernetes_parser.add_argument('serviceName', help='{error_msg}')

api = Namespace('kubernetes', description='Academy related operations')

@api.route('/challenges/<string:challenge_id>')
class KubernetesDeploy(Resource):
    @api.doc('deploy_challenge')
    def post(self, challenge_id):
        args = kubernetes_parser.parse_args()
        try:
            challengesManageChallenge1(args['clusterName'],args['userName'],args['action'])
            return "success", 201 ,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "POST"} 
        except:
            return "error", 404
