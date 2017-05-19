from unicampbot.communication.basic import markdown_message
from unicampbot.menu.keyboards import day_keyboard
from unicampbot.subscriptions.subscription import Subscription


def start(chat_id):
    response = """
    *"O que vai ter no bandeco hoje?"*

    Essa é uma pergunta que você costuma fazer?
    Tem preguiça de ir olhar o app da unicamp, ou quer poder receber uma notificação sobre o cardápio do dia?

    _Seus problemas acabaram_

    *Comandos*
    /cardapio - Veja os cardápios
    /inscrever - Controle suas inscrições
    /help - Obter ajuda
    /creditos - Créditos do Bot e acesso ao código
    """
    markdown_message(chat_id, response)


def help(chat_id):
    response = """
    *Ajuda*

    Está com problemas para usar o bot?

    Entre em contato comigo por:
    @GustavoMaronato

    *Comandos*
    /cardapio - Veja os cardápios
    /inscrever - Controle suas inscrições
    /help - Obter ajuda
    /creditos - Créditos do Bot e acesso ao código
    """
    markdown_message(chat_id, response)


def creditos(chat_id):
    response = """
    *Créditos*

    Esse bot foi feito por
    @GustavoMaronato

    e todo o código fonte dele é aberto sob a licença MIT:
    https://github.com/Maronato/BandeconatoBot

    Sinta-se livre para colaborar!
    """
    markdown_message(chat_id, response)


def cardapio(chat_id):
    day_keyboard(chat_id)


def inscrever(chat_id):
    Subscription(chat_id).interact()
