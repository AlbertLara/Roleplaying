from flask import Blueprint

blueprint = Blueprint('groups', __name__, url_prefix='/group')
from . import views