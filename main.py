import telebot  # pip install pyTelegramBotApi
import pathlib
import logging

from bot_settings import *
from bot_functions import *
from bot_word_functions import *
from bot_event_functions import *
from bot_leader_functions import *
from bot_player_functions import *
from bot_private_functions import *


Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="logfile.log", filemode="a", format=Log_Format, level=logging.ERROR)
logger = logging.getLogger()
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type == 'private':
        keyboard = telebot.types.InlineKeyboardMarkup()
        vqr_button = telebot.types.InlineKeyboardButton(text="virtualquestchat", url="https://t.me/virtualquestchat")
        pg_button = telebot.types.InlineKeyboardButton(text="paranoya_games", url="https://t.me/paranoya_games")
        keyboard.add(vqr_button)
        keyboard.add(pg_button)
        bot.send_message(message.chat.id, "Для игры перейдите", reply_markup=keyboard)
        time.sleep(1)
        keyboard_1 = telebot.types.InlineKeyboardMarkup()
        button_wallet = telebot.types.InlineKeyboardButton(text='Нажмите сюда', callback_data='wallet')
        keyboard_1.add(button_wallet)
        bot.send_message(message.chat.id, "Для работы с кошельком", reply_markup=keyboard_1)
    else:
        path = pathlib.Path(f'{message.chat.title}.json')
        if not path.is_file():
            if DEBUG:
                bot.send_message(message.chat.id, f"DEBUG:\nПервый запуск...")
            first_run(message)
            bot.send_message(message.chat.id, f"Cоздан файл:\n{message.chat.title}.json"
                                              f"\nВыполните команду /play")
        else:
            if check_leader(message):
                bot.send_message(message.chat.id, f"Игра уже запущена.")
            else:
                bot.send_message(message.chat.id, f"Выполните команду /play")
                play(message)


@bot.message_handler(commands=['play'])
def play(message):
    if DEBUG:
        # bot.send_message(message.chat.id, "Debug:\n")
        bot.send_message(message.chat.id, f"Debug:\nКоманда play\nОткрываем файл с данными")
    if not check_leader(message):
        markup = telebot.types.InlineKeyboardMarkup()
        button_leader = telebot.types.InlineKeyboardButton(text='ЖМИ', callback_data='new_leader')
        markup.add(button_leader)
        if check_leader(message):
            bot.answer_callback_query(callback_query_id=message.from_user.id, text='Вы не ведущий')
        if DEBUG:
            bot.send_message(message.chat.id, "Debug:\nВедущего нет")
        bot.send_message(message.chat.id, "Хочешь быть ведущим?", reply_markup=markup)
    else:
        markup = telebot.types.InlineKeyboardMarkup()
        button_word = telebot.types.InlineKeyboardButton(text='Выбрать/Сменить слово', callback_data='word')
        button_word_remind = telebot.types.InlineKeyboardButton(text='Напомнить слово', callback_data='remind')
        button_leave = telebot.types.InlineKeyboardButton(text='Не хочу быть ведущим', callback_data='leave')
        markup.add(button_word)
        markup.add(button_word_remind)
        markup.add(button_leave)
        bot.send_message(message.chat.id, f"Игра №: {get_game_id(message)}", reply_markup=markup)


@bot.message_handler(commands=['wallet'])
def wallet(message):
    if message.chat.type != 'private':
        bot.send_message(message.chat.id, "Для работы с кошельками перейдите к боту в личные сообщения")


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if DEBUG:
        bot.send_message(call.message.chat.id, "Debug:\nЭто обработчик кнопок")
    if call.data == 'wallet':
        json_file = search_user_data_file(call)
        if not json_file:
            bot.send_message(call.message.chat.id, "Информация не найдена\nСначала примите участие в игре")
        else:
            user_address = get_player_address(call, json_file)
            if not user_address:
                bot.send_message(call.message.chat.id, f"Для добавления кошелька\n"
                                                       f"Отправьте мне ваш адрес VQRC")
            else:
                player_earn = get_player_balance(call, json_file)
                bot.send_message(call.message.chat.id, f"Ваш адрес:\n{user_address}\n"
                                                       f"Для изменения кошелька\n"
                                                       f"Отправьте мне ваш адрес VQRC\n\n"
                                                       f"Для запроса вывода средств\n"
                                                       f"{player_earn} VQRC\n"
                                                       f"Отправьте мне слово ДАЙ")
    else:
        if call.data == 'new_leader':
            if not hidden_word(call):
                if DEBUG:
                    bot.send_message(call.message.chat.id, "Debug:\nЗапоминаем того кто нажал на кнопку быть ведущим")
                add_leader(call)
                bot.send_message(call.message.chat.id, f"Ведущий: {call.from_user.first_name} "
                                                       f"@{call.from_user.username}\n"
                                                       f"{get_player_score(call)}")
                if not check_player(call):
                    if DEBUG:
                        bot.send_message(call.message.chat.id, "Debug:\nДобавляем нового игрока")
                    add_new_player(call)
                time.sleep(1)
                play(call.message)
            else:
                bot.answer_callback_query(callback_query_id=call.id, text='Ведущий уже выбран')
        if check_leader_id(call):
            if call.data == 'word':
                if DEBUG:
                    bot.send_message(call.message.chat.id, "Debug:\nНажатие на кнопку выбора слова")
                bot.answer_callback_query(callback_query_id=call.id, text=word_choice(call), show_alert=True)
            if call.data == 'remind':
                if DEBUG:
                    bot.send_message(call.message.chat.id, "Debug:\nНажатие на кнопку напомнить слово")
                bot.answer_callback_query(callback_query_id=call.id, text=word_remind(call.message), show_alert=True)
            if call.data == 'leave':
                bot.send_message(call.message.chat.id, f"{call.from_user.username} отказался быть ведущим")
                clear_round_data(call.message)
                play(call.message)
        else:
            bot.answer_callback_query(callback_query_id=call.id, text='Вы не ведущий')


