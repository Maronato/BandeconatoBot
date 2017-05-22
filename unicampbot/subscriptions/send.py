from unicampbot.database.subscriptions_api import get_all_subscriptions, get_subscription
from unicampbot.menu.cardapio import Cardapio
from unicampbot.communication.basic import markdown_message

import os


class SubscriptionSender:
    """docstring for SubscriptionSender"""

    def __init__(self, menu_type, debug=False):
        self.menu_type = menu_type
        self.debug = debug

        print(menu_type, debug)

        if menu_type == "lunch":
            self.menus = ["lunch", "veglunch"]
        elif menu_type == "dinner":
            self.menus = ["dinner", "vegdinner"]
        else:
            self.menus = ["breakfast"]

    titles = {
        "breakfast": "*Café da manhã de hoje*\n\n",
        "lunch": "*Almoço de hoje*\n\n",
        "veglunch": "*Almoço vegetariano de hoje*\n\n",
        "dinner": "*Jantar de hoje*\n\n",
        "vegdinner": "*Jantar vegetariano de hoje*\n\n"
    }

    def send(self):
        if self.debug:
            chats = [{'sub': get_subscription(os.environ.get("DEV_CHAT_ID")), 'id': os.environ.get("DEV_CHAT_ID")}]
        else:
            chats = get_all_subscriptions()
        mensagens = {}
        for menu in self.menus:
            cardapio = Cardapio()
            cardapio = getattr(cardapio, menu)
            msg = self.titles.get(menu)
            msg += cardapio
            mensagens[menu] = msg

        for chat in chats:
            for menu in self.menus:
                if chat['sub'].get(menu, False):
                    markdown_message(chat['id'], mensagens[menu])
