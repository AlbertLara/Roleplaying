import os
import redis
from distutils.util import strtobool

ENV = os.getenv('ENV')
PORT = os.getenv('PORT')
FLASK_ENV = os.getenv('FLASK_ENV')
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = bool(os.getenv('DEBUG'))
SQLALCHEMY_TRACK_MODIFICATIONS = bool(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS'))
SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')
JWT_BLACKLIST_TOKEN_CHECKS = os.getenv('JWT_BLACKLIST_TOKEN_CHECKS').split(" ")
DB_URL = os.getenv("DATABASE_URL")

SQLALCHEMY_DATABASE_URI =os.getenv('SQL_URL' DB_URL)

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True

MAIL_USERNAME = os.getenv('APP_MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('APP_MAIL_PASSWORD')

REDIS_URL = os.getenv('REDIS_URL')
QUEUES = ['default']

SESSION_TYPE = os.getenv('SESSION_TYPE')
SESSION_REDIS = redis.from_url(os.getenv('SESSION_REDIS'))
SESSION_PERMANENT = False
SESSION_PROTECTION = 'strong'