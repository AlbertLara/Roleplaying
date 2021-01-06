# api/home/views.py
from flask import render_template, abort
from flask_login import login_required
from ...models import *
from . import admin
from ... import db
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
    for game in games:
        print(game.players)
    template = render_template('admin/games.html',games=games, title='Partidas')
    return template


@admin.route('/sistemas')
@login_required
def sistemas():
    check_admin()
    systems = Sistema.query.all()
    for sistema in systems:
        print(sistema.games)
    template = render_template('admin/sistemas.html',sistemas=systems,title='Sistemas')
    return template