from flask import Blueprint
from flask_login import current_user


games = Blueprint('game', __name__, url_prefix='/game')

from . import views