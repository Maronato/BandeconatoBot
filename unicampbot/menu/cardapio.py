import requests
from bs4 import BeautifulSoup
from datetime import timedelta, datetime
from random import choice


BASE_URL = "http://catedral.prefeitura.unicamp.br/cardapio.php?d="


def format_string(text):
    def remove_excess_spaces(text):
        return ' '.join(text.strip().split()).strip()

    def capitalize_after_period(text):
        return '. '.join([word.strip().capitalize() for word in text.split('.')]).strip()

    def capitalize_after_two(text):
        return ': '.join([(word.strip()[0].capitalize() + word.strip()[1:]) if len(word) > 1 else '' for word in text.split(':')]).strip()

    return [remove_excess_spaces(capitalize_after_two(remove_excess_spaces(capitalize_after_period(remove_excess_spaces(line.text))))) for line in text]


class Cardapio:

    def __init__(self, delta=0):
        date = (datetime.today() + timedelta(days=delta, hours=-3)).strftime('%Y-%m-%d')
        try:
            response = requests.get(BASE_URL + date, timeout=2)
            response.raise_for_status()
            if response.text.find("Não existe cardápio") >= 0:
                raise LookupError("Não existe cardápio")
            self.soup = BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.Timeout:
            self.soup = "_O servidor da Unicamp demorou demais para responder._\n_Tente novamente mais tarde._"
        except requests.HTTPError:
            self.soup = "_O servidor da Unicamp está sendo malcriado._"
        except LookupError:
            self.soup = "*Esse cardápio não existe.*\n_Será que não tem bandeco?_"
        except requests.exceptions.ConnectionError:
            self.soup = "_Não foi possível estabelecer uma conexão com o servidor da Unicamp._"
        except Exception as e:
            self.soup = "_Algo bem errado aconteceu:_\n\n" + str(type(e).__name__)

    @property
    def breakfast(self):
        if type(self.soup) is str:
            return self.soup
        raw = self.soup.find_all("div", {"class": "fundo_cardapio"})
        return '\n'.join(format_string(raw)).strip()

    @property
    def lunch(self):
        if type(self.soup) is str:
            return self.soup
        raw = self.soup.find_all("table", {"class": "fundo_cardapio"})[0].find_all("td")
        return '\n'.join(format_string(raw)).strip()

    @property
    def veglunch(self):
        if type(self.soup) is str:
            return self.soup
        raw = self.soup.find_all("table", {"class": "fundo_cardapio"})[1].find_all("td")
        return '\n'.join(format_string(raw)).strip()

    @property
    def dinner(self):
        if type(self.soup) is str:
            return self.soup
        raw = self.soup.find_all("table", {"class": "fundo_cardapio"})[2].find_all("td")
        return '\n'.join(format_string(raw)).strip()

    @property
    def vegdinner(self):
        if type(self.soup) is str:
            return self.soup
        raw = self.soup.find_all("table", {"class": "fundo_cardapio"})[3].find_all("td")
        return '\n'.join(format_string(raw)).strip()

    @property
    def quote(self):
        return "*" + choice(self.quotes) + "*"

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
