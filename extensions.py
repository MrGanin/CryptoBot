import json
import requests
from config import keys

class APIExeption(Exception):
    pass

class API:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIExeption(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIExeption(f'Не удалось обработать валюту {quote}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIExeption(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIExeption(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://api.currencyapi.com/v3/latest?apikey=cur_live_LIwetRnyLoJo90CPiOYwiZZ8duUnnhcISj5oilax&currencies={base_ticker}&base_currency={quote_ticker}')
        total_base = json.loads(r.content)['data'][base_ticker]['value']

        return float(total_base)
