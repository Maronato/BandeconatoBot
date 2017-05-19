import telepot
import os

TOKEN = os.environ.get('TELEGRAM_TOKEN', None)
bot = telepot.Bot(TOKEN)


def simple_message(chat_id, message):
    bot.sendMessage(chat_id, message)


def markdown_message(chat_id, message):
    print(chat_id, message)
    bot.sendMessage(chat_id, message, parse_mode="Markdown")


def html_message(chat_id, message):
    bot.sendMessage(chat_id, message, parse_mode="HTML")


def inline_keyboard_message(chat_id, message, keyboard):

    bot.sendMessage(chat_id, message, reply_markup=keyboard, parse_mode="Markdown")


def edit_message(message_id, message, reply_markup=None):
    bot.editMessageText(message_id, message, reply_markup=reply_markup, parse_mode="Markdown")


def answer_callback_query(query_id, message='', show_alert=False):
    bot.answerCallbackQuery(query_id, message, show_alert)
