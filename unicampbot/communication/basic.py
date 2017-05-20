import telepot
import os

TOKEN = os.environ.get('TELEGRAM_TOKEN', None)
bot = telepot.Bot(TOKEN)


def simple_message(chat_id, message, **kwargs):
    bot.sendMessage(chat_id, message, **kwargs)


def markdown_message(chat_id, message, **kwargs):
    simple_message(chat_id, message, parse_mode="Markdown", **kwargs)


def html_message(chat_id, message, **kwargs):
    simple_message(chat_id, message, parse_mode="HTML", **kwargs)


def inline_keyboard_message(chat_id, message, keyboard, **kwargs):
    simple_message(chat_id, message, parse_mode="Markdown", reply_markup=keyboard, **kwargs)


def edit_message(message_id, message, **kwargs):
    bot.editMessageText(message_id, message, parse_mode="Markdown", **kwargs)


def answer_callback_query(query_id, message='', show_alert=False, **kwargs):
    bot.answerCallbackQuery(query_id, message, show_alert, **kwargs)
