from tkinter.constants import INSERT

import telebot
from telebot import types

bot = telebot.TeleBot('TOKEN')

user_text = {}  # Используем словарь, чтобы сохранять текст для каждого пользователя

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, рад тебя видеть! \nОтправить мне текст, который тебе нужно отформатировать')

    # пользователь вводит текст

@bot.message_handler(content_types=['text'])
def format_text(message):

    global user_text
    user_text[message.chat.id] = message.text.strip()                     # Сохраняем текст пользователя

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('ВСЕ ЗАГЛАВНЫЕ', callback_data='upper')
    btn2 = types.InlineKeyboardButton('все маленькие', callback_data='lower')
    btn3 = types.InlineKeyboardButton('Каждое Слово С Заглавной Буквы', callback_data='title')
    btn4 = types.InlineKeyboardButton('🐍 Заменить пробелы на _', callback_data='snake')
    btn5 = types.InlineKeyboardButton('тскеТ йынтарбО', callback_data='reverse')

    markup.row(btn1, btn2)
    markup.row(btn3)
    markup.row(btn4)
    markup.row(btn5)

    bot.send_message(message.chat.id, 'Выбери регистр:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_message(callback):
    chat_id = callback.message.chat.id
    if chat_id in user_text:                                              # Проверяем, есть ли сохраненный текст

        if callback.data == 'upper':
            bot.send_message(chat_id, user_text[chat_id].upper())
        elif callback.data == 'lower':
            bot.send_message(chat_id, user_text[chat_id].lower())
        elif callback.data == 'title':
            bot.send_message(chat_id, user_text[chat_id].title())
        elif callback.data == 'snake':
            bot.send_message(chat_id, user_text[chat_id].replace(' ', '_').lower())
        elif callback.data == 'reverse':
            bot.send_message(chat_id, user_text[chat_id][::-1])
    else:
        bot.send_message(chat_id, 'Сначала отправьте текст!')

bot.polling(non_stop=True)
