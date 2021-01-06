from flask_restx import Api
from flask import Blueprint


api_blueprint = Blueprint('api',__name__,url_prefix='/rest/api')
api = Api(version='1.0',title='My API',
          description='A simple demonstration', validate=True)


api.init_app(api_blueprint)