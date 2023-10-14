import requests
import config


def get_currency(currency_from, currency_to):
    url = f'https://rest.coinapi.io/v1/exchangerate/{currency_from}/{currency_to}'
    headers = {'X-CoinAPI-Key': config.API_KEY}
    response = requests.get(url, headers=headers).json()
    return response
