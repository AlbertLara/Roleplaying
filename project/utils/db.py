from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from datetime import timedelta

login_manager = LoginManager()
db = SQLAlchemy()
ma = Marshmallow()

def get_delta(REMEMBER_COOKIE_DURATION:str):
    args = REMEMBER_COOKIE_DURATION.split(',')
    args = [arg.strip() for arg in args]
    kwargs = {}
    for arg in args:
        params = arg.split('=')
        kwargs[params[0]] = int(params[1])
    delta = timedelta(**kwargs)
    return delta