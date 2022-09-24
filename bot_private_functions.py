import os
import json
import time
import requests


def search_user_data_file(call):
    path = os.getcwd()
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".json"):
                file_is = os.path.join(file)
                # group_name = file_is.replace(".json", "")
                # print(file_is, group_name)
                with open(f'{file_is}', 'r') as f:
                    chat_data = json.load(f)
                for players in chat_data['players']:
                    if call.from_user.id == players['id']:
                        # print(group_name)
                        return file_is


def get_player_address(call, file) -> str:
    with open(f'{file}', 'r') as f:
        chat_data = json.load(f)
    for player in chat_data['players']:
        if call.from_user.id == player['id']:
            return player['address']


def check_address_balance(address):
    url = 'https://masternode.vqr.quest/api.php?'
    response = requests.get(f'{url}action=balance&addr={address}').json()
    return response['balance']


def add_player_address(message, file):
    with open(f'{file}', 'r') as f:
        chat_data = json.load(f)
    for data in chat_data['players']:
        if data['id'] == message.from_user.id:
            data['address'] = message.text
            with open(f'{file}', 'w') as w:
                json.dump(chat_data, w, indent=4)
            return data['address']


def get_player_balance(call, file) -> float:
    with open(f'{file}', 'r') as f:
        chat_data = json.load(f)
    for player in chat_data['players']:
        if call.from_user.id == player['id']:
            return float(player['event_score'])


def send_funds(address, quantity):
    os.system("cd")
    time.sleep(1)
    cmd = f"/home/ubuntu/./vqr-cli sendtoaddress {address} {quantity}"
    send = os.popen(cmd).read()
    return send


def take_score(message, file):
    with open(f'{file}', 'r') as f:
        chat_data = json.load(f)
    for data in chat_data['players']:
        if data['id'] == message.from_user.id:
            data['event_score'] = round(data['event_score'] - 0.0011, 4)
            with open(f'{file}', 'w') as w:
                json.dump(chat_data, w, indent=4)
            return data['event_score']
