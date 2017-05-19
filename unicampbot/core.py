import telepot
from unicampbot.commands import commands
from unicampbot.menu.keyboards import day_keyboard, menu_keyboard, menu_view
from unicampbot.subscriptions.send import SubscriptionSender
from unicampbot.subscriptions.subscription import Subscription
from unicampbot.communication.basic import simple_message


def receiver(data):
    """Receives data from Lambda
    """

    # Handlers
    update_types = {
        'message': _message,
        'edited_message': _edited_message,
        'channel_post': _channel_post,
        'edited_channel_post': _edited_channel_post,
        'inline_query': _inline_query,
        'chosen_inline_result': _chosen_inline_result,
        'callback_query': _callback_query
    }

    # Get update info
    for key in data:
        if key == 'update_id':
            update_id = data[key]
        else:
            update_type = key

    # Call correct handler passing correct values
    update_types[update_type](update_id, data[update_type])


# Handlers below
def _message(update_id, msg):
    """Message handler"""

    # Get basic info
    content_type, chat_type, chat_id = telepot.glance(msg)

    # If the message is a text message
    if content_type == 'text':

        # Get its text
        text = msg['text']

        # Private chat commands
        if chat_type == 'private':
            if text.strip() == '/start':
                commands.start(chat_id)

            elif text.strip() == '/help':
                commands.help(chat_id)

            elif text.strip() == '/creditos':
                commands.creditos(chat_id)

            elif text.strip() in ['cardapio', '/cardapio']:
                commands.cardapio(chat_id)

            elif text.strip() in ['inscrever', '/inscrever']:
                commands.inscrever(chat_id)

            else:
                simple_message(chat_id, "Não reconheço esse comando :(\n\n/help - Lista de comandos")

        # Group chat commands
        if chat_type == 'group':
            if text.strip() in ['/start', '@BandeconatoBot']:
                commands.start(chat_id)

            elif text.strip() in ['/help', '/help@BandeconatoBot']:
                commands.help(chat_id)

            elif text.strip() in ['/creditos', '/creditos@BandeconatoBot']:
                commands.creditos(chat_id)

            elif text.strip() in ['/cardapio', '/cardapio@BandeconatoBot']:
                commands.cardapio(chat_id)

            elif text.strip() in ['/inscrever', '/inscrever@BandeconatoBot']:
                commands.inscrever(chat_id)

            else:
                simple_message(chat_id, "Não reconheço esse comando :(\n\n/help - Lista de comandos")


def _edited_message(update_id, msg):
    """Edited message handler"""
    pass


def _channel_post(update_id, msg):
    """Channel post handler"""
    pass


def _edited_channel_post(update_id, msg):
    """Edited channel post handler"""
    pass


def _inline_query(update_id, in_query):
    """Inline query handler"""
    pass


def _chosen_inline_result(update_id, in_query_res):
    """Choosen inline result handler"""
    pass


def _callback_query(update_id, callback_query):
    """Callback query handler"""

    # Get callback's basic info
    query_id, from_id, query_data = telepot.glance(callback_query, flavor='callback_query')

    # Build message identification
    try:
        message_id = telepot.message_identifier(callback_query)
    except ValueError:
        message_id = (callback_query['message']['chat']['id'], callback_query['message']['message_id'])

    # Navigate the callback if it came from the menu
    if query_data.split('.')[0] == 'menu':

        # Pass arguments to callback response constructors
        if len(query_data.split('.')) == 1:
            day_keyboard(message_id, query_id)

        elif len(query_data.split('.')) == 2:
            menu_keyboard(query_data.split('.')[1], message_id, query_id)

        elif len(query_data.split('.')) == 3:
            menu_view(query_data.split('.')[1], query_data.split('.')[2], message_id, query_id)

    # Navigate the callback if it came from the subscription command
    if query_data.split('.')[0] == 'sub':

        # Get the changed subscription
        changed_sub = query_data.split('.')[1]
        # Get the chat id
        chat_id = callback_query['message']['chat']['id']
        # Update subscription and respond to query
        Subscription(chat_id, query_id, message_id).update_subscription(changed_sub).interact()


def send_subscriptions(sub):
    SubscriptionSender(sub['menu'], sub.get('debug', False)).send()