@bot.message_handler(commands=['event'])
def event(message):
    admins = bot.get_chat_administrators(message.chat.id)
    if check_admin(message, admins):
        clear_round_data(message)
        if not check_event(message):
            bot.send_message(message.chat.id, f"Начинаем событие!")
            if DEBUG:
                bot.send_message(message.chat.id, f"Обнуляем счет предыдущего события.")
            reset_event(message)
            time.sleep(1)
            play(message)
        else:
            bot.send_message(message.chat.id, f"Событие окончено!\n#event #result")
            bot.send_message(message.chat.id, show_stat(message))
        time.sleep(1)
        event_mode(message)
    else:
        bot.send_message(message.chat.id, f'Изменить режим игры может только администратор')


@bot.message_handler(commands=['score'])
def stat(message):
    top_players = show_stat(message)
    if not check_event(message):
        bot.send_message(message.chat.id, top_players)
    else:
        balance = get_event_address_balance()
        bot.send_message(message.chat.id, f"Event balance: {balance} VQRC\n{top_players}")


@bot.message_handler(commands=['stop'])
def stop(message):
    admins = bot.get_chat_administrators(message.chat.id)
    if check_admin(message, admins):
        clear_round_data(message)
        bot.send_message(message.chat.id, f'Игра остановлена')
    else:
        bot.send_message(message.chat.id, f'Остановить игру может только администратор')


@bot.message_handler(commands=['rules'])
def rules(message):
    bot.send_message(message.chat.id, f'Какие-то правила')


@bot.message_handler(commands=['help'])
def commands(message):
    bot.send_message(message.chat.id, f'Доступные команды:\n/start\n/play\n/score\n/rules\n/help\n\n'
                                      f'Только для администраторов:\n/event\n/stop')


@bot.message_handler(content_types=['text'])
def repeat_all_message(message):
    if message.chat.type == 'private':
        if "VQR" in message.text:
            user_balance = check_address_balance(message.text)
            if user_balance:
                json_file = search_user_data_file(message)
                add_player_address(message, json_file)
                bot.send_message(message.chat.id, f"Адрес:\n{message.text} успешно изменен!\n"
                                                  f"Ваш текущий баланс:\n{user_balance} VQRC")
                start(message)
            else:
                bot.send_message(message.chat.id, f"Адрес:\n{message.text} не найден\n"
                                                  f"Проверьте правильность введенных данных и попробуйте ещё раз")
        if "ДАЙ" in message.text:
            json_file = search_user_data_file(message)
            user_address = get_player_address(message, json_file)
            player_earn = get_player_balance(message, json_file)
            if player_earn < WITHDRAW_LIMIT:
                bot.send_message(message.chat.id, f"Вывод возможен от {WITHDRAW_LIMIT} VQRC")
                start(message)
            else:
                amount = round(player_earn - 0.0001, 4)
                bot.send_message(message.chat.id, f"Делаю транзакцию в размере {amount} VQRC\n"
                                                  f"Если сообщением ниже вы не получите hash обратитесь к "
                                                  f"администратору чата")
                time.sleep(1)
                res = send_funds(user_address, amount)
                bot.send_message(message.chat.id, f"HASH:\n{res}\nhttps://vqr.bitex.one/tx.php?hash={res}")
                take_score(message, json_file)
                start(message)
    else:
        message_lower = message.text.lower()
        message_replace = message_lower.replace('е', 'ё').title()
        message_title = message_lower.title()
        user_message_list = [message_title, message_replace]
        for user_message in user_message_list:
            if DEBUG:
                bot.send_message(message.chat.id, f"Debug:\n{user_message}")
            if word_remind(message) in user_message:
                if get_message_from_leader(message):
                    bot.send_message(message.chat.id, f"@{message.from_user.username} раскрыл слово\n"
                                                      f"и больше не ведущий")
                    clear_round_data(message)
                    play(message)
                else:
                    add_score(message)
                    bot.send_message(message.chat.id, f"{message.from_user.first_name} @{message.from_user.username}\n"
                                                      f"угадал слово:\n{word_remind(message)}")
                    clear_round_data(message)
                    play(message)


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as err:
        logger.error(err)
        logging.exception(err)
        time.sleep(2)
