from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_session import Session


login_manager = LoginManager()
db = SQLAlchemy()
ma = Marshmallow()
session = Session()