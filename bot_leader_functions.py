import json


def add_leader(call):
    with open(f'{call.message.chat.title}.json', 'r') as f:
        chat_data = json.load(f)
    chat_data['leader_id'] = call.from_user.id
    with open(f'{call.message.chat.title}.json', 'w') as f:
        json.dump(chat_data, f, indent=4, ensure_ascii=False)


def check_leader(message) -> bool:
    with open(f'{message.chat.title}.json', 'r') as f:
        chat_data = json.load(f)
    if chat_data['leader_id']:
        return True


def check_leader_id(call) -> bool:
    with open(f'{call.message.chat.title}.json', 'r') as f:
        chat_data = json.load(f)
    if chat_data['leader_id'] == call.from_user.id:
        return True


def get_message_from_leader(message) -> bool:
    with open(f'{message.chat.title}.json', 'r') as f:
        chat_data = json.load(f)
    if chat_data['leader_id'] == message.from_user.id:
        return True


def clear_leader(message):
    with open(f'{message.chat.title}.json', 'r') as f:
        chat_data = json.load(f)
    chat_data['leader_id'] = None
    with open(f'{message.chat.title}.json', 'w') as f:
        json.dump(chat_data, f, indent=4, ensure_ascii=False)
