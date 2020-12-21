from app.models import *
import itertools
class GameService():
    def __init__(self):
        pass

    @classmethod
    def get_games_for_user(self,user_id):
        games = Games.query.\
            join(Members, Members.game_id==Games.id).\
            filter(Members.user_id==user_id).order_by(Games.update_date.desc()).with_entities(Games, Members).all()

        data = []
        for i in range(len(games)):
            game = games[i][0]
            member = games[i][1]
            print(member.approved)
            print(game.title)