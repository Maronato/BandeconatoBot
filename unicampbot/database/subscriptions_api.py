import json
from .dynamo_db import getkey, setkey, deletekey, get_all


def get_chat(chat_id):
    key = {'chat_id': {'S': str(chat_id)}}
    try:
        return getkey(key)['Item']
    except KeyError:
        return None


def delete_chat(chat_id):
    key = {'chat_id': {'S': str(chat_id)}}
    return deletekey(key)


def get_subscription(chat_id):
    sub = get_chat(chat_id)
    if sub is not None:
        return json.loads(sub['sub']['S'])
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
            n_sub = json.loads(sub['sub']['S'])
            try:
                extra = sub['extra']['M']
                all_subs.append({"id": c_id, "sub": n_sub, "extra": extra})
            except KeyError as e:
                all_subs.append({"id": c_id, "sub": n_sub})
                print("INFO User {} does not have Extra info".format(c_id))
        except Exception as e:
            print("ERROR: ", e.__class__, e)
    return all_subs
