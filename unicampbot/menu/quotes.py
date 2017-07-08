from random import choice


quotes = [
    'Parece gostoso!',
    'Será que vai tá bom?',
    'Pelo menos não é cozido misto',
    'Será que tem feirinha hoje?',
    'Esse é o meu favorito',
    'O que será que tem no dia seguinte?',
    'Nossa, que fome',
    "To bandeco or not, that's the question"
]


def quote_choice():
    return "*" + choice(quotes) + "*"
