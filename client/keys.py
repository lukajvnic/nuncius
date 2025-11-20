import json


def get_pubkeys():
    with open("pubkeys.json", "r") as file:
        return json.loads(file.read())
    

def update_pubkeys(pubkeys_dict):
    with open("pubkeys.json", "w") as file:
        file.write(json.dumps(pubkeys_dict, indent=4))
