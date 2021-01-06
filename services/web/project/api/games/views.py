from flask import redirect, url_for, abort, render_template
from flask_login import login_required
from .forms import *
from . import games
import re
from ...services.service import *


def can_view(game_id):
    member = Members.query.filter_by(game_id=game_id,user_id=current_user.id, approved=True).count()
    if member == 0:
        abort(403)

def list_games_pending():
    pass

@games.route('/',methods=['GET','POST'])
@login_required
def user_games():
    games = GameService.get_games_for_user()
    form = NewGame()
    if form.validate_on_submit():
        return redirect(url_for('game.create'))

    return render_template('games/index.html', games=games,form=form, title="Games")



@games.route('/create', methods=['GET','POST'])
@login_required
#Crear una nueva partida
def create():
    form = CreateGameForm()
    sistemas = Sistema.query.filter_by(status='a').all()
    values = [row.get_list() for row in sistemas]
    form.Sistema.choices = values
    if form.validate_on_submit():
        title = form.title.data.lower()
        regex = "([a-zA-Z0-9]*)"
        x = re.findall(regex,title)
        game_key = '-'.join(list(filter(lambda item:item,x)))

        params = {'title':form.title.data,
                  'game_key':game_key,
                  'max_players':form.max_players.data,
                  'master_id':current_user.id,
                  'sistema_id':form.Sistema.data,
                  'is_public':bool(form.is_public.data),
                  'creation_date':datetime.now(),
                  'update_date':datetime.now()}
        GameService().create_game(params)

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
        games = Games.query.filter(Games.sistema_id == sistema).all()
    for game in all_games:
        if not game.is_player and game.is_public:
            games.append(game)
    return render_template('games/new.html',games=games, form=form,title="Buscar Partida")



@games.route('/join/<string:key>',methods=['GET','POST'])
@login_required
def join(key):
    game_id = Games.query.filter_by(game_key=key).first().id
    member = Members(game_id=game_id,
                     user_id=current_user.id)
    db.session.add(member)
    db.session.commit()
    return redirect(url_for('game.new_games'))


@games.route('/details/<int:id>', methods=['GET','POST'])
@login_required
def view_game(id):
    can_view(id)
    game = Games.query.filter_by(id=id).first()
    members = game.members
    requests = []
    for member in members:
        if member.approved == None:
            requests.append(member)
    game.requests = requests
    return render_template('games/view.html',title='', game=game)