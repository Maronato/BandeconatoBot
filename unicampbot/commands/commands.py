from unicampbot.communication.basic import markdown_message, custom_keyboard
from unicampbot.menu.keyboards import day_keyboard
from unicampbot.subscriptions.subscription import Subscription


def start(chat_id, group=False):
    response = """
*"O que vai ter no bandeco hoje?"*

Essa é uma pergunta que você costuma fazer?
Tem preguiça de ir olhar o app da unicamp, ou quer poder receber uma notificação sobre o cardápio do dia?

_Seus problemas acabaram_

*Comandos*
/cardapio - Veja os cardápios
/inscrever - Controle suas inscrições
/ajuda - Obter ajuda
/codigo - Código do bot
    """
    markdown_message(chat_id, response, reply_markup=keyboard(group))


def help(chat_id, group=False):
    response = """
*Ajuda*

A lista de comandos disponíveis é:
*Comandos*
/cardapio - Veja os cardápios
/inscrever - Controle suas inscrições
/ajuda - Obter ajuda
/codigo - Código do bot

Se precisar de suporte, entre em contato com o desenvolvedor:
@Maronato
    """
    markdown_message(chat_id, response, reply_markup=keyboard(group))


def codigo(chat_id, group=False):
    response = """
*Código*

Todo o código fonte dele pode ser encontrado aqui:
https://github.com/Maronato/BandeconatoBot

Esse bot usa essa API para coletar os cardápios:
https://github.com/Maronato/BandecoAPI
    """
    markdown_message(chat_id, response, reply_markup=keyboard(group))


def cardapio(chat_id):
    day_keyboard(chat_id)


def inscrever(chat_id):
    Subscription(chat_id).interact()


def unknown(chat_id, group=False):
    response = "Não reconheço esse comando :(\n\n/ajuda - Lista de comandos"
    markdown_message(chat_id, response, reply_markup=keyboard(group))


def keyboard(group):
    if not group:
        reply_markup = custom_keyboard()
    else:
        reply_markup = None
    return reply_markup
