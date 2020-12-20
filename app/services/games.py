from app.models import *
import itertools
class GameService():
    ids = {0:'Three',1:'Two',2:'One'}
    titles = {0:'Esperando respuesta',
              1:'Partidas como jugador',
              2:'Partidas creadas'}
    def __init__(self):
        pass

    @classmethod
    def get_games_for_user(self,user_id):
        games = Games.query.\
            join(Members, Members.game_id==Games.id).\
            join(Groups, Groups.id==Members.group_id).\
            filter(Members.user_id==user_id).order_by(Games.update_date.desc()).with_entities(Games, Members, Groups).all()

        data = []
        for gamemember in games:
            game = gamemember[0]
            member = gamemember[1]
            group = gamemember[2]
            print(group.group_name)
            players = User.query.join(Members, Members.game_id==game.id).all()
            users = [user.username for user in players]
            print(users)
            obj = {'title':game.title,'rol':''}
