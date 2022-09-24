import json
import random
# import requests
# from bs4 import BeautifulSoup  # pip install bs4


def random_line(txt_file):
    """
    Эта функция выбирает случайную строку из текстового файла
    """
    try:
        # Возвращаем следующий элемент объекта итератора
        line = next(txt_file)
        # Для каждого кол-ва итераций и значения элемента на текущей итерации
        for line_num, line_value in enumerate(txt_file, 2):
            # Возвращаем случайное число из диапазона
            if random.randrange(line_num):
                continue
            line = line_value
        # Проверяем строку на нежелательные символы
        if "\n" in line:
            return line.replace("\n", "")
        return line
    except StopIteration:
        return


def word_choice(call) -> str:
    """
    Выбирает слово из файла и сохраняет его в нужном регистре.
    Спасибо за словарь:
     https://github.com/Harrix/Russian-Nouns
     https://harrix.dev/blog/2018/russian-nouns/
    :return: str
    """
    word = random_line(open("russian_nouns.txt", encoding='utf-8'))
    with open(f'{call.message.chat.title}.json', 'r') as f:
        chat_data = json.load(f)
    chat_data['hidden_word'] = word.capitalize()
    with open(f'{call.message.chat.title}.json', 'w') as f:
        json.dump(chat_data, f, indent=4, ensure_ascii=False)
    return word.capitalize()


# def word_choice(call):
#     """
#     Эта функция берет рандомные слова со стороннего ресурса.
#     :return: str
#     """
#     html = requests.get(
#         "https://calculator888.ru/random-generator/sluchaynoye-slovo"
#     ).text
#     bs4 = BeautifulSoup(html, "html.parser")
#     tables = bs4.find_all("div", class_="blok_otvet")  # получаем список таблиц
#     for table in tables:
#         with open(f'{call.message.chat.title}.json', 'r') as f:
#             chat_data = json.load(f)
#         chat_data['hidden_word'] = table.text
#         with open(f'{call.message.chat.title}.json', 'w') as f:
#             json.dump(chat_data, f, indent=4, ensure_ascii=False)
#         return table.text


def word_remind(message) -> str:
    with open(f'{message.chat.title}.json', 'r') as f:
        chat_data = json.load(f)
    if not chat_data['hidden_word']:
        return f"Слово не загадано"
    else:
        return chat_data['hidden_word']


def word_clear(message):
    with open(f'{message.chat.title}.json', 'r') as f:
        chat_data = json.load(f)
    chat_data['hidden_word'] = None
    with open(f'{message.chat.title}.json', 'w') as f:
        json.dump(chat_data, f, indent=4, ensure_ascii=False)


def hidden_word(call) -> bool:
    with open(f'{call.message.chat.title}.json', 'r') as f:
        chat_data = json.load(f)
    if chat_data['hidden_word']:
        return True
