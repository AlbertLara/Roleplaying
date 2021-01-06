import json
import logging

class ProcessData():
    data = {}
    uid = "ProcessData--"
    def __init__(self):
        json_file = open('queries.json','r',encoding='utf-8')
        self.data = json.loads(json_file.read())

    def process_data(self):
        if 'User' in self.data.keys():
            self.create_users()
        if 'Sistema' in self.data.keys():
            self.create_sistema()

    def create_users(self):
        users = self.data.get('User')
        for user_params in users:
            logging.getLogger(self.uid).info(user_params)
            from .service import UserService
            UserService(**user_params)

    def create_sistema(self):
        sistemas = self.data.get("Sistemas")
        for param in sistemas:
            logging.getLogger(self.uid).info(param)
            from .service import SistemaService
            SistemaService(**param)