from .models import *
from .db import ma

class UserSchema(ma.Schema):
    class Meta:
        model = User
        sqla_session = db.session

class GameSchema(ma.Schema):
    class Meta:
        model = Games
        sqla_session = db.session