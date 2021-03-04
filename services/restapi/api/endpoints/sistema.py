from flask_restx import Resource, fields, marshal, reqparse
from flask import request, jsonify
from ..models import Sistema, Games
from ..schema import *
from ..instance import api, token_required
ns = api.namespace('sistemas',description='Sistemas de partidas de rol')

@ns.route('')
class SistemasList(Resource):
    @ns.param('status', type=str,required=False)
    @token_required
    def get(self):
        args = dict(request.args)
        print(args)
        if args == {}:
            sistemas = Sistema.query.all()
            return sistema_schema.dump(sistemas,many=True)
        else:
            status = args.get('status')
            sistemas = Sistema.get_by_status(status)
            return sistema_schema.dump(sistemas,many=True)



@ns.route('/<int:id>/Games')
class GamesSistemaResource(Resource):
    @token_required
    def get(self,id):
        games = Games.query.filter_by(sistema_id=id).all()
        return game_schema.dump(games,many=True)