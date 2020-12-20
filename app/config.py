import json


class Configuration():
    __data = {}
    def __init__(self,filename):
        json_file = open(filename,"r",encoding="utf8")
        data = json.load(json_file)
        self.__data = data

    def get_query_params(self,key):
        return self.__data.get("queries").get(key)

    def get_app_config(self):
        obj = self.__data.get("APP")
        return dict(obj)

    def get_params(self,key):
        return self.__data.get(key)