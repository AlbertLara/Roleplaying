from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_socketio import SocketIO

socketio = SocketIO()
login_manager = LoginManager()
db = SQLAlchemy()
ma = Marshmallow()