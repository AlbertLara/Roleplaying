import json
import os
from dotenv import dotenv_values

class Configuration():
    __data = {}
    def __init__(self):
        data = {"APP":{}}
        apps = os.environ.get("APP").split(" ")
        for key in apps:
            v = os.environ.get(key)
            value = str(v)
            if v.isnumeric():
                value = int(v)
            elif v.lower() in ('true','false'):
                value= v.lower() == 'true'
            data['APP'][key] = value
        user_id = os.environ.get("POSTGRES_USER")
        user_pwd = os.environ.get("POSTGRES_PWD")
        host = os.environ.get("POSTGRES_HOST")
        port = os.environ.get("POSTGRES_PORT")
        db = os.environ.get("POSTGRES_DB")
        data['APP']['JWT_BLACKLIST_TOKEN_CHECKS'] =os.environ.get('JWT_BLACKLIST_TOKEN_CHECKS').split(" ")
        data['APP']['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{user_id}:{user_pwd}@{host}:{port}/{db}'
        self.__data = data

    def get_query_params(self,key):
        return self.__data.get("queries").get(key)

    def get_app_config(self):
        obj = self.__data.get("APP")
        return dict(obj)

    def get_params(self,key):
        return self.__data.get(key)