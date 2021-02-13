from flask import Blueprint

blueprint = Blueprint('friends', __name__, url_prefix='/friends')
from . import views