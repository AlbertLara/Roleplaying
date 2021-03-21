from flask import jsonify, request, abort, session
from flask_login import current_user
import redis
from functools import wraps, update_wrapper
from flask_session import RedisSessionInterface
from itsdangerous import URLSafeTimedSerializer
from flask import current_app as app
import os

def admin_role_required(f):
    @wraps(f)
    def decorator(*args,**kwargs):
        if not current_user.is_admin:
            abort(400)
        return f(*args,**kwargs)
    return decorator


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'])
    except:
        return False
    return email

def decouple_user_sessions():
    conn = redis.from_url(os.getenv('SESSION_REDIS'))
    rs = RedisSessionInterface(conn, os.getenv('SECRET_KEY'))
    sessions = conn.keys(pattern='session:[a-zA-Z0-9]*')
    print(session)
    sessions = [sess.decode('utf8') for sess in sessions]
    sessions = [sess for sess in sessions if session.sid not in sess]
    data = {}
    for sess in sessions:
        values = conn.get(sess)
        user_session = rs.serializer.loads(values)

        userId = user_session.get('_user_id')
        username = user_session.get('username')
        email = user_session.get('email')
        active = user_session.get('active')

        data[userId] = {'username': username,
                        'email': email,
                        'active': active}
    session['users'] = data
    print(session['users'])