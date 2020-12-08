from flask import Blueprint

games = Blueprint('game', __name__)

from . import views