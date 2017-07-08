from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from bandecoapi.api.api import get_menu

from unicampbot.communication.basic import edit_message, answer_callback_query, inline_keyboard_message
from .quotes import quote_choice


day_ref = {
    '0': 'hoje',
    '1': 'amanhã',
    '2': 'depois de amanhã'
}
menu_trans_options = {
    'bf': 'Café da manhã',
    'al': 'Almoço',
    'av': 'Almoço vegetariano',
    'jn': 'Jantar',
    'jv': 'Jantar vegetariano'
}


def day_keyboard(message_id, query_id=False):
    message = "*Cardápio*\n\nEscolha o dia que deseja saber o cardápio."

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Hoje', callback_data='menu.0')],
        [InlineKeyboardButton(text='Amanhã', callback_data='menu.1')],
        [InlineKeyboardButton(text='Depois de amanhã', callback_data='menu.2')],
    ])
    if query_id:
        edit_message(message_id, message, keyboard)
        answer_callback_query(query_id)
    else:
        inline_keyboard_message(message_id, message, keyboard)


def menu_keyboard(day, message_id, query_id):
    response = "*Cardápio de " + day_ref[str(day)] + "*\n\nEscolha o cardápio que deseja saber."

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Café da manhã', callback_data='menu.' + str(day) + '.bf')],
        [
            InlineKeyboardButton(text='Almoço', callback_data='menu.' + str(day) + '.al'),
            InlineKeyboardButton(text='Almoço veg', callback_data='menu.' + str(day) + '.av')
        ],
        [
            InlineKeyboardButton(text='Jantar', callback_data='menu.' + str(day) + '.jn'),
            InlineKeyboardButton(text='Jantar veg', callback_data='menu.' + str(day) + '.jv')
        ],
        [InlineKeyboardButton(text='<< Voltar', callback_data='menu')],
    ])
    edit_message(message_id, response, keyboard)
    answer_callback_query(query_id)


def menu_view(day, option, message_id, query_id):

    menu_options = {
        'bf': 'breakfast',
        'al': 'lunch',
        'av': 'veglunch',
        'jn': 'dinner',
        'jv': 'vegdinner'
    }

    menu = get_menu(menus=[menu_options[option]], days_delta=int(day), hours_delta=-3)

    if menu.get("error", False):
        menu = menu["error"]
        quote = ""
    else:
        menu = menu["menu"][menu_options[option]]
        quote = quote_choice()

    response = '\n\n'.join(["*" + menu_trans_options[option] + ' de ' + day_ref[str(day)] + '*', menu, quote])

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='<< Voltar', callback_data='menu.' + str(day))],
    ])
    edit_message(message_id, response, keyboard)
    answer_callback_query(query_id)
