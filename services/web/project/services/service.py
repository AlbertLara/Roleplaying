from ..models import *
from datetime import datetime
from flask_login import current_user
from ..models import *
from ..schema import *
import json
import os


"""class Service():
    name = ''
    def __init__(self):
        self.endpoint = os.environ.get('ENDPOINT')
        self.session = session
        self.url = f"{self.endpoint}/{self.name}"

    def exist_record(self,payload:dict):
        print(payload)
        query = "&".join([f"{key}={value}" for key, value in payload.items()])
        print(query)
        url = f"{self.url}?{query}"
        response = self.session.get(url)
        return response.status_code == 200

    def insert_data(self,payload):
        print(self.url)
        response = self.session.post(self.url,json=json.dumps(payload))
        return response.status_code

class UserService(Service):
    name = 'users'
    def verifyCredentials(self,credentials):
        url = f"{self.url}/verifyUser?credentials={credentials}"
        response = self.session.get(url)
        status_code = response.status_code
        data = {}
        if status_code == 200:
            data = response.json()
        return {'status_code':status_code,'data':data}


class SistemaService(Service):
    name = 'sistemas'

    def get_active(self):
        url = f"{self.url}?status=a"
        response = self.session.get(url)
        if response.status_code == 200:
            data = response.json()
            values = [(row['id'],row['nombre']) for row in data]
            return values"""

class SistemaService():
    def get_active(self):
        sistemas = Sistema.get_by_status("a")
        data = sistema_schema.dump(sistemas,many=True)
        values = [(row['id'],row['nombre']) for row in data]
        print(values)
        return values

class GameService():
    def get_games_for_user(self):
        userId = current_user.id
        members = Members.query.filter_by(user_id=userId).all()
        games = [member.game for member in members]
        data = game_schema.dump(games,many=True)
        return data

    def get_unjoined(self):
        userId = current_user.id
        all_games = Games.query.filter_by(is_public=True).all()
        games = []
        for game in all_games:
            members = [member.user_id for member in game.members]
            is_member = userId in members
            if not is_member:
                games.append(game)
        data = game_member_schema.dump(games,many=True)
        print(data)
        return data
