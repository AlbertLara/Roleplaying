from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from .services.services import *
from flask_mail import Mail
import os
ma = Marshmallow()
login_manager = LoginManager()
app = Flask(__name__,instance_relative_config=True, template_folder='web/templates', static_folder='web/static')
mail = Mail()
db = SQLAlchemy()



def create_app(ENV):
    print(os.getenv("CONFIG"))
    config_path = os.getenv("CONFIG_PATH")
    config_file = f"{config_path}/config_{ENV}.json"
    from .config import Configuration
    config = Configuration(config_file)
    obj = config.get_app_config()
    app.config.from_mapping(obj)
    ma.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = 'Debes iniciar sesión para acceder a esta página.'
    login_manager.login_view = "auth.login"
    m1 = Migrate()
    m1.init_app(app,db)
    Bootstrap(app)
    with app.app_context():
        db.init_app(app)
        db.create_all()
        db.session.commit()
        process_data = ProcessData(config_file)
        process_data.process_data()
    from .api.home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .api.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .api.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .api.games import games as game_blueprint
    app.register_blueprint(game_blueprint)



    @app.errorhandler(403)
    def unauthorized(e):
        return render_template('errors/403.html')

    return app