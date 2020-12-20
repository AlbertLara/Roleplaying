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
        sKey = Sistema.query.filter_by(id=form.Sistema.data).first().sKey


        game = Games(title=form.title.data,
                     game_key=form.key.data,
                     max_players=form.max_players.data,
                     Sistema=form.Sistema.data,
                     is_public=bool(form.is_public.data),
                     creation_date=datetime.now(),
                     update_date=datetime.now())
        db.session.add(game)
        db.session.commit()

        roles = Roles.query.all()
        role_admin = Roles.query.filter(Roles.priority==2).first()
        game_id = game.id
        for role in roles:
            role_name = role.rol
            group_name = f"{sKey} - {form.key.data} - {role_name}"
            priority = role.priority
            max_users = role.max_users
            max_players = None
            if max_users == '1':
                max_players = int(max_users)
            elif max_users == 'max_players':
                max_players = game.max_players
            elif max_users == 'is_public':
                if not game.is_public:
                    max_players = 0

            group = Groups(game_id=game_id,
                           group_name=group_name,
                           priority=priority,
                           max_players=max_players)
            db.session.add(group)
            db.session.commit()
        admin = Groups.query.filter(Groups.game_id==game_id,Groups.priority==role_admin.priority).first()
        member = Members(user_id=current_user.id,
                         group_id=admin.id,
                         game_id=game_id)
        db.session.add(member)
        db.session.commit()
        flash('Partida creada')
        return redirect(url_for('game.user_games'))
    return render_template('games/create_game.html',form=form,title='Partida')


@games.route('/join', methods=['GET','POST'])
@login_required
#Lista de partidas que el usuario no se ha unido
def new_games():
    games = Games.query.all()
    all_games = []
    form = ViewGamesForm()
    if form.validate_on_submit():
        sistema = form.sistema.data.id
        games = Games.query.filter(Games.Sistema == sistema).all()
    for game in games:
        game.group = game.groups.get(0)
        members = Members.query.filter(Members.user_id==current_user.id,Members.game_id==game.id).count()
        if members == 0:
            all_games.append(game)
    return render_template('home/view_games.html',games=all_games, form=form,title="Buscar Partida")



@games.route('/join/<string:key>',methods=['GET','POST'])
@login_required
def join(key):
    print(key)
    group = Groups.query.filter(Groups.group_name.like(f"%{key}%")).order_by(Groups.priority.asc()).first()

    if not current_user.has_group(group.id):
        print("Add group")
        member = Members(group_id=group.id,
                         user_id=current_user.id)
        db.session.add(member)
        db.session.commit()
    return redirect(url_for('game.new_games'))