# app/home/views.py

from flask import render_template, redirect, render_template, url_for, abort
from flask_login import login_required, current_user
from ..models import Games, Players
from .forms import *
from . import home


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html',path='home', title="Welcome")


@home.route('/players')
@login_required
def players():
    """
    Render the dashboard template on the /dashboard route
    """
    print(current_user.is_admin)
    return render_template('home/players.html',path='home', title="Players")


@home.route('/games', methods=['GET','POST'])
@login_required
def games():
    """
    Render the dashboard template on the /dashboard route
    """
    games = Games.query.filter_by(MasterId=current_user.id).all()
    form = NewGame()
    if form.validate_on_submit():
        return redirect(url_for('game.create'))
    return render_template('home/games.html',form=form, title="Games")

@home.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)
    return render_template('home/admin_dashboard.html',title='Dashboard')
