from flask_restx import Resource
from flask import request
from ..models import User
from ..schema import  UserSchema
from ..instance import api
from ..common.error_handling import ObjectNotFound,AppErrorBaseClass
users_schema = UserSchema(many=True)
user_schema = UserSchema()

ns = api.namespace('users',description='Get all Users')

@ns.route('')
class UserListResource(Resource):
    def post(self):
        pass

    def get(self):
        users = User.query.all()
        print(users)
        return user_schema.dump(users,many=True)


@ns.route('/<int:userId>')
class UserResource(Resource):
    def get(self,userId):
        user = User.query.filter_by(id=userId).first()
        if user is None:
            raise ObjectNotFound('El usuario no existe')
        return user_schema.dump(user)