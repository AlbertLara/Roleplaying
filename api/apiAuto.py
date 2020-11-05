from flask import Blueprint
from flask_restx import Api
from .apis.models import api as game_api

blueprint = Blueprint('api',__name__,url_prefix='/')
api = Api(
    blueprint,
    title='Rest Api',
    version='0.1',
    description='Rest API Service for Role App'
)

api.add_namespace(game_api)
