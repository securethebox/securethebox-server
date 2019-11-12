from flask_restplus import Namespace, Resource, fields, reqparse
from app_controllers.creator.application import (
    Application,
    generateDeploymentYaml,
    generateIngressYaml,
    generateServiceYaml,
)

app = Application()
app.loadApplications(
    [
        {'name': 'kubernetes', 'label': 'Kubernetes', 'category': 'infrastructure','category_label': 'Infrastructure'},
        {'name': 'virtual_machine', 'label': 'Virtual Machine', 'category': 'infrastructure','category_label': 'Infrastructure'},
        {'name': 'nginx', 'label': 'Nginx', 'category': 'load_balancer','category_label': 'Load Balancer'},
        {'name': 'haproxy', 'label': 'HAProxy', 'category': 'load_balancer','category_label': 'Load Balancer'},
        {'name': 'juice-shop', 'label': 'Juice Shop', 'category': 'application','category_label': 'Applications'},
        {'name': 'suricata', 'label': 'Suricata', 'category': 'ids','category_label': 'IDS'},
        {'name': 'wazuh', 'label': 'Wazuh', 'category': 'endpoint_security','category_label': 'Endpoint Security'},
        {'name': 'elk', 'label': 'ELK', 'category': 'siem','category_label': 'SIEM'},
        {'name': 'splunk', 'label': 'Splunk', 'category': 'siem','category_label': 'SIEM'}, 
    ])

apps_parser = reqparse.RequestParser()
apps_parser.add_argument('yamlData', help='{error_msg}')

api = Namespace('applications', description='Applications related operations')

@api.route('/')
class ApplicationsList(Resource):
    @api.doc('get_applications_list')
    def get(self):
        try:
            return app.getApplicationList(), 201,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "GET"}
        except:
            return "error", 404

@api.route('/categories')
class ApplicationsCategories(Resource):
    @api.doc('get_applications_categories')
    def get(self):
        try:
            return app.getCategories(), 201,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "GET"}
        except:
            return "error", 404