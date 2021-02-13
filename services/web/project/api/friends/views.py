from flask import redirect, url_for, abort, render_template
from flask_login import login_required, current_user
from .forms import *
from . import *
import re
from ...services.service import *
from ...token import *

@blueprint.route('/', methods=['GET','POST'])
@login_required
def index():
    users = User.query.filter(User.id != current_user.id).all()
    data = [(user.id, user.username) for user in users]
    """form = SendRequest()
    form.users.choices = data"""
    template = render_template('friends/index.html',title='Amigos')
    return template