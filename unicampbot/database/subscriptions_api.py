import json
from .dynamo_db import getkey, setkey, get_all


def get_subscription(chat_id):
    key = {'chat_id': {'S': str(chat_id)}}
    try:
        sub = getkey(key)
        if sub is not None:
            sub = json.loads(sub['Item']['sub']['S'])
    except KeyError:
        return None
    return sub


def set_subscription(chat_id, sub, extra={'S': ""}):
    row = {'chat_id': {'S': str(chat_id)}, 'sub': {'S': json.dumps(sub)}, "extra": {"M": extra}}
    return setkey(chat_id, row)


def get_all_subscriptions():
    subs = get_all()
    all_subs = []
    for sub in subs['Items']:
        try:
            c_id = int(sub['chat_id']['S'])
            sub = json.loads(sub['sub']['S'])
            all_subs.append({"id": c_id, "sub": sub})
        except Exception as e:
            pass
    return all_subs
