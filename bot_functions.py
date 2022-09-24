import time
import json

from bot_word_functions import word_clear
from bot_leader_functions import clear_leader


def first_run(message):  # Create *.json
    players = [dict(id=message.from_user.id, first_name=message.from_user.first_name,
                    username=message.from_user.username, total_score=0, event_score=0, address=None)]
    with open(f'{message.chat.title}.json', 'w+') as f:
        json.dump(dict(chat_id=message.chat.id, game_id=0, is_event=None, leader_id=None, hidden_word=None,
                       players=players), f, indent=4, ensure_ascii=False)


def check_admin(message, admins) -> bool:
    admins_list = []
    for admin in admins:
        if not admin.user.is_bot:
            admins_list.append(admin.user.id)
    for admin_id in admins_list:
        if message.from_user.id == admin_id:
            return True


def get_game_id(message) -> int:
    with open(f'{message.chat.title}.json', 'r') as f:
        chat_data = json.load(f)
    chat_data['game_id'] = chat_data['game_id'] + 1
    with open(f'{message.chat.title}.json', 'w') as f:
        json.dump(chat_data, f, indent=4, ensure_ascii=False)
    return chat_data['game_id']


def show_stat(message) -> str:
    with open(f'{message.chat.title}.json', 'r') as f:
        players_dict = json.load(f)
        new_dict = {}
        for player in players_dict['players']:
            if not players_dict['is_event']:
                new_dict[player['first_name']] = player['total_score']
            else:
                new_dict[player['first_name']] = player['event_score']
        sorted_new_dict_tuples = sorted(new_dict.items(), key=lambda item: item[1], reverse=True)
        sorted_dict = {k: v for k, v in sorted_new_dict_tuples}
        message_text = []
        place = 0
        for k in sorted_dict:
            place += 1
            if not players_dict['is_event']:
                message_text.append(f'{place}. Счет: {sorted_dict.get(k)} - {k}')
            else:
                message_text.append(f'{place}. Earn: {sorted_dict.get(k)} VQRC - {k}')
        return '\n'.join(message_text)


def clear_round_data(message):
    clear_leader(message)
    word_clear(message)
    time.sleep(1)

