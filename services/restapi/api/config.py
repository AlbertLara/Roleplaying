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
        self.__data = data

    def get_query_params(self,key):
        return self.__data.get("queries").get(key)

    def get_app_config(self):
        obj = self.__data.get("APP")
        return dict(obj)

    def get_params(self,key):
        return self.__data.get(key)