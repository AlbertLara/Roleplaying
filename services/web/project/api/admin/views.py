# api/home/views.py
from flask import render_template, abort
from flask_login import login_required, current_user
from ...models import *
from . import *
from .forms import *
from ... import db
from ...token import *

def check_admin():
    if not current_user.is_admin:
        abort(403)


@blueprint.route('/')
@login_required
@admin_role_required
def admin_dashboard():
    template = render_template(template_name_or_list='admin/main.html',
                               title='Admin',
                               permission='admin')
    return template

@blueprint.route('/Usuarios')
@login_required
@admin_role_required
def users():
    users = User.query.all()
    forms = []
    for user in users:
        user.default_active = f"{'checked' if user.active else ''}"
        user.default_admin = f"{'checked' if user.is_admin else ''}"
        user_form = UsersForm(obj=user)
        user_form.active.default = user.default_active
        user_form.is_admin.default = user.default_admin
        forms.append(user_form)
    print(forms)
    print(users)
    template = render_template('admin/users.html', forms=forms, title='Usuarios')
    return template