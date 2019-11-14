from flask import Flask, request
from flask_restplus import reqparse, abort, Api, Resource
from flask_cors import CORS
import os
from apiv1 import blueprint as apiv1
from apiv2 import blueprint as apiv2

"""

Service listens on port 5000 (Flask Default Port)

"""

app = Flask(__name__)
api = Api(app=app)
# Api v1 - current features
app.register_blueprint(apiv1, url_prefix='/api/v1')
# Api v2 - future features
app.register_blueprint(apiv2, url_prefix='/api/v2')
cors = CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == '__main__':
    # Look for environment variable APPENV
    current_environment = os.environ['APPENV']
    if current_environment == "DEV":
        app.run(host= '0.0.0.0', debug=True)    
    elif current_environment == "PROD":
        app.run(host= '0.0.0.0', debug=False)
    else:
        app.run(host= '0.0.0.0', debug=False)