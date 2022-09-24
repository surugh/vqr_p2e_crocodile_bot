import json


def check_player(call) -> bool:
    with open(f'{call.message.chat.title}.json', 'r') as f:
        chat_data = json.load(f)
    for players in chat_data['players']:
        if call.from_user.id == players['id']:
            return True


def add_new_player(call):  # To *.json
    with open(f'{call.message.chat.title}.json', 'r') as f:
        chat_data = json.load(f)
    chat_data['players'].append(dict(id=call.from_user.id, first_name=call.from_user.first_name,
                                     username=call.from_user.username, total_score=0, event_score=0,
                                     address=None))
    with open(f'{call.message.chat.title}.json', 'w') as f:
        json.dump(chat_data, f, indent=4, ensure_ascii=False)


def get_player_score(call) -> str:
    with open(f'{call.message.chat.title}.json', 'r') as f:
        chat_data = json.load(f)
    for player in chat_data['players']:
        if call.from_user.id == player['id']:
            if not chat_data['is_event']:
                return f"Счет: {player['total_score']}"
            else:
                return f"Earn: {player['event_score']} VQRC"


def add_score(message):
    with open(f'{message.chat.title}.json', 'r') as f:
        chat_data = json.load(f)
    for data in chat_data['players']:
        if data['id'] == message.from_user.id:
            if not chat_data['is_event']:
                data['total_score'] = data['total_score'] + 1
                with open(f'{message.chat.title}.json', 'w') as w:
                    json.dump(chat_data, w, indent=4)
                return data['total_score']
            else:
                data['event_score'] = round(data['event_score'] + 0.0001, 4)
                with open(f'{message.chat.title}.json', 'w') as w:
                    json.dump(chat_data, w, indent=4)
                return data['event_score']
