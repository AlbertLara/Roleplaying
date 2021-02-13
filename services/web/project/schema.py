from .models import *
from .db import ma
from marshmallow import Schema, fields
from datetime import datetime

class SistemaSchema(Schema):
    id = fields.Integer()
    nombre = fields.String()

class UserPostSchema(Schema):
    username = fields.String()
    email = fields.String()
    password_hash = fields.String()

class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    email = fields.String()
    is_admin = fields.Boolean()
    active = fields.Boolean()

class RoleSchema(Schema):
    username = fields.String()
    role = fields.String()
    approved = fields.Boolean()

class MemberSchema(Schema):
    user_id = fields.Integer()
    game_id = fields.Integer()

class GameMemberSchema(Schema):
    title = fields.String()
    game_key = fields.String()
    max_players = fields.Integer()
    master = fields.String()
    description = fields.String()
    sistema = fields.Nested(SistemaSchema)
    users = fields.List(fields.Nested(RoleSchema))


class GameSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    game_key = fields.String()
    max_players = fields.Integer()
    masterid = fields.Integer()
    sistema_id = fields.Integer()
    is_public = fields.Boolean()
    creation_date = fields.DateTime(default=datetime.now())
    update_date = fields.DateTime(default=datetime.now())

user_schema = UserSchema()
game_schema = GameSchema()
sistema_schema = SistemaSchema()
member_schema = MemberSchema()
role_schema = RoleSchema()
game_member_schema = GameMemberSchema()
user_post_schema = UserPostSchema()