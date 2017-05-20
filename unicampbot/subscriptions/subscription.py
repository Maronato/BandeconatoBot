from unicampbot.database.subscriptions_api import get_subscription, set_subscription
from unicampbot.communication.basic import inline_keyboard_message, edit_message, answer_callback_query
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import emoji


class Subscription:
    """docstring for Subscription"""

    def __init__(self, chat_id, callback=False, message_id=False, extra_info={'S': ""}):
        self.chat_id = chat_id
        self.message_id = message_id
        self.callback = callback
        self.extra_info = extra_info

    def update_subscription(self, changed):
        subs = self.subs
        subs[changed] = not subs[changed]
        set_subscription(self.chat_id, subs, extra=self.extra_info)
        self.get_subs()
        return self

    def interact(self):
        sender_method = edit_message if self.callback else inline_keyboard_message
        sender_method(*self.menu_tuple)
        if self.callback:
            answer_callback_query(self.callback)
        return self

    def get_subs(self):
        subs = get_subscription(self.chat_id)
        # Create a new one if the user is new
        if not subs:
            subs = {
                'breakfast': False,
                'lunch': False,
                'veglunch': False,
                'dinner': False,
                'vegdinner': False
            }
        self.loadedsubs = subs
        return self

    @property
    def menu_tuple(self):
        message = """*Inscrições*\n
Toque uma opção para se inscrever nela.
Toque novamente para se desinscrever.\n
As mensagens de café da manhã são enviadas por volta das 6 da manhã.
As de almoço por volta das 10 e as de jantar por volta das 16.
"""

        subs = self.subs
        sub_sign = emoji.emojize(':white_heavy_check_mark:  ', use_aliases=True)

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=(sub_sign if subs['breakfast'] else '') + 'Café da manhã', callback_data='sub.breakfast')],
            [
                InlineKeyboardButton(text=(sub_sign if subs['lunch'] else '') + 'Almoço', callback_data='sub.lunch'),
                InlineKeyboardButton(text=(sub_sign if subs['veglunch'] else '') + 'Almoço veg', callback_data='sub.veglunch')
            ],
            [
                InlineKeyboardButton(text=(sub_sign if subs['dinner'] else '') + 'Jantar', callback_data='sub.dinner'),
                InlineKeyboardButton(text=(sub_sign if subs['vegdinner'] else '') + 'Jantar veg', callback_data='sub.vegdinner')
            ],
        ])
        response_id = self.message_id or self.chat_id
        return [response_id, message, keyboard]

    @property
    def subs(self):
        subs = getattr(self, "loadedsubs", False)
        if not subs:
            self.get_subs()
        return self.loadedsubs
