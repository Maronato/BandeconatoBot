from unicampbot.database.subscriptions_api import get_subscription, set_subscription
from unicampbot.communication.basic import inline_keyboard_message, edit_message, answer_callback_query
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


class Subscription:
    """docstring for Subscription"""

    def __init__(self, chat_id, callback=False, message_id=False):
        self.chat_id = chat_id
        self.message_id = message_id
        self.callback = callback

    def update_subscription(self, changed):
        subs = self.subs
        subs[changed] = not subs[changed]
        set_subscription(self.chat_id, subs)
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
        message = "*Inscrições*\n\n\
        Toque uma opção para se inscrever nela.\n\
        Toque novamente para se desinscrever.\n\n\
        As mensagens de café da manhã são enviadas por volta das 6 da manhã.\n\
        As de almoço por volta das 10 e as de jantar por volta das 16."

        subs = self.subs

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Café da manhã' + (' - inscrito' if subs['breakfast'] else ''), callback_data='sub.breakfast')],
            [
                InlineKeyboardButton(text='Almoço' + (' - inscrito' if subs['lunch'] else ''), callback_data='sub.lunch'),
                InlineKeyboardButton(text='Almoço veg' + (' - inscrito' if subs['veglunch'] else ''), callback_data='sub.veglunch')
            ],
            [
                InlineKeyboardButton(text='Jantar' + (' - inscrito' if subs['dinner'] else ''), callback_data='sub.dinner'),
                InlineKeyboardButton(text='Jantar veg' + (' - inscrito' if subs['vegdinner'] else ''), callback_data='sub.vegdinner')
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
