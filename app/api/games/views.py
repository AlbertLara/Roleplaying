from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from .forms import *
from . import games
from app import *
from app.models import *
from app.services.games import *
from datetime import datetime
def list_games_pending():
    pass

@games.route('/',methods=['GET','POST'])
@login_required
def user_games():
    GameService.get_games_for_user(current_user.id)

    games = Games.query.join(Members, Members.game_id==Games.id).filter(Members.user_id==current_user.id).all()
    form = NewGame()
    if form.validate_on_submit():
        return redirect(url_for('game.create'))
    return render_template('home/games.html', games=games,form=form, title="Games")



@games.route('/create', methods=['GET','POST'])
@login_required
#Crear una nueva partida
def create():
    form = CreateGameForm()
    sistemas = Sistema.query.filter_by(status='a').all()
    values = [row.get_list() for row in sistemas]
    form.Sistema.choices = values
    if form.validate_on_submit():
        game = Games(title=form.title.data,
                     game_key=form.key.data,
                     max_players=form.max_players.data,
                     master_Id=current_user.id,
                     Sistema=form.Sistema.data,
                     is_public=bool(form.is_public.data),
                     creation_date=datetime.now(),
                     update_date=datetime.now())
        db.session.add(game)
        db.session.commit()

        member = Members(game_id=game.id,
                         user_id=current_user.id,
                         approved=True)
        db.session.add(member)
        db.session.commit()

        return redirect(url_for('game.user_games'))
    return render_template('games/create_game.html',form=form,title='Partida')


@games.route('/join', methods=['GET','POST'])
@login_required
#Lista de partidas que el usuario no se ha unido
def new_games():
    games = []
    all_games = Games.query.all()
    form = ViewGamesForm()
    if form.validate_on_submit():
        sistema = form.sistema.data.id
        games = Games.query.filter(Games.Sistema == sistema).all()
    for game in all_games:
        is_member = Members.query.filter(Members.user_id==current_user.id, Members.game_id==game.id).count() == 1
        if not is_member:
            games.append(game)
    return render_template('home/view_games.html',games=games, form=form,title="Buscar Partida")



@games.route('/join/<string:key>',methods=['GET','POST'])
@login_required
def join(key):
    print(key)
    game_id = Games.query.filter_by(game_key=key).first().id
    member = Members(game_id=game_id,
                     user_id=current_user.id)
    db.session.add(member)
    db.session.commit()

    return redirect(url_for('game.new_games'))