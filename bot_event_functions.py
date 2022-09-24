import json
import requests


def get_event_address_balance(address='VQRe1skpSUMChZ37bpJg7Dtz4rSzrzutPKZK'):
    url = 'https://masternode.vqr.quest/api.php?'
    response = requests.get(f'{url}action=balance&addr={address}').json()
    return round(response['balance'], 4)


def check_event(message) -> bool:
    with open(f'{message.chat.title}.json', 'r') as f:
        chat_data = json.load(f)
    if chat_data['is_event']:
        return True


def event_mode(message):
    with open(f'{message.chat.title}.json', 'r') as f:
        chat_data = json.load(f)
    if not chat_data['is_event']:
        chat_data['is_event'] = True
    else:
        chat_data['is_event'] = False
    with open(f'{message.chat.title}.json', 'w') as f:
        json.dump(chat_data, f, indent=4, ensure_ascii=False)


def reset_event(message):
    with open(f'{message.chat.title}.json', 'r') as r:
        chat_data = json.load(r)
    for data in chat_data['players']:
        data['event_score'] = 0
    with open(f'{message.chat.title}.json', 'w') as w:
        json.dump(chat_data, w, indent=4)
