from flask_restx import Api
from flask import Blueprint, request, jsonify
from .models import User
from functools import wraps
import jwt
import os
authorizations = {
    'Basic':{
        'type':'basic',
        'in':'header',
        'name':'Authorization'
    }
}

api_blueprint = Blueprint('api',__name__,url_prefix='/rest/api')
api = Api(version='1.0',title='Roleplaying API',
          description='A simple demonstration')

api.init_app(api_blueprint)

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, os.environ.get('SECRET_KEY'))
            print(data)
            current_user = User.query.filter_by(username=data['sub']).first()

            if not current_user.is_admin:
                return jsonify({'message':'Insufficient privileges'})

        except:
            return jsonify({'message': 'token is invalid'})
        return f(*args, **kwargs)
    return decorator