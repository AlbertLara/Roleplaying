import os
from distutils.util import strtobool

ENV = os.getenv('ENV')
PORT = os.getenv('PORT')
FLASK_ENV = os.getenv('FLASK_ENV')
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = bool(os.getenv('DEBUG'))
SQLALCHEMY_TRACK_MODIFICATIONS = bool(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS'))
SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')
JWT_BLACKLIST_TOKEN_CHECKS = os.getenv('JWT_BLACKLIST_TOKEN_CHECKS').split(" ")
SQLALCHEMY_DATABASE_URI =os.getenv('DATABASE_URL')

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True

MAIL_USERNAME = os.getenv('APP_MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('APP_MAIL_PASSWORD')

REDIS_URL = os.getenv('REDIS_URL')
QUEUES = ['default']
