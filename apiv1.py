from flask import Blueprint
from flask_restplus import Api, Resource

from app_routes.namespace_academy import api as ns1
from app_routes.namespace_challenges import api as ns2
from app_routes.namespace_applications import api as ns3
from app_routes.namespace_helm import api as ns4
from app_routes.namespace_kubernetes import api as ns5

blueprint = Blueprint('apiv1', __name__)

api = Api(blueprint)
api.add_namespace(ns1)
api.add_namespace(ns2)
api.add_namespace(ns3)
api.add_namespace(ns4)
api.add_namespace(ns5)