from flask_restx import Resource, fields, marshal, marshal_with, Model
from flask import request
from ..models import User, Members
from ..schema import *
from ..instance import api, token_required
from ..db import db
import base64
import json


model_user = api.model('user_post',{
    'email':fields.String(description='User email address', required=True),
    'username':fields.String(description='Username', required=True),
    'password':fields.String(description='User password', required=True),
    'is_admin':fields.Boolean(default=False,description='User is admin')
})
ns = api.namespace('users',description='Get all Users')

@ns.route('')
class UserListResource(Resource):
    @token_required
    def post(self):
        req = request.get_json()
        data = user_post_schema.loads(req)
        user = User.find_user(data.get('username'),data.get('email'))
        if user is not None:
            return "User already exists.", 404
        user = User(**data)
        user.save_to_db()
        userattributes = UserAtributes(userid=user.id,
                                       atribute_name='creation_date',
                                       atribute_value=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        userattributes.save_to_db()
        return "User successfully created.", 204

    @token_required
    def get(self):
        args = dict(request.args)
        print(args)
        schema_fields = user_schema.dump_fields
        if len(args.keys()) > 0:
            columns = [key for key, value in args.items() if key not in schema_fields.keys()]
            if len(columns) > 0:
                return "Bad Request.", 400
            data = user_schema.loads(json_data=json.dumps(args))

            users = User.query.filter_by(**data).all()
            print(users)
            if len(users) == 0:
                return "User not found", 400
            elif len(users) == 1:
                user = User.query.filter_by(**data).first()
                print(user_schema.dump(user))
                user_data = user_schema.dump(user)
                user_data = {key:value for key, value in user_data.items() if key != 'password_hash'}
                return user_data
        else:
            users = User.query.all()
        return user_schema.dump(users,many=True)

    @ns.response(204,'User updated successfully')
    @ns.response(400,'Bad Request.')
    @ns.param('userId',required=True)
    @token_required
    def put(self):
        args = request.args
        userId = args.get('userId')
        user = User.query.get(userId)
        if user is None:
            return "Bad Request.", 400
        try:
            data = api.payload
            user.update(data)
            return "User updated successfully", 204
        except:
            return "Bad Request", 400


@ns.route('/verifyUser')
class UserResource(Resource):
    @ns.response(200,'Correct password')
    @ns.response(400,'Incorrect password')
    @ns.param('credentials',required=True)
    @token_required
    def get(self):
        args = dict(request.args)
        creds = str(args.get('credentials'))
        credentials = base64.b64decode(creds).decode('utf8').split(':')
        username = credentials[0]
        password = credentials[1]
        user = User.query.filter_by(username=username).first()
        if user is not None and User.verify_hash(password,user.password_hash):
            print("Correct")
            return user_schema.dump(user)
        else:
            return "Incorrect password", 400


@ns.route('/<int:userId>/games')
class MemberResource(Resource):
    @token_required
    def get(self,userId):
        print(userId)
        members = Members.query.filter_by(user_id=userId).all()
        games = [member.game for member in members]
        return game_schema.dump(games,many=True)