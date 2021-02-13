from flask import redirect, url_for, abort, render_template
from flask_login import login_required, current_user
from .forms import *
from . import *
import re
from ...services.service import *
from ...token import *

@blueprint.route('/')
@login_required
def index():
    form = NewGroup()
    if form.validate_on_submit():
        pass
    return render_template('groups/index.html',title='Grupos', form=form)