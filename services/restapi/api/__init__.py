from flask import Blueprint, Flask, jsonify
from flask_restx import Api
from .instance import api_blueprint
from .common.error_handling import ObjectNotFound, AppErrorBaseClass
import logging
from dotenv import load_dotenv
from .endpoints.user import UserListResource
from .db import db
import os
authorizations = {
    'Basic':{
        'type':'basic',
        'in':'header',
        'name':'Authorization'
    }
}





def create_app(ENV):
    app = Flask(__name__)
    config_path = os.getenv("CONFIG_PATH")
    envfile = f"{config_path}/.env.{ENV}"
    load_dotenv(envfile)
    from .config import Configuration
    config = Configuration()
    obj = config.get_app_config()
    app.config.from_mapping(obj)
    logging.basicConfig(level=logging.INFO)
    with app.app_context():
        db.init_app(app)
    logging.getLogger("Main").info(api_blueprint.name)
    app.register_blueprint(api_blueprint)
    register_error_handlers(app)
    return app

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