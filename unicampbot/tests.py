from .core import receiver
from unicampbot.communication.basic import bot


def test():
    """Test stuff"""
    bot.deleteWebhook()

    def maximum_offset(queries, offset):
        for i in queries:
            if i['update_id'] > offset and len(queries) > 1:
                return maximum_offset(bot.getUpdates(offset=i['update_id']), i['update_id'])
            if len(queries) == 1:
                return i
    query = maximum_offset(bot.getUpdates(), offset=10)
    receiver(query)
