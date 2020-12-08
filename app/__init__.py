from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate, init, upgrade, migrate

from config import app_config

db = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = 'Debes iniciar sesión para acceder a esta página.'
    login_manager.login_view = "auth.login"
    m1 = Migrate()
    m1.init_app(app,db)

    Bootstrap(app)
    from app import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .games import games as game_blueprint
    app.register_blueprint(game_blueprint,url_prefix='/game')

    return app