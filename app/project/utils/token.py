from flask import jsonify, request, abort
from flask_login import current_user
from functools import wraps, update_wrapper
from itsdangerous import URLSafeTimedSerializer
from ..project import app

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
        email = serializer.loads(token,salt=app.config['SECURITY_PASSWORD_SALT'],max_age=expiration)
    except:
        return False
    return email

