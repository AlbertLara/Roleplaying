from flask import Blueprint, Flask, jsonify, Response
from flask_restx import Api
from .instance import api_blueprint
from .common.error_handling import ObjectNotFound, AppErrorBaseClass
import logging
from dotenv import load_dotenv, dotenv_values
from .endpoints.user import UserListResource, User, UserAtributes
from .endpoints.game import GameListResourse
from .endpoints.sistema import SistemasList
from .db import db
import os
from datetime import datetime


def create_app(ENV):
    app = Flask(__name__)
    config_path = os.getenv("CONFIG_PATH")
    envfile = f"{config_path}/.env.{ENV}"

    load_dotenv(envfile)

    from .config import Configuration
    config = Configuration()
    obj = config.get_app_config()
    app.config.from_mapping(obj)
    resp = Response()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    logging.basicConfig(level=logging.INFO)
    with app.app_context():
        db.init_app(app)
        add_user(config_path)
    logging.getLogger("Main").info(api_blueprint.name)
    app.register_blueprint(api_blueprint)
    register_error_handlers(app)
    return app

def add_user(config_path):
    webrest = f"{config_path}/.env.web_rest"
    credentials = dotenv_values(webrest)
    data = {}
    for key, value in credentials.items():
        if value.upper() in ('TRUE','FALSE'):
            value = value.upper() == 'TRUE'
        if key == 'password':
            value = User.generate_hash(value)
            key = 'password_hash'
        data[key] = value
    username = os.environ.get('USER_ID')
    email = os.environ.get('USER_MAIL')
    password = os.environ.get('USER_PWD')
    user = User.find_user(username,email)
    if user.password_hash == '':
        user.password_hash = data['password_hash']
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
    @app.errorhandler(AppErrorBaseClass)
    def handle_app_base_error(e):
        return jsonify({'msg': str(e)}), 500
    @app.errorhandler(ObjectNotFound)
    def handle_object_not_found_error(e):
        return jsonify({'msg': str(e)}), 404