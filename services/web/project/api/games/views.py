from flask import redirect, url_for, abort, render_template
from flask_login import login_required, current_user
from .forms import *
from . import *
import re
from ...services.service import *
from ...token import *

@games.route('/',methods=['GET','POST'])
@login_required
def user_games():
    games = GameService().get_games_for_user()
    form = NewGame()
    if form.validate_on_submit():
        return redirect(url_for('game.create'))
    return render_template('games/index.html', games=games,form=form, title="Games")



@games.route('/create', methods=['GET','POST'])
@login_required
#Crear una nueva partida
def create():
    form = CreateGameForm()
    values = SistemaService().get_active()
    form.Sistema.choices = values
    if form.validate_on_submit():
        title = form.title.data.lower()
        regex = "([a-zA-Z0-9]*)"
        x = re.findall(regex,title)
        game_key = '-'.join(list(filter(lambda item:item,x)))
        params = {'title':form.title.data,
                  'game_key':game_key,
                  'description':form.description.data,
                  'max_players':form.max_players.data,
                  'masterid':current_user.id,
                  'sistema_id':form.Sistema.data,
                  'is_public':bool(form.is_public.data),
                  'creation_date':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                  'update_date':datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        game = Games(**params)
        game.save_to_db()
        member = Members(game_id=game.id,
                         user_id=current_user.id,
                         approved=True,
                         role='GM')
        member.save_to_db()
        return redirect(url_for('game.user_games'))
    return render_template('games/create_game.html',form=form,title='Games')


@games.route('/join', methods=['GET','POST'])
@login_required
def new_games():
    games = GameService().get_unjoined()
    for game in games:
        print(game['users'])
    return render_template('games/new.html',games=games,title="Buscar Partida")



@games.route('/join/<string:key>',methods=['GET','POST'])
@login_required
def join(key):
    game_id = Games.query.filter_by(game_key=key).first().id
    member = Members(game_id=game_id,
                     user_id=current_user.id,
                     role='viewer')
    member.save_to_db()
    return redirect(url_for('game.new_games'))


@games.route('/details/<string:game_key>', methods=['GET','POST'])
@login_required
def view_game(game_key):
    game = Games.find_game_by_key(game_key)
    return render_template('games/view.html',title='', game=game)