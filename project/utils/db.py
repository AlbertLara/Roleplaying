from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO, emit, disconnect
from flask_marshmallow import Marshmallow
from flask_mail import Mail

login_manager = LoginManager()
db = SQLAlchemy()
ma = Marshmallow()
mail = Mail()
bootstrap = Bootstrap()
socket = SocketIO()