from flask_restx import Resource
from flask import request
from ..models import Games
from ..schema import GameSchema
from ..instance import api
multischema = GameSchema(many=True)
singleschema = GameSchema()

ns = api.namespace('games',description='Get all Games')

@ns.route('')
class UserListResource(Resource):
    def post(self):
        pass

    def get(self):
        users = Games.query.all()
        print(users)
        return multischema.dump(users)




