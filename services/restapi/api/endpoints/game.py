from flask_restx import Resource, fields, marshal, reqparse
from flask import request, jsonify
from ..models import *
from ..schema import *
from ..instance import api, token_required
from datetime import datetime
import json

ns = api.namespace('games',description='Get all Games')

@ns.route('')
class GameListResourse(Resource):
    @ns.response(204,'Game successfully created.')
    @ns.response(400,'Bad Request.')
    @ns.response(404,'Game already exists.')
    @ns.doc(description='Create a new game')
    @token_required
    def post(self):
        req = request.json
        try:
            data = game_schema.dump(req)
            game = Games(**data)
            game.save_to_db()
            member = Members(game_id=game.id,
                             user_id=game.masterid,
                             approved=True)
            member.save_to_db()
        except:
            return "Bad Request", 400
        return "Game successfully created", 204

    @token_required
    def get(self):
        args = dict(request.args)
        schema_fields = game_schema.dump_fields
        if len(args.keys()) > 0:
            columns = [key for key, value in args.items() if key not in schema_fields.keys()]
            if len(columns) > 0:
                return "Bad Request.", 400
            data = game_schema.loads(json_data=json.dumps(args))
            games = Games.query.filter_by(**data).all()
            if len(games) == 0:
                return "Game not found", 400
        else:
            games = Games.query.all()
        return game_schema.dump(games,many=True)


@ns.route('/<gameId>/members')
class GamesMember(Resource):
    @token_required
    def get(self,gameId):
        try:
            game = Games.query.filter_by(id=gameId).first()
            role_members = game.users
            print(role_members)
            return role_schema.dump(role_members,many=True)
        except:
            return "Game not found"


@ns.route('/unJoined')
class GameNotJoined(Resource):
    @token_required
    @ns.param('userId')
    @ns.response(400,'Bad Request.')
    def get(self):
        games = []
        try:
            data = dict(request.args)
            userId = int(data['userId'])
            all_games = Games.query.filter_by(is_public=True).all()
            for game in all_games:
                members = [member.user_id for member in game.members]
                is_member = userId in members
                if not is_member:
                    games.append(game)
        except:
            return "Bad Request", 400
        return game_member_schema.dump(games,many=True)



