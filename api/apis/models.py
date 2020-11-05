from flask_restx import Namespace, Resource, fields
from datetime import datetime

api = Namespace('Games', description='Tickets scripts')

model_check_game = api.model('Game: Check Game',
                             {'gameId':fields.Integer(required=True,
                                                      description='Game Id to filter')})


@api.route('/')
class Games(Resource):
    def get(self):
        pass

@api.route('/<int:gameId>')
class GameResource(Resource):
    @api.expect(model_check_game)
    def get(self,gameId):
        print(gameId)