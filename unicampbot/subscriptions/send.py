from bandecoapi.api.api import get_menu

from unicampbot.database.subscriptions_api import get_all_subscriptions, get_subscription
from unicampbot.communication.basic import markdown_message

import os


class SubscriptionSender:
    """docstring for SubscriptionSender"""

    def __init__(self, menu, debug=False, hours_delta=-3, debug_days_delta=0):
        self.menu_type = menu
        self.debug = debug
        self.hours_delta = hours_delta
        self.debug_days_delta = debug_days_delta

        print(menu, debug)

        if menu == "lunch":
            self.menus = ["lunch", "veglunch"]
        elif menu == "dinner":
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

        menus = get_menu(menus=self.menus, hours_delta=self.hours_delta, days_delta=self.debug_days_delta)

        if menus.get("error"):
            # TODO report error here
            print("ERROR: ", menus.get("error"))
            return
        for key, menu in menus['menu'].items():
            msg = self.titles.get(key)
            msg += menu
            mensagens[key] = msg

        for chat in chats:
            for menu in self.menus:
                if chat['sub'].get(menu, False):
                    markdown_message(chat['id'], mensagens[menu])
