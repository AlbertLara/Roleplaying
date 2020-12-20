from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from app.services.services import *

ma = Marshmallow()
login_manager = LoginManager()
app = Flask(__name__,instance_relative_config=True)
db = SQLAlchemy()
def create_app(ENV):

    json_file = f"../../configuration/settings_{ENV}.json"
    config_file = f"../configuration/config_{ENV}.json"
    from app.config import Configuration
    config = Configuration(config_file)
    obj = config.get_app_config()

    app.config.from_mapping(obj)
    ma.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = 'Debes iniciar sesión para acceder a esta página.'
    login_manager.login_view = "auth.login"
    m1 = Migrate()
    m1.init_app(app,db)
    Bootstrap(app)
    from app import models
    with app.app_context():
        db.init_app(app)
        db.create_all()
        db.session.commit()
        process_data = ProcessData(config_file)
        process_data.process_data()



    from app.api.home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from app.api.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.api.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from app.api.games import games as game_blueprint
    app.register_blueprint(game_blueprint)

    return app