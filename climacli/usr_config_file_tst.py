"""To do: Create a class to handle the persistence of user data into a file"""
import json


def create_usr_file(token, default_city=None):
    usr_conf = {"TOKEN": token, "default_city": default_city}
    
    with open('usr_confg_file_tst.json', 'w') as f:
        json.dump(usr_conf, f)

def read_usr_file():
    with open('usr_confg_file_tst.json', 'r') as f:
        usr_conf = json.load(f)
        return usr_conf