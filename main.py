import random
from logging import exception

import telebot
import json

from pyexpat.errors import messages

TOKEN = '7806372947:AAElfeN44-af9OevCf4RYm2DDpxm3KMMiSU'

bot = telebot.TeleBot(TOKEN)

# user_data = {}

try:
    with open('user_data.json', 'r', encoding='utf-8') as file:
        user_data = json.load(file)

except FileNotFoundError:
    user_data = {}
    print('Файл не найен')


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, 'Привет. Это твой бот! Скоро тут будет много инересных функций')


@bot.message_handler(commands=['learn'])
def handle_learn(message):
    user_words = user_data.get(str(message.chat.id), {})

    if len(user_data) > 0:
        try:
            words_number = int(message.text.split()[1])
            ask_translation(message.chat.id, user_words, words_number)
        except ValueError:
            bot.send_message(message.chat.id, "Используй команду /learn <количество цифрами>")
        except IndexError:
            bot.send_message(message.chat.id, "Напиши другое число")

    else:
        bot.send_message(message.chat.id, "В словаре еще нет слов. Необходимо их добавить.")
        return


def ask_translation(chat_id, user_words, words_left):
    if words_left > 0:
        word = random.choice(list(user_words.keys()))
        translation = user_words[word]
        bot.send_message(chat_id, f"Напиши перевод слова '{word}'.")

        bot.register_next_step_handler_by_chat_id(chat_id, check_translation, translation, words_left)

    else:
        bot.send_message(chat_id, "Урок закончен.")


def check_translation(message, expected_translation, words_left):
    user_translation = message.text.strip().lower()
    if user_translation == expected_translation.lower():
        bot.send_message(message.chat.id, f"Правильно! Молодец!")
    else:
        bot.send_message(message.chat.id, f"Неправильно. Правильный перевод: {expected_translation}")

    ask_translation(message.chat.id, user_data[str(message.chat.id)], words_left - 1)


@bot.message_handler(commands=['addword'])
def handle_addword(message):
    global user_data
    chat_id = message.chat.id
    user_dict = user_data.get(chat_id, {})

    try:
        words = message.text.split()[1:]
        if len(words) == 2:
            word, translation = words[0].lower(), words[1].lower()
            user_dict[word] = translation

            user_data[chat_id] = user_dict

            with open('user_data.json', 'w', encoding='utf-8') as file:
                json.dump(user_data, file, ensure_ascii=False, indent=4)
            bot.send_message(chat_id, f"Слово '{word}' добвлено в словарь. ")
        else:
            bot.send_message(chat_id, f'Произошла ошибка. Попробуйте еще раз')
    except Exception as e:
        bot.send_message(chat_id, f'Что-то пошло не так. Попробуйте еще раз')


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, 'Этот бот поможет тебе при обучении английского языка.')
    bot.send_message(message.chat.id, 'Вот список доступных команд: ')
    bot.send_message(message.chat.id, '/start - комнада запуска бота')
    bot.send_message(message.chat.id, '/learn - команда начала обучения')
    bot.send_message(message.chat.id, '/help - команда вызова помощи')
    bot.send_message(message.chat.id, 'Автор: Кристина')


@bot.message_handler(func=lambda message: True)
def handle_all(message):
    if message.text.lower() == 'как дела?':
        bot.send_message(message.chat.id, 'все отлично!')
    elif message.text.lower() == 'как тебя зовут?':
        bot.send_message(message.chat.id, 'у меня пока еще нет имени')


if __name__ == "__main__":
    bot.polling(none_stop=True)