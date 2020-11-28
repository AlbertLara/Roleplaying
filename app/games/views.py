from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from .forms import CreateGameForm
from . import games
from .. import db
from ..models import Games, Sistema
import json

@games.route('/create', methods=['GET','POST'])
@login_required
def create():
    form = CreateGameForm()
    sistemas = Sistema.query.filter_by(status='a').all()
    values = [row.get_list() for row in sistemas]
    form.Sistema.choices = values
    if form.validate_on_submit():
        game = Games(title=form.title.data,
                     max_players=form.max_players.data,
                     players=0,
                     new_users=0,
                     MasterId=current_user.id,
                     masterName=current_user.username,
                     Sistema=form.Sistema.data)
        db.session.add(game)
        db.session.commit()
        flash('Partida creada')
        return redirect(url_for('home.games'))
    return render_template('games/create_game.html',form=form,title='Partida')