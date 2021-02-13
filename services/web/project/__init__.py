from flask import Flask, render_template, Response, jsonify
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_mail import Mail
from dotenv import load_dotenv
from .db import login_manager, ma, db
import os
import logging
from .models import User
import libgravatar
app = Flask(__name__, template_folder='web/templates', static_folder='web/static')
mail = Mail()


def create_app(ENV):
    config_path = os.getenv("CONFIG_PATH")
    envfile = f"{config_path}/.env.{ENV}"

    load_dotenv(envfile)

    from .config import Configuration

    config = Configuration()
    obj = config.get_app_config()
    app.config.from_mapping(obj)

    ma.init_app(app)
    mail.init_app(app)
    bootstrap = Bootstrap()
    bootstrap.init_app(app)
    with app.app_context():
        db.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        user = User.query.get(int(user_id))
        user.online = True
        user.save_to_db()
        return user

    login_manager.init_app(app)
    login_manager.login_message = 'Debes iniciar sesión para acceder a esta página.'
    login_manager.login_view = "auth.login"
    logging.basicConfig(level=logging.INFO)
    register_blueprint(app)
    register_error_handlers(app)
    return app

def register_blueprint(app):
    from .api.admin import blueprint as admin_blueprint
    from .api.auth import blueprint as auth_blueprint
    from .api.home import blueprint as home_blueprint
    from .api.groups import blueprint as group_blueprint
    from .api.friends import blueprint as friend_blueprint

    app.register_blueprint(home_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(group_blueprint)
    app.register_blueprint(friend_blueprint)


def update_user():
    username = os.environ.get('USER_ID')
    user = User.query.filter_by(username=username).first()
    if user.password_hash == '':
        user.password = os.environ.get('USER_PWD')
        user.save_to_db()

def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception_error(e):
        return jsonify({'msg': 'Internal server error'}), 500
    @app.errorhandler(405)
    def handle_405_error(e):
        return jsonify({'msg': 'Method not allowed'}), 405
    @app.errorhandler(403)
    def handle_403_error(e):
        return jsonify({'msg': 'Forbidden error'}), 403
    @app.errorhandler(404)
    def handle_404_error(e):
        return jsonify({'msg': 'Not Found error'}), 404
    @app.errorhandler(400)
    def handle_app_base_error(e):
        return jsonify({'msg': str(e)}), 400