# app/home/views.py

from flask import render_template, redirect, render_template, url_for, abort
from flask_login import login_required, current_user
from ..models import Games
from .forms import *
from . import home
from .. import db

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
    games = db.session.query(Games).filter(Games.masterId != current_user.id).all()
    print(games)
    return render_template('home/players.html', games=games,path='home', title="Players")


@home.route('/games', methods=['GET','POST'])
@login_required
def games():
    """
    Render the dashboard template on the /dashboard route
    """
    games = Games.query.filter_by(masterId=current_user.id).all()
    form = NewGame()
    if form.validate_on_submit():
        return redirect(url_for('game.create'))
    return render_template('home/games.html', games=games,form=form, title="Games")