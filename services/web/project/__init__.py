from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from .services.services import ProcessData
from flask_mail import Mail
from dotenv import load_dotenv
from .rest_db import db, login_manager, ma
import os
import logging
from .models import User


app = Flask(__name__,instance_relative_config=True, template_folder='web/templates', static_folder='web/static')
mail = Mail()


def create_app(ENV):
    config_path = os.getenv("CONFIG_PATH")
    envfile = f"{config_path}/.env.{ENV}"
    load_dotenv(envfile)
    logging.basicConfig(level=logging.INFO)
    from .config import Configuration
    config = Configuration()
    obj = config.get_app_config()
    app.config.from_mapping(obj)
    ma.init_app(app)
    mail.init_app(app)
    m1 = Migrate()
    bootstrap = Bootstrap()

    with app.app_context():
        db.init_app(app)
        db.create_all()
        db.session.commit()
        bootstrap.init_app(app)
        proces = ProcessData()
        proces.process_data()
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    login_manager.init_app(app)
    login_manager.login_message = 'Debes iniciar sesión para acceder a esta página.'
    login_manager.login_view = "auth.login"

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