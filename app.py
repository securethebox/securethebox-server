from flask import Flask, request
from flask_restplus import reqparse, abort, Api, Resource
from flask_cors import CORS
import os

"""

Service listens on port 5000 (Flask Default Port)

"""

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@api.route('/')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

if __name__ == '__main__':
    # Look for environment variable APPENV
    current_environment = os.environ['APPENV']
    if current_environment == "DEV":
        app.run(host= '0.0.0.0', debug=True)    
    elif current_environment == "PROD":
        app.run(host= '0.0.0.0', debug=False)
    else:
        app.run(host= '0.0.0.0', debug=False)