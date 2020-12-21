# app/home/views.py
from flask import render_template, abort
from flask_login import login_required, current_user
from app.models import *
from . import admin
from app import db
def check_admin():
    if not current_user.is_admin:
        abort(403)


@admin.route('/')
@login_required
def admin_dashboard():
    check_admin()
    template = render_template(template_name_or_list='admin/main.html',
                               title='Admin',
                               permission='admin')
    return template

@admin.route('/Usuarios')
@login_required
def users():
    check_admin()
    users = User.query.all()
    for user in users:
        user_id = user.id
        groups = db.session.query(Members).filter_by(user_id=user_id).all()
        print(groups)
    template = render_template('admin/users.html',users=users,title='Usuarios')
    return template

@admin.route('/partidas')
@login_required
def partidas():
    check_admin()
    games = Games.query.all()
    template = render_template('admin/games.html',games=games, title='Partidas')
    return template