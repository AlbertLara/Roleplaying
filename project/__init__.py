from flask import Flask, render_template, make_response, jsonify, session, request, g
from .utils.db import *
from flask_login import user_logged_out, current_user
from redis import Redis
import rq
import os
import logging
from .utils.models import User
from datetime import timedelta
from .utils.token import decouple_user_sessions
from datetime import timedelta


def create_app():
    app = Flask(__name__, template_folder='web/templates', static_folder='web/static')
    app.config.from_pyfile("config/settings.py")
    socket.init_app(app)
    ma.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    sess.init_app(app)
    with app.app_context():
        db.init_app(app)
        db.create_all()

    @app.before_request
    def before_request():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=30)
        session.modified = True
        g.user = current_user

    @login_manager.user_loader
    def load_user(user_id):
        user = User.query.get(int(user_id))
        decouple_user_sessions()
        session['username'] = user.username
        session['email'] = user.email
        session['active'] = user.active
        user.online = True
        user.save_to_db()
        return user
    register_blueprint(app)

    login_manager.init_app(app)
    login_manager.login_message = 'Debes iniciar sesión para acceder a esta página.'
    login_manager.login_view = "auth.login"
    login_manager.session_protection = 'strong'
    logging.basicConfig(level=logging.INFO)
    register_error_handlers(app)
    app.shell_context_processor({'app': app, 'db': db})
    return app

def register_blueprint(app):
    from .api.admin import blueprint as admin_blueprint
    from .api.auth import blueprint as auth_blueprint
    from .api.friends import blueprint as friend_blueprint
    from .api.groups import blueprint as group_blueprint
    from .api.home import blueprint as home_blueprint

    app.register_blueprint(home_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(group_blueprint)
    app.register_blueprint(friend_blueprint)

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