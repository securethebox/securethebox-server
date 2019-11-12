from flask_restplus import Namespace, Resource, fields, reqparse
import yaml

from app_controllers.creator.application import (
    Application,
    generateDeploymentYaml,
    generateIngressYaml,
    generateServiceYaml,
)
from app_controllers.applications.helm_chart import (
    HelmChart
)

api = Namespace('helm', description='Helm chart related operations')

helm_parser = reqparse.RequestParser()
helm_parser.add_argument('yamlData', help='{error_msg}')

@api.route('/query')
class HelmQuery(Resource):
    @api.doc('query_helm')
    def post(self):
        args = helm_parser.parse_args()
        yd = args['yamlData']
        yData = yaml.safe_load(yd)
        hc = HelmChart()
        hc.setName(yData['name'])
        hc.setType("git")
        hc.setHost("localhost")
        # Ideally each user should have their own namespace
        hc.setNamespace("default")
        hc.setLocation(yData['url'])
        hc.loadChart()
        responsedata = hc.getChartValuesYaml()
        try:
            return responsedata, 201,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "POST"}
        except:
            return args, 404

@api.route('/save')
class HelmSave(Resource):
    @api.doc('save_helm')
    def post(self):
        args = apps_parser.parse_args()
        yd = args['yamlData']
        yData = yaml.safe_load(yd)
        hc = HelmChart()
        hc.setName(yData['name'])
        hc.setType("git")
        hc.setHost("localhost")
        # Ideally each user should have their own namespace
        hc.setNamespace("default")
        hc.setLocation(yData['url'])
        hc.loadChart()
        hc.setChartValuesYaml("  raw: \""+yData['chart']+"\"")

        app.addApplication(
            {
                'name': yData['name'],
                'label': yData['name'].capitalize(),
                'category': 'infrastructure',
                'category_label': 'Infrastructure'
            }
        )
        try:
            return "chart was added", 201,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "POST"}
        except:
            return args, 404