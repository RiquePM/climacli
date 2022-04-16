import json
from pathlib import Path


class UserData:
    """To do: specify a path to user file"""
    path = "user_data.json"
    
    def __init__(self):
        if Path(self.path).is_file():
            self.TOKEN = self.read_usr_file()["TOKEN"]
            self.city = self.read_usr_file()["default_city"]
        else:
            self.TOKEN = None
            self.city = None
    
    def create_usr_file(self, TOKEN, default_city=None):
        usr_conf = {"TOKEN": TOKEN, "default_city": default_city}
        self.TOKEN = TOKEN
        self.city = default_city

        with open(self.path, 'w') as f:
            json.dump(usr_conf, f)

        return self.TOKEN, self.city
    
    def read_usr_file(self):
        with open(self.path, 'r') as f:
            usr_conf = json.load(f)
            return usr_conf