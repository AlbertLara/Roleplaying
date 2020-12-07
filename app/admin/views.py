# app/home/views.py
from flask import render_template, redirect, render_template, abort, current_app, flash, url_for
from flask_login import login_required, current_user
from ..models import *
from . import admin
from .. import db
from .forms import *
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
    template = render_template('admin/users.html',users=users,title='Usuarios')
    return template

@admin.route('/partidas')
@login_required
def partidas():
    check_admin()
    games = Games.query.all()
    template = render_template('admin/partidas.html',data=games, title='Partidas')
    return template

@admin.route('/sistemas')
@login_required
def sistemas():
    check_admin()
    sistemas = Sistema.query.all()
    template = render_template('admin/sistemas.html',sistemas=sistemas, title='Sistemas')
    return template


@admin.route('/sistemas/partidas/<int:id>')
@login_required
def list_partidas(id):
    check_admin()
    games = Games.query.filter_by(Sistema = id).all()
    if len(games) == 0:
        games = []
    template = render_template('admin/sistemas/partidas.html',games=games,title='Partidas')
    return template