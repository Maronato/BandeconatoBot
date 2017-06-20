# Bandeconato Bot
Telegram bot that interactively shows Unicamp's lunch and dining menu and manages subscriptions.

Users can both subscribe to regular menu updates and check specific menus.

# How do I set it up?
This bot is supposed to be hosted in an AWS's lambda function and receive requests through a webhook using the API Gateway. It also uses a DynamoDB table to manage users' subscriptions.

# Does it work?
Yep, check it out [here](https://telegram.me/BandeconatoBot)


# TODO
- Login and cache(?) passwords for [card balance report](https://www1.sistemas.unicamp.br/SmartCardWeb/consultaSaldo.do)
