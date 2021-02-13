from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature, BadData
from flask import jsonify, request, abort
from flask_login import current_user
from functools import wraps, update_wrapper
from . import app

def admin_role_required(f):
    @wraps(f)
    def decorator(*args,**kwargs):
        if not current_user.is_admin:
            abort(400)
        return f(*args,**kwargs)
    return decorator

def check_role(f):
    @wraps(f)
    def decorator(*args,**kwargs):

        if not current_user.is_authenticated:
            return jsonify({'message':'Unauthorized'}), 400
        print(request.url_rule)
        return f(*args, **kwargs)
    return decorator


