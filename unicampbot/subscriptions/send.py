from bandecoapi.api import get_menu
from telepot.exception import BotWasBlockedError

from unicampbot.database.subscriptions_api import get_all_subscriptions, delete_chat
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
        print("Sending subs")
        chats = get_all_subscriptions()
        if self.debug:
            chats = list(filter(lambda x: str(x['id']) == str(os.environ.get("DEV_CHAT_ID")), chats))

        print(len(chats), "chats selected")
        mensagens = {}

        menus = get_menu(menus=self.menus, hours_delta=self.hours_delta, days_delta=self.debug_days_delta)

        print("Building message")
        if menus.get("error"):
            # TODO report error here
            print("ERROR: ", menus.get("error"))
            return
        for key, menu in menus['menu'].items():
            msg = self.titles.get(key)
            msg += menu
            mensagens[key] = msg

        print("Sending subs")
        for k, chat in enumerate(chats):
            print("Sending sub", k)
            for menu in self.menus:
                if chat['sub'].get(menu, False):
                    # Try to send
                    try:
                        markdown_message(chat['id'], mensagens[menu])
                        print("Sub '", menu, "' sent to user", k)
                    except BotWasBlockedError as e:
                        try:
                            if chat['extra']['chat_type']['S'] == 'private':
                                username = chat['extra']['username']['S']
                                name = chat['extra']['first_name']['S'] + " " + chat['extra']['last_name']['S']
                                info = "User {}({}) with ID {} blocked the bot and is being removed from the table".format(name, username, chat['id'])
                            elif chat['extra']['chat_type']['S'] == 'group':
                                group_name = chat['extra']['first_name']['S']
                                info = "Group {} with ID {} blocked the bot and is being removed from the table".format(group_name, chat['id'])
                        except KeyError:
                            info = "Unknown with ID {} blocked the bot and is being removed from the table".format(chat['id'])

                        # Log error
                        print("EXCEPTION: ", info)
                        delete_chat(chat['id'])
                    except Exception as e:

                        # Log error
                        print("EXCEPTION: An error has occured when sending sub notification to chat ID {}:\n{}".format(chat['id'], e))
                else:
                    print("User", k, "not subscribed to", menu)
