from ..models import *
from datetime import datetime




class UserService():
    def __init__(self,**kwargs):
        self.email = kwargs['email']
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.confirmed = kwargs['confirmed']
        try:
            self.is_admin = kwargs['is_admin']
        except:
            self.is_admin = False
        self.create_user()

    def create_user(self):
        user_exists = db.session.query(User).filter_by(username=self.username).count()
        if not user_exists:
            user = User(email=self.email,
                        username=self.username,
                        password=self.password,
                        is_admin=self.is_admin,
                        confirmed=self.confirmed)
            db.session.add(user)
            db.session.commit()


class SistemaService():
    def __init__(self,**kwargs):
        self.nombre = kwargs['nombre']
        self.sKey = kwargs['sKey']
        self.status = kwargs['status']
        self.create_sistema()

    def create_sistema(self):
        exists = db.session.query(Sistema).filter_by(nombre=self.nombre).count() == 1
        if not exists:
            sistema = Sistema(nombre=self.nombre,
                              sKey=self.sKey,
                              status=self.status)
            db.session.add(sistema)
            db.session.commit()

class GameService():

    @classmethod
    def get_games_for_user(self):
        members = current_user.members
        data = []

        for member in members:
            game = member.game
            approved = member.approved
            created = game.master_Id == current_user.id
            game_data = {key:value for key, value in game.__dict__.items() if not str(key).startswith('_')}
            obj = {'approved':approved,'created':created}
            for key, value in game_data.items():
                if isinstance(value, datetime):
                    value = value.strftime('%d/%m/%Y')
                obj[key] = str(value)
                pass
            data.append(obj)
        return data

    def create_game(self,params):
        game = Games(**params)
        db.session.add(game)
        db.session.commit()
        author_id = params['master_Id']
        member = Members(game_id=game.id,
                         user_id=author_id,
                         approved=True)
        db.session.add(member)
        db.session.commit()