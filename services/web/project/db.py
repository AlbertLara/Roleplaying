from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask_marshmallow import Marshmallow
from requests import Session
import requests
import jwt
import os

login_manager = LoginManager()
db = SQLAlchemy()
ma = Marshmallow()