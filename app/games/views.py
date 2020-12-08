from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from .forms import CreateGameForm
from . import games
from .. import db
from ..models import Games,Sistema,Groups, Members
import json

def create_groups(sKey, key):
    roles = ['User', 'Viewer']
    for role in roles:
        name = f"{sKey} - {key} - {role}"
        group_exist = Groups.query.filter_by(group_name=name).all()
        if len(group_exist) == 0:
            group = Groups(group_name=name)
            db.session.add(group)
            db.session.commit()

@games.route('/create', methods=['GET','POST'])
@login_required
def create():
    form = CreateGameForm()
    sistemas = Sistema.query.filter_by(status='Activo').all()
    values = [row.get_list() for row in sistemas]
    form.Sistema.choices = values
    if form.validate_on_submit():
        sKey = Sistema.query.filter_by(id=form.Sistema.data).first().sKey
        create_groups(sKey,form.key.data)
        game = Games(title=form.title.data,
                     key=form.key.data,
                     max_players=form.max_players.data,
                     players=0,
                     masterId=current_user.id,
                     Sistema=form.Sistema.data)
        db.session.add(game)
        db.session.commit()

        flash('Partida creada')
        return redirect(url_for('home.games'))
    return render_template('games/create_game.html',form=form,title='Partida')