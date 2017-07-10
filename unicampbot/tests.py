from telepot import Bot
from os.path import dirname, abspath
import os

# set environ variables
path = dirname(dirname(abspath(__file__))) + "/.env"
with open(path, 'r') as f:
    for line in f:
        line.split("=")
        os.environ[line.split("=")[0]] = line.split("=")[1].strip()
bot = Bot(os.environ.get('TELEGRAM_TOKEN'))
from .core import receiver, send_subscriptions


def test():
    """Test stuff"""
    bot.deleteWebhook()

    def maximum_offset(queries, offset):
        for i in queries:
            if i['update_id'] > offset and len(queries) > 1:
                offset = i['update_id']
                return maximum_offset(bot.getUpdates(offset=offset), offset)
            if len(queries) == 1:
                offset = i['update_id']
                return i, offset
    offset = 0
    while True:
        try:
            of = offset
            query, offset = maximum_offset(bot.getUpdates(), offset)
            if of != offset:
                receiver(query)
                print("\n\nreceived: " + str(query))
        except KeyboardInterrupt:
            reset_webhook()
            break
        except Exception as e:
            print(e)


def reset_webhook():
    return bot.setWebhook(os.environ.get('API_URL'))


def test_notification(menu_type, days_delta=0, hours_delta=-3):
    bot.deleteWebhook()
    args = {"menu": menu_type, "debug": True, "hours_delta": hours_delta, "debug_days_delta": days_delta}
    send_subscriptions(args)
    reset_webhook()
